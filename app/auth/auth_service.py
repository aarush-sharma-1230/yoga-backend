import asyncio
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from bson import ObjectId
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.auth.settings import get_auth_settings
from app.globals.errors import AuthenticationError, InternalAppError, NotFoundError
from app.schemas.auth import HardPriorityStrategy, MediumPriorityStrategy, default_user_profile
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

    def _create_access_token(self, user_id: str) -> str:
        """Encode a new access JWT for Mongo ``users._id`` string ``user_id``."""

        settings = get_auth_settings()
        now = datetime.now(timezone.utc)
        payload = {
            "_id": user_id,
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_ttl_minutes),
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    @staticmethod
    def decode_access_token_payload(bearer_token: str) -> dict[str, Any]:
        """
        Decode and validate an access JWT (signature, expiry, required claims).

        Returns claim dict with string ``_id`` (Mongo ``users._id``). Raises ``AuthenticationError`` if invalid.
        """

        settings = get_auth_settings()
        try:
            payload = jwt.decode(
                bearer_token,
                settings.jwt_secret,
                algorithms=["HS256"],
                options={"require": ["exp", "iat", "_id"]},
            )
        except jwt.PyJWTError as exc:
            raise AuthenticationError() from exc
        payload["_id"] = str(payload["_id"])
        return payload

    @staticmethod
    def _bearer_context_from_token(bearer_token: str) -> tuple[str, float]:
        """
        Decode a Bearer token and return ``(user_id, seconds_until_exp)``.

        Raises ``AuthenticationError`` if invalid or expired.
        """

        payload = AuthService.decode_access_token_payload(bearer_token)
        exp = payload["exp"]
        if isinstance(exp, datetime):
            exp_ts = exp.timestamp()
        else:
            exp_ts = float(exp)
        now_ts = datetime.now(timezone.utc).timestamp()
        return payload["_id"], exp_ts - now_ts

    def authenticated_access_context(self, bearer_token: str) -> tuple[str, float]:
        """
        Validate a Bearer access JWT for HTTP; return ``(user_id, seconds_until_exp)``.

        Raises ``AuthenticationError`` if the token is invalid or expired.
        """

        return self._bearer_context_from_token(bearer_token)

    @staticmethod
    def user_id_from_access_context(access_context: tuple[str, float]) -> str:
        """Return Mongo ``users._id`` string from the tuple returned by ``authenticated_access_context``."""

        return access_context[0]

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
        except ValueError as exc:
            raise AuthenticationError() from exc

        google_sub = idinfo["sub"]
        email = idinfo.get("email")
        full_name = idinfo.get("name")
        user_doc = await self.upsert_user_from_google(google_sub, email, full_name)
        uid = str(user_doc["_id"])
        settings = get_auth_settings()
        access = self._create_access_token(uid)
        raw_refresh = await self.create_refresh_token_for_user(uid, settings.refresh_ttl_days)

        return {"access_token": access, "refresh_token_raw": raw_refresh}

    async def refresh_session(self, raw_refresh_cookie: str | None) -> dict:
        """
        Rotate refresh cookie and return new access and refresh raw values.

        Raises ``AuthenticationError`` when the refresh token is missing, unknown, or expired.
        """

        settings = get_auth_settings()
        result = await self.exchange_refresh_token(raw_refresh_cookie, settings.refresh_ttl_days)
        if not result:
            raise AuthenticationError()
        user_id, new_raw = result
        access = self._create_access_token(user_id)
        return {"access_token": access, "refresh_token_raw": new_raw}

    async def get_user_data(self, user_id: str):
        user_obj = await self.db["users"].find_one(
            {"_id": ObjectId(user_id)},
            {"full_name": 1, "email": 1, "profile": 1},
        )

        if not user_obj:
            raise NotFoundError()

        return {"status": True, "user": user_obj}

    async def _generate_priority_summary(self, user_id: str, strategy_dict: dict, kind: str) -> str:
        """Run the profile summary LLM for ``kind`` (``\"hard\"`` or ``\"medium\"``) and record usage."""

        start_request_llm_cost_tracking()
        try:
            resp = await self.summary_agent.generate_summary(strategy_dict, kind)
            summary_text = resp["text"]
        finally:
            total_micro = get_request_llm_cost_micro_total()
            stop_request_llm_cost_tracking()
        if total_micro > 0:
            await LlmCostService(self.db).commit_delta_micro_usd(user_id, total_micro)
        return summary_text

    async def save_hard_priority_strategy(self, user_id: str, strategy: HardPriorityStrategy) -> dict:
        """Persist medical / safety strategy and its LLM summary after generation succeeds."""

        doc = strategy.model_dump()
        summary_text = await self._generate_priority_summary(user_id, doc, "hard")
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "profile.hard_priority_strategy": doc,
                    "profile.hard_priority_summary": summary_text,
                }
            },
        )
        return {"status": True}

    async def save_medium_priority_strategy(self, user_id: str, strategy: MediumPriorityStrategy) -> dict:
        """Persist goals / experience strategy and its LLM summary after generation succeeds."""

        doc = strategy.model_dump()
        summary_text = await self._generate_priority_summary(user_id, doc, "medium")
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "profile.medium_priority_strategy": doc,
                    "profile.medium_priority_summary": summary_text,
                }
            },
        )
        return {"status": True}

    async def get_profile(self, user_id: str) -> dict:
        """Fetch user profile by user_id. Returns MongoDB document structure."""
        user = await self.db["users"].find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if not user:
            raise NotFoundError()
        return user

    async def upsert_user_from_google(self, google_sub: str, email: str, full_name: str | None) -> dict:
        """Create or update a user row keyed by stable Google ``sub``."""

        now = datetime.now(timezone.utc)
        set_doc: dict = {"google_sub": google_sub, "email": email}
        if full_name:
            set_doc["full_name"] = full_name
        await self.db["users"].update_one(
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
        )
        doc = await self.db["users"].find_one({"google_sub": google_sub})
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

    async def create_refresh_token_for_user(self, user_id: str, refresh_ttl_days: int) -> str:
        """Issue a new refresh token row and return the raw cookie value."""

        return await self._insert_refresh_token(user_id, refresh_ttl_days)

    async def exchange_refresh_token(self, raw_cookie: str | None, refresh_ttl_days: int) -> tuple[str, str] | None:
        """
        Validate the refresh cookie value, rotate storage, and return ``(user_id, new_raw_refresh)``.

        Returns ``None`` if the token is missing, unknown, or expired.
        """

        if not raw_cookie or not raw_cookie.strip():
            return None
        digest = _hash_refresh_token(raw_cookie.strip())
        doc = await self.db["refresh_tokens"].find_one({"token_hash": digest})
        if not doc:
            return None
        exp = doc.get("expires_at")
        if exp is not None:
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if exp < datetime.now(timezone.utc):
                await self.db["refresh_tokens"].delete_one({"_id": doc["_id"]})
                return None
        user_id = str(doc["user_id"])
        await self.db["refresh_tokens"].delete_one({"_id": doc["_id"]})
        new_raw = await self._insert_refresh_token(user_id, refresh_ttl_days)
        return user_id, new_raw


from app.dependency_injector import DependencyInjector

security = HTTPBearer(auto_error=True)


async def get_access_context(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(DependencyInjector.get_auth_service),
) -> tuple[str, float]:
    """Return ``(user_id, seconds_until_exp)`` for the current Bearer token."""

    return auth_service.authenticated_access_context(credentials.credentials)


async def get_current_user_id(
    context: tuple[str, float] = Depends(get_access_context),
) -> str:
    """Return authenticated Mongo ``users._id`` as string."""

    return AuthService.user_id_from_access_context(context)
