"""Request-scoped LLM cost tracking, budget HTTP checks, and FastAPI dependencies for spend gates."""

from __future__ import annotations

import contextvars
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.auth.auth_service import AuthService
from app.dependency_injector import DependencyInjector
from app.usage.llm_cost_service import llm_window_exhausted

_micro_stack: contextvars.ContextVar[Optional[list[int]]] = contextvars.ContextVar(
    "request_llm_cost_micro_stack", default=None
)

security = HTTPBearer(auto_error=True)


def start_request_llm_cost_tracking() -> None:
    """Begin accumulating micro-USD for the current asyncio context; replaces any prior list."""
    _micro_stack.set([])


def stop_request_llm_cost_tracking() -> None:
    """Clear tracking for this context."""
    _micro_stack.set(None)


def add_request_llm_cost_micro(delta: int) -> None:
    """Add micro-USD to the current request total if tracking is active."""
    if delta <= 0:
        return
    bucket = _micro_stack.get()
    if bucket is not None:
        bucket.append(delta)


def get_request_llm_cost_micro_total() -> int:
    """Return accumulated micro-USD for this context, or 0 if not tracking."""
    bucket = _micro_stack.get()
    if not bucket:
        return 0
    return sum(bucket)


def is_request_llm_cost_tracking() -> bool:
    """Return True when request-level accumulation is active."""
    return _micro_stack.get() is not None


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
    renews_iso = renews.isoformat() + "Z" if renews and renews.tzinfo is None else (
        renews.isoformat() if renews else None
    )
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "code": "llm_daily_cap",
            "message": "Daily LLM usage limit reached. Try again after the reset time.",
            "renews_on": renews_iso,
            "limit_usd": limit_usd,
        },
    )


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
