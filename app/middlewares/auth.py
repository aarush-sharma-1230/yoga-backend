"""Bearer JWT validation and loading the authenticated user document from MongoDB."""

from __future__ import annotations

from typing import Any

import jwt
from bson import ObjectId
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.auth.settings import get_auth_settings
from app.dependency_injector import DependencyInjector
from app.globals.errors import AuthenticationError, NotFoundError

bearer_scheme = HTTPBearer(auto_error=True)


def decode_bearer_access_token(bearer_token: str) -> dict[str, Any]:
    """
    Decode and validate an access JWT (signature, expiry, required claims).

    Returns claim dict with string ``_id``. Raises ``AuthenticationError`` if invalid.
    """

    try:
        settings = get_auth_settings()
        payload = jwt.decode(
            bearer_token,
            settings.jwt_secret,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "_id"]},
        )
        payload["_id"] = str(payload["_id"])
        return payload

    except jwt.PyJWTError as exc:
        raise AuthenticationError() from exc


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncIOMotorDatabase = Depends(DependencyInjector.get_database),
) -> dict[str, Any]:
    """
    Validate the Bearer access JWT, load the user row from MongoDB, and return it.

    The document excludes ``password``. Raises ``NotFoundError`` if the user id from the token
    has no matching document.
    """

    payload = decode_bearer_access_token(credentials.credentials)

    user_id = payload["_id"]
    user = await db["users"].find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        raise NotFoundError()

    return user


__all__ = [
    "bearer_scheme",
    "decode_bearer_access_token",
    "get_current_user",
]
