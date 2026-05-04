"""FastAPI dependencies combining JWT validation with ``users.llm_cost`` for budget gates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bson import ObjectId
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.auth.auth_service import AuthService
from app.dependency_injector import DependencyInjector

security = HTTPBearer(auto_error=True)


@dataclass(frozen=True)
class UserBudgetAccess:
    """Authenticated user id, token TTL, and latest ``llm_cost`` subdocument from MongoDB."""

    user_id: str
    seconds_until_exp: float
    llm_cost: dict[str, Any] | None


async def get_user_budget_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(DependencyInjector.get_auth_service),
    db: AsyncIOMotorDatabase = Depends(DependencyInjector.get_database),
) -> UserBudgetAccess:
    """Decode Bearer JWT and load ``llm_cost`` for rolling-window spend checks."""
    user_id, seconds_until_exp = auth_service.authenticated_access_context(credentials.credentials)
    doc = await db["users"].find_one({"_id": ObjectId(user_id)}, {"llm_cost": 1})
    lc = doc.get("llm_cost") if doc else None
    return UserBudgetAccess(user_id=user_id, seconds_until_exp=seconds_until_exp, llm_cost=lc)
