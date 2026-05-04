"""HTTP helpers for LLM spend caps on gated routes."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import HTTPException, status

from app.usage.llm_cost_service import llm_window_exhausted


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
