"""Persist and read per-user LLM spend on ``users.llm_cost``."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.usage.constants import WINDOW_HOURS


def llm_window_exhausted(llm_cost: dict[str, Any] | None, cap_micro_usd: int, now: datetime) -> bool:
    """
    Return True when the rolling window is still active and spend has reached the cap.

    Missing ``llm_cost`` or an expired ``renews_on`` means the user may proceed (new window on next commit).

    This function uses explicit guards and returns a boolean; it does not catch exceptions or hide
    invalid ``llm_cost`` shapes beyond treating absent fields as “not exhausted” for gating purposes.
    """
    if cap_micro_usd <= 0:
        return False
    if not llm_cost:
        return False
    renews_on = llm_cost.get("renews_on")
    curr = int(llm_cost.get("curr_window") or 0)
    if renews_on is None:
        return False
    if now >= renews_on:
        return False
    return curr >= cap_micro_usd


class LlmCostService:
    """Atomic updates to ``users.llm_cost`` (micro-USD ``curr_window``, ``total``, ``renews_on``)."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db

    async def commit_delta_micro_usd(self, user_id: str, delta_micro_usd: int) -> None:
        """
        Add ``delta_micro_usd`` to lifetime ``total`` and to ``curr_window`` (or reset window if expired).

        Rolling window: when ``renews_on`` is absent or ``now >= renews_on``, set ``curr_window`` to
        ``delta`` only and ``renews_on`` to now + 24 hours; otherwise increment ``curr_window``.
        """
        if delta_micro_usd <= 0:
            return
        oid = ObjectId(user_id)
        now = datetime.utcnow()
        renews = now + timedelta(hours=WINDOW_HOURS)
        pipeline: list[dict[str, Any]] = [
            {
                "$set": {
                    "_expired": {
                        "$or": [
                            {"$eq": [{"$ifNull": ["$llm_cost.renews_on", None]}, None]},
                            {"$lte": ["$llm_cost.renews_on", now]},
                        ]
                    }
                }
            },
            {
                "$set": {
                    "llm_cost.curr_window": {
                        "$cond": [
                            "$_expired",
                            delta_micro_usd,
                            {"$add": [{"$ifNull": ["$llm_cost.curr_window", 0]}, delta_micro_usd]},
                        ]
                    },
                    "llm_cost.renews_on": {
                        "$cond": [
                            "$_expired",
                            renews,
                            {"$ifNull": ["$llm_cost.renews_on", renews]},
                        ]
                    },
                    "llm_cost.total": {"$add": [{"$ifNull": ["$llm_cost.total", 0]}, delta_micro_usd]},
                }
            },
            {"$unset": ["_expired"]},
        ]
        await self._db["users"].update_one({"_id": oid}, pipeline)
