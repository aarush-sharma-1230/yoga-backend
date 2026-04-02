"""User prompt: pre-sequence request review.

Prompt function receives pre-computed values only. No function calls inside.
All data fetching and processing is done by the RequestReviewer agent.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.prompts.v4.developer.profile_context import ProfileContext


def get_request_review_prompt(
    ctx: ProfileContext,
    hard_strategy: dict,
    medium_strategy: dict,
    theme: dict,
    duration_minutes: int,
    user_notes: str | None,
) -> str:
    """
    Build the user prompt for the request reviewer.

    Provides both the LLM-generated profile summaries and the raw strategy
    dicts so the reviewer can cross-reference specifics.
    """
    sections: list[str] = []

    sections.append("<PRACTITIONER_PROFILE>")
    if ctx.hard_priority_summary:
        sections.append(f"Medical & safety summary: {ctx.hard_priority_summary}")
    if ctx.medium_priority_summary:
        sections.append(f"Goals & experience summary: {ctx.medium_priority_summary}")
    if ctx.laws_context:
        sections.append(f"\n{ctx.laws_context}")
    sections.append("</PRACTITIONER_PROFILE>")

    sections.append("")
    sections.append(f"<RAW_MEDICAL_DATA>\n{json.dumps(hard_strategy, indent=2)}\n</RAW_MEDICAL_DATA>")

    sections.append("")
    sections.append(f"<RAW_GOALS_DATA>\n{json.dumps(medium_strategy, indent=2)}\n</RAW_GOALS_DATA>")

    sections.append("")
    display_name = theme.get("display_name") or ""
    functional_category = theme.get("functional_category") or ""
    description = theme.get("description") or ""
    sections.append("<SESSION_REQUEST>")
    sections.append(f"Theme: {display_name} ({functional_category}). {description}")
    sections.append(f"Duration: {duration_minutes} minutes")
    if user_notes:
        sections.append(f"User notes: {user_notes}")
    sections.append("</SESSION_REQUEST>")

    sections.append("")
    sections.append(
        "Review the practitioner's profile against the session request. "
        "Identify any conflicts, ambiguities, or missing information that could affect sequence safety or quality. "
        "Return your assessment as the structured JSON output described in your instructions."
    )

    return "\n".join(sections)
