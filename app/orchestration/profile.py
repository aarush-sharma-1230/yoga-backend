"""User profile extraction for orchestration and prompt builders."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

from app.prompts.v4.medical_conditions_laws import get_yoga_laws_context


@dataclass
class ProfileContext:
    """Extracted context from user profile for prompt building."""

    hard_priority_summary: str
    medium_priority_summary: str
    laws_context: str


def extract_profile_bundle(user_doc: Optional[dict]) -> ProfileContext:
    """
    Read a user document once and return ``ProfileContext`` (summaries and rule-derived laws text).

    Uses stored ``hard_priority_strategy`` only server-side for ``get_yoga_laws_context``;
    it is not exposed to downstream prompts.
    """
    if not user_doc:
        return ProfileContext("", "", "")

    profile = user_doc.get("profile") or {}
    hard_strategy = profile.get("hard_priority_strategy") or {}
    hard = profile.get("hard_priority_summary") or ""
    medium = profile.get("medium_priority_summary") or ""
    laws_context = get_yoga_laws_context(hard_strategy)

    return ProfileContext(hard, medium, laws_context)


def build_profiler_profile_bundle(user_doc: Optional[dict]) -> dict[str, Any]:
    """
    Produce state fragments for the profiler node: ``profile_context`` dict only.
    """
    ctx = extract_profile_bundle(user_doc)
    return {"profile_context": asdict(ctx)}
