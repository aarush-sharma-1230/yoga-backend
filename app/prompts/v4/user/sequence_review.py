"""User prompt: sequence safety and alignment review."""

from __future__ import annotations

import json
from typing import Any


def get_sequence_review_user_prompt(
    *,
    session_briefing: str,
    theme: dict[str, Any],
    duration_minutes: int,
    composer_output: dict[str, Any],
) -> str:
    """
    Build the user message for the sequence reviewer.

    ``composer_output`` is the structured sequence from the composer (e.g. model_dump of CustomSequenceOutput).
    """
    display_name = theme.get("display_name") or ""
    functional_category = theme.get("functional_category") or ""
    description = theme.get("description") or ""

    sections: list[str] = [
        "<SESSION_BRIEFING>",
        session_briefing,
        "</SESSION_BRIEFING>",
        "",
        "<SESSION_REQUEST>",
        f"Theme: {display_name} ({functional_category}). {description}",
        f"Duration: {duration_minutes} minutes",
        "</SESSION_REQUEST>",
        "",
        "<PROPOSED_SEQUENCE_JSON>",
        json.dumps(composer_output, indent=2),
        "</PROPOSED_SEQUENCE_JSON>",
        "",
        "Assess safety and alignment. Return the structured JSON per your instructions.",
    ]
    return "\n".join(sections)
