"""Shared user-profile extraction for orchestration and prompt builders.

Single place to read ``profile`` from a user document: summaries, laws context,
and raw strategy dicts—without redundant passes over the same fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from app.prompts.v4.medical_conditions_laws import get_yoga_laws_context


@dataclass
class ProfileContext:
    """Extracted context from user profile for prompt building."""

    hard_priority_summary: str
    medium_priority_summary: str
    laws_context: str


def extract_profile_bundle(user_doc: Optional[dict]) -> Tuple[ProfileContext, dict, dict]:
    """
    Read a user document once and return ``ProfileContext`` plus raw strategy dicts.

    ``hard_strategy`` and ``medium_strategy`` are the stored JSON blobs;
    ``ProfileContext`` holds summaries and rule-derived ``laws_context``.
    """
    if not user_doc:
        return ProfileContext("", "", ""), {}, {}

    profile = user_doc.get("profile") or {}
    hard_strategy = profile.get("hard_priority_strategy") or {}
    medium_strategy = profile.get("medium_priority_strategy") or {}
    hard = profile.get("hard_priority_summary") or ""
    medium = profile.get("medium_priority_summary") or ""
    laws_context = get_yoga_laws_context(hard_strategy)

    return ProfileContext(hard, medium, laws_context), hard_strategy, medium_strategy
