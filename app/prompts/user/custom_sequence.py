"""User prompt: custom yoga sequence generation.

Prompt functions receive pre-computed values only. No function calls inside.
All data fetching and processing is done by the SequenceComposer agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.prompts.developer.profile_context import ProfileContext


def get_sequence_user_prompt(
    ctx: ProfileContext,
    posture_range_lo: int,
    posture_range_hi: int,
    theme: dict,
    user_notes: str | None,
) -> str:
    """
    Build the user prompt for sequence generation. Contains only session-specific
    information: user profile, theme, and what the user intends.

    Receives pre-computed values. No function calls inside.
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
            # sections.append(ctx.laws_context)
        sections.append("")

    # Session parameters
    sections.append("SESSION PARAMETERS")
    sections.append("")
    params = []
    params.append(
        f"- Aim for approximately {posture_range_lo}–{posture_range_hi} postures total. Prioritize smooth transitions over hitting an exact count."
    )
    display_name = theme.get("display_name") or ""
    functional_category = theme.get("functional_category") or ""
    description = theme.get("description") or ""
    params.append(f"- Practice theme: {display_name} ({functional_category}). {description}")
    if user_notes:
        params.append(f"- User notes: {user_notes}")
    sections.extend(params)
    sections.append("")
    sections.append(
        "Design a sequence for this practitioner that fits the requested theme and session length. "
        "Return JSON with reasoning, name, and postures. "
        "Each posture should include posture_id, entry_transitions, and recommended_modification."
    )

    return "\n".join(sections)
