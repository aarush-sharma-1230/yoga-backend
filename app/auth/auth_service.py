import asyncio
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from bson import ObjectId
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.auth.helpers import default_user_profile
from app.auth.settings import get_auth_settings
from app.globals.errors import AuthenticationError, InternalAppError, NotFoundError
from app.schemas.auth import (
    USER_GOALS_FIELD,
    USER_GOALS_SUMMARY_FIELD,
    USER_MEDICAL_PROFILE_FIELD,
    USER_MEDICAL_PROFILE_SUMMARY_FIELD,
    UserGoals,
    UserMedicalProfile
)
from app.usage.llm_cost_service import LlmCostService
from app.usage.request_cost_context import (
            get_request_llm_cost_micro_total,
            start_request_llm_cost_tracking,
            stop_request_llm_cost_tracking,
        )


def _hash_refresh_token(raw: str) -> str:
    """SHA-256 digest of the opaque refresh string for indexed lookup in MongoDB."""

    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase, summary_agent=None):
        self.db = db
        self.summary_agent = summary_agent

    def _create_access_token(self, user_id: str, access_ttl_minutes: int, jwt_secret: str) -> str:
        """Encode a new access JWT for Mongo ``users._id`` string ``user_id``."""

        now = datetime.now(timezone.utc)
        payload = {
            "_id": user_id,
            "iat": now,
            "exp": now + timedelta(minutes=access_ttl_minutes),
        }
        return jwt.encode(payload, jwt_secret, algorithm="HS256")

    def _verify_google_id_token_sync(self, id_token: str) -> dict:
        settings = get_auth_settings()
        return google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            settings.google_client_id,
        )

    async def sign_in_with_google(self, id_token: str) -> dict:
        """
        Verify Google ID token, upsert user, issue access JWT and refresh token.
        Returns ``{"access_token", "refresh_token_raw"}``.
        """

        try:
            idinfo = await asyncio.to_thread(self._verify_google_id_token_sync, id_token)

            google_sub = idinfo["sub"]
            email = idinfo.get("email")
            full_name = idinfo.get("name")
            user_doc = await self.upsert_user_from_google(google_sub, email, full_name)

            uid = str(user_doc["_id"])
            settings = get_auth_settings()
            access = self._create_access_token(uid, settings.access_ttl_minutes, settings.jwt_secret)
            raw_refresh = await self._insert_refresh_token(uid, settings.refresh_ttl_days)

            return {"access_token": access, "refresh_token_raw": raw_refresh}

        except ValueError as exc:
            raise AuthenticationError() from exc

    async def refresh_session(self, raw_refresh_cookie: str | None) -> dict:
        """
        Rotate refresh cookie and return new access and refresh raw values.

        Raises ``AuthenticationError`` when the refresh token is missing, unknown, or expired.
        """

        settings = get_auth_settings()

        result = await self.exchange_refresh_token(raw_refresh_cookie, settings.refresh_ttl_days)
        user_id, new_raw = result

        access = self._create_access_token(user_id, settings.access_ttl_minutes, settings.jwt_secret)
        return {"access_token": access, "refresh_token_raw": new_raw}

    async def get_user_data(self, user_id: str) -> dict:
        """
        Load a projection of the user document by id for callers outside FastAPI routes.

        Returns ``{"status": True, "user": {...}}`` where ``user`` includes ``full_name``, ``email``, and ``profile``.
        """

        user_obj = await self.db["users"].find_one(
            {"_id": ObjectId(user_id)},
            {"password": 0},
        )

        if not user_obj:
            raise NotFoundError()

        return {"status": True, "user": user_obj}

    async def _generate_priority_summary(self, user_id: str, payload: dict, kind: str) -> str:
        """Run the profile summary LLM for ``kind`` (medical profile or goals) and record usage."""

        start_request_llm_cost_tracking()
        try:
            resp = await self.summary_agent.generate_summary(payload, kind)
            summary_text = resp["text"]
        finally:
            total_micro = get_request_llm_cost_micro_total()
            stop_request_llm_cost_tracking()

        if total_micro > 0:
            await LlmCostService(self.db).commit_delta_micro_usd(user_id, total_micro)

        return summary_text

    async def save_user_medical_profile(self, user_id: str, profile: UserMedicalProfile) -> dict:
        """Persist user medical profile and its LLM summary after generation succeeds."""

        doc = profile.model_dump()
        summary_text = await self._generate_priority_summary(user_id, doc, "user_medical_profile")
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    f"profile.{USER_MEDICAL_PROFILE_FIELD}": doc,
                    f"profile.{USER_MEDICAL_PROFILE_SUMMARY_FIELD}": summary_text,
                }
            },
        )
        return {"status": True}

    async def save_user_goals(self, user_id: str, goals: UserGoals) -> dict:
        """Persist user goals and their LLM summary after generation succeeds."""

        doc = goals.model_dump()
        summary_text = await self._generate_priority_summary(user_id, doc, "user_goals")
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    f"profile.{USER_GOALS_FIELD}": doc,
                    f"profile.{USER_GOALS_SUMMARY_FIELD}": summary_text,
                }
            },
        )
        return {"status": True}

    async def upsert_user_from_google(self, google_sub: str, email: str, full_name: str | None) -> dict:
        """Create or update a user row keyed by stable Google ``sub``."""

        now = datetime.now(timezone.utc)
        set_doc: dict = {"google_sub": google_sub, "email": email, "full_name": full_name}

        doc = await self.db["users"].find_one_and_update(
            {"google_sub": google_sub},
            {
                "$set": set_doc,
                "$setOnInsert": {
                    "profile": default_user_profile(),
                    "created_on": now,
                    "llm_cost": {
                        "curr_window": 0,
                        "total": 0,
                        "renews_on": None,
                    },
                },
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        if not doc:
            raise InternalAppError()
        return doc

    async def _insert_refresh_token(self, user_id: str, refresh_ttl_days: int) -> str:
        """Persist a new opaque refresh token and return the raw secret for the cookie."""

        raw = secrets.token_urlsafe(48)
        digest = _hash_refresh_token(raw)
        expires_at = datetime.now(timezone.utc) + timedelta(days=refresh_ttl_days)
        await self.db["refresh_tokens"].insert_one(
            {
                "user_id": ObjectId(user_id),
                "token_hash": digest,
                "expires_at": expires_at,
                "created_on": datetime.now(timezone.utc),
            }
        )

        return raw

    async def exchange_refresh_token(self, raw_cookie: str | None, refresh_ttl_days: int) -> tuple[str, str] | None:
        """
        Validate the refresh cookie value, rotate storage, and return ``(user_id, new_raw_refresh)`` """

        if not raw_cookie or not raw_cookie.strip():
            raise AuthenticationError()

        digest = _hash_refresh_token(raw_cookie.strip())
        doc = await self.db["refresh_tokens"].find_one({"token_hash": digest})
        if not doc:
            raise AuthenticationError()

        exp = doc.get("expires_at")
        if exp is not None:
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if exp < datetime.now(timezone.utc):
                await self.db["refresh_tokens"].delete_one({"_id": doc["_id"]})
                raise AuthenticationError()

        user_id = str(doc["user_id"])
        await self.db["refresh_tokens"].delete_one({"_id": doc["_id"]})
        new_raw = await self._insert_refresh_token(user_id, refresh_ttl_days)
        return user_id, new_raw
