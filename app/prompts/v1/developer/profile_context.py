"""Profile context for developer prompts. Agents fetch user profile and extract this context."""

from dataclasses import dataclass
from typing import Optional

from app.prompts.v1.medical_conditions_laws import get_yoga_laws_context


@dataclass
class ProfileContext:
    """Extracted context from user profile for prompt building."""

    hard_priority_summary: str
    medium_priority_summary: str
    laws_context: str


def extract_profile_context(user_doc: Optional[dict]) -> ProfileContext:
    """Extract ProfileContext from a user document. Returns empty context if user is None or has no profile."""
    if not user_doc:
        return ProfileContext("", "", "")
    profile = user_doc.get("profile") or {}
    hard = profile.get("hard_priority_summary") or ""
    medium = profile.get("medium_priority_summary") or ""

    hard_strategy = profile.get("hard_priority_strategy") or {}
    laws_context = get_yoga_laws_context(hard_strategy)
    
    return ProfileContext(hard, medium, laws_context)
