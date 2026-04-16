"""Orchestration helpers for profiler / briefing nodes.

Delegates to :func:`app.profile_extraction.extract_profile_bundle` so profile
fields are computed in one pass (no duplicate reads of the same user document).
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Optional

from app.profile_extraction import extract_profile_bundle


def build_profiler_profile_bundle(user_doc: Optional[dict]) -> dict[str, Any]:
    """
    Produce state fragments for the profiler node: ``profile_context`` dict,
    ``hard_strategy``, and ``medium_strategy``.
    """
    ctx, hard_strategy, medium_strategy = extract_profile_bundle(user_doc)
    return {
        "profile_context": asdict(ctx),
        "hard_strategy": hard_strategy,
        "medium_strategy": medium_strategy,
    }
