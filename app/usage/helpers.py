"""Request-scoped LLM cost tracking, budget checks, and FastAPI dependencies for spend gates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.dependency_injector import DependencyInjector
from app.globals.errors import LlmBudgetExceededError
from app.usage.llm_cost_service import llm_window_exhausted

security = HTTPBearer(auto_error=True)


def raise_if_llm_daily_cap_exceeded(
    *,
    llm_cost: dict[str, Any] | None,
    cap_micro_usd: int,
    limit_usd: float,
) -> None:
    """
    Raise ``429`` when the user has reached the rolling-window cap.

    ``detail`` includes machine-readable fields for clients.
    """
    now = datetime.utcnow()
    if not llm_window_exhausted(llm_cost, cap_micro_usd, now):
        return
    renews = (llm_cost or {}).get("renews_on")
    renews_iso = renews.isoformat() + "Z" if renews and renews.tzinfo is None else (renews.isoformat() if renews else None)
    raise LlmBudgetExceededError(renews_on=renews_iso, limit_usd=limit_usd)


@dataclass(frozen=True)
class UserBudgetAccess:
    """Authenticated user id, token TTL, and latest ``llm_cost`` subdocument from MongoDB."""

    user_id: str
    seconds_until_exp: float
    llm_cost: dict[str, Any] | None


async def get_user_budget_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: Any = Depends(DependencyInjector.get_auth_service),
    db: AsyncIOMotorDatabase = Depends(DependencyInjector.get_database),
) -> UserBudgetAccess:
    """Decode Bearer JWT and load ``llm_cost`` for rolling-window spend checks."""
    user_id, seconds_until_exp = auth_service.authenticated_access_context(credentials.credentials)
    doc = await db["users"].find_one({"_id": ObjectId(user_id)}, {"llm_cost": 1})
    lc = doc.get("llm_cost") if doc else None
    return UserBudgetAccess(user_id=user_id, seconds_until_exp=seconds_until_exp, llm_cost=lc)


__all__ = [
    "raise_if_llm_daily_cap_exceeded",
    "security",
    "UserBudgetAccess",
    "get_user_budget_access",
]
