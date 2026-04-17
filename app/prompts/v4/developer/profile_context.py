"""Profile context for developer prompts. Canonical types live in ``app.orchestration.profile``."""

from typing import Optional

from app.orchestration.profile import ProfileContext, extract_profile_bundle

__all__ = ["ProfileContext", "extract_profile_context"]


def extract_profile_context(user_doc: Optional[dict]) -> ProfileContext:
    """Extract ProfileContext from a user document. Returns empty context if user is None or has no profile."""
    return extract_profile_bundle(user_doc)
