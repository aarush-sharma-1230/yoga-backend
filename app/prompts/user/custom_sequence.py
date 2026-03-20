"""User prompt: custom yoga sequence generation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from app.prompts.user.sequence_intensity import get_intensity_instruction

if TYPE_CHECKING:
    from app.prompts.developer.profile_context import ProfileContext


def get_sequence_user_prompt(
    ctx: ProfileContext,
    duration_minutes: Optional[int] = None,
    focus: Optional[str] = None,
    intensity_level: Optional[str] = None,
) -> str:
    """
    Build the user prompt for sequence generation. Contains only session-specific
    information: user profile (medical history, priorities), what the user intends,
    and difficulty level.
    """
    sections = []

    # User profile (medical history, priorities)
    if ctx.hard_priority_summary or ctx.medium_priority_summary or ctx.laws_context:
        sections.append("PRACTITIONER PROFILE FOR THIS SESSION")
        sections.append("")
        if ctx.hard_priority_summary:
            sections.append(f"Medical history & safety: {ctx.hard_priority_summary}")
        if ctx.medium_priority_summary:
            sections.append(f"Goals & priorities: {ctx.medium_priority_summary}")
        if ctx.laws_context:
            sections.append("")
            sections.append(ctx.laws_context)
        sections.append("")

    # What the user intends
    sections.append("SESSION PARAMETERS")
    sections.append("")
    params = []
    if duration_minutes:
        params.append(f"- Target duration: approximately {duration_minutes} minutes.")
    if focus:
        params.append(f"- Primary focus: {focus}.")
    if intensity_level:
        params.append(f"- {get_intensity_instruction(intensity_level, duration_minutes)}")
    if not params:
        params.append("- No specific duration, focus, or intensity; design a balanced sequence.")
    sections.extend(params)
    sections.append("")
    sections.append(
        "Design a yoga sequence for this practitioner based on the catalogue in the system prompt. "
        "Match their profile and session parameters. Return a JSON object with reasoning, name, and posture_ids."
    )

    return "\n".join(sections)
