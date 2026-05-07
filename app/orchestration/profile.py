"""User profile extraction for orchestration and prompt builders."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

from app.schemas.auth import (
    USER_GOALS_SUMMARY_FIELD,
    USER_MEDICAL_PROFILE_SUMMARY_FIELD,
)


@dataclass
class ProfileContext:
    """Extracted context from user profile for prompt building."""

    user_medical_profile_summary: str
    user_goals_summary: str


def extract_profile_bundle(user_doc: Optional[dict]) -> ProfileContext:
    """Read a user document once and return stored profile summaries for prompts."""
    if not user_doc:
        return ProfileContext("", "")

    profile = user_doc.get("profile") or {}
    medical_summary = profile.get(USER_MEDICAL_PROFILE_SUMMARY_FIELD) or ""
    goals_summary = profile.get(USER_GOALS_SUMMARY_FIELD) or ""

    return ProfileContext(medical_summary, goals_summary)


def build_profiler_profile_bundle(user_doc: Optional[dict]) -> dict[str, Any]:
    """
    Produce state fragments for the profiler node: ``profile_context`` dict only.
    """
    ctx = extract_profile_bundle(user_doc)
    return {"profile_context": asdict(ctx)}
