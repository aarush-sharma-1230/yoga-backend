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
    focus: str | None,
    intensity_instruction: str,
) -> str:
    """
    Build the user prompt for sequence generation. Contains only session-specific
    information: user profile (medical history, priorities), what the user intends,
    and difficulty level.

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
            sections.append(ctx.laws_context)
        sections.append("")

    # What the user intends
    sections.append("SESSION PARAMETERS")
    sections.append("")
    params = []
    params.append(
        f"- Aim for approximately {posture_range_lo}–{posture_range_hi} postures total. Prioritize smooth transitions over hitting an exact count."
    )
    if focus:
        params.append(f"- Primary focus: {focus}.")
    params.append(f"- {intensity_instruction}")
    sections.extend(params)
    sections.append("")
    sections.append(
        "Design a yoga sequence for this practitioner based on the catalogue in the system prompt. "
        "Match their profile and session parameters. Return a JSON object with reasoning, name, and postures. "
        "Each posture has posture_id (main pose to hold), entry_transitions (transitional poses to flow through before holding—e.g. p_downward_dog between standing poses), and recommended_modification. "
        "Use entry_transitions for poses that are meant to be quick passes rather than held; leave empty when none."
    )

    return "\n".join(sections)
