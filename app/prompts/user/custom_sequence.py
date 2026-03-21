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
        "Design a yoga sequence in two steps: (1) Select postures that match intent and are safe for this practitioner. "
        "(2) Order them and use entry_transitions only to bridge two held postures that lack a direct transition link (typical_entries/typical_exits). "
        "Entry_transitions must contain ONLY valid client_ids from the catalogue—never invent IDs. Leave entry_transitions empty when the previous pose connects directly. "
        "For short sequences (6–7 postures), use fewer position categories; for long sequences, include more variety. "
        "Return JSON with reasoning, name, and postures (each: posture_id, entry_transitions, recommended_modification)."
    )

    return "\n".join(sections)
