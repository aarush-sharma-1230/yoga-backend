"""User profile extraction for orchestration and prompt builders."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

from app.prompts.v4.medical_conditions_laws import get_yoga_laws_context
from app.schemas.auth import (
    resolve_user_goals_summary,
    resolve_user_medical_profile,
    resolve_user_medical_profile_summary,
)


@dataclass
class ProfileContext:
    """Extracted context from user profile for prompt building."""

    user_medical_profile_summary: str
    user_goals_summary: str
    laws_context: str


def extract_profile_bundle(user_doc: Optional[dict]) -> ProfileContext:
    """
    Read a user document once and return ``ProfileContext`` (summaries and rule-derived laws text).

    Uses stored ``user_medical_profile`` only server-side for ``get_yoga_laws_context``;
    it is not exposed to downstream prompts as raw structured data.
    """
    if not user_doc:
        return ProfileContext("", "", "")

    profile = user_doc.get("profile") or {}
    medical_profile = resolve_user_medical_profile(profile)
    medical_summary = resolve_user_medical_profile_summary(profile)
    goals_summary = resolve_user_goals_summary(profile)
    laws_context = get_yoga_laws_context(medical_profile)

    return ProfileContext(medical_summary, goals_summary, laws_context)


def build_profiler_profile_bundle(user_doc: Optional[dict]) -> dict[str, Any]:
    """
    Produce state fragments for the profiler node: ``profile_context`` dict only.
    """
    ctx = extract_profile_bundle(user_doc)
    return {"profile_context": asdict(ctx)}
