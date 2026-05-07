"""LLM cost tracking helpers and budget enforcement for spend gates."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.globals.errors import LlmBudgetExceededError
from app.usage.llm_cost_service import llm_window_exhausted


def raise_if_llm_daily_cap_exceeded(
    *,
    llm_cost: dict[str, Any] | None,
    cap_micro_usd: int,
    limit_usd: float,
) -> None:
    """
    Raise ``429`` when the user has reached the rolling-window cap.

    Prefer ``enforce_user_llm_budget`` for new code; this name is kept for compatibility.
    """
    now = datetime.utcnow()
    if not llm_window_exhausted(llm_cost, cap_micro_usd, now):
        return
    renews = (llm_cost or {}).get("renews_on")
    renews_iso = renews.isoformat() + "Z" if renews and renews.tzinfo is None else (renews.isoformat() if renews else None)
    raise LlmBudgetExceededError(renews_on=renews_iso, limit_usd=limit_usd)


def enforce_user_llm_budget(
    *,
    llm_cost: dict[str, Any] | None,
    cap_micro_usd: int,
    limit_usd: float,
) -> None:
    """
    Raise when the authenticated user has exceeded the rolling-window LLM usage cap.

    Single entry point for user-side usage limits on LLM endpoints; raises ``429`` with
    ``error.code`` = ``user_usage_limit_exceeded``.
    """
    raise_if_llm_daily_cap_exceeded(llm_cost=llm_cost, cap_micro_usd=cap_micro_usd, limit_usd=limit_usd)


__all__ = [
    "enforce_user_llm_budget",
    "raise_if_llm_daily_cap_exceeded",
]
