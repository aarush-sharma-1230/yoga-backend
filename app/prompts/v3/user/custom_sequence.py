"""User prompt: custom yoga sequence generation.

Prompt functions receive pre-computed values only. No function calls inside.
All data fetching and processing is done by the SequenceComposer agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.prompts.v3.developer.profile_context import ProfileContext


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
        params.append(f"- Current session user notes which have to be given priority above user's other goals and medical histories if conflicting: {user_notes}")
    sections.extend(params)
    sections.append("")
    sections.append(
        "Design a sequence for this practitioner that fits the requested theme and session length. "
        "Warm-up and early grounding should feel easy on the joints: choose gentler catalogue options and shorter static_hold times there; build intensity gradually. "
        "Return JSON with reasoning, name, and postures (flat array in flow order). "
        "Each item has posture_intent: static_hold (posture_id, recommended_modification, hold_time_seconds > 0), "
        "transitional_hub (posture_id, recommended_modification only—no hold_time_seconds), "
        "interval_set (rounds, hold_time_seconds > 0, rest_time_seconds >= 0, work_posture and recovery_posture each with posture_id and recommended_modification only), "
        "or vinyasa_loop (rounds >= 1, cycle_postures with at least 2 entries each with posture_id and recommended_modification; parent recommended_modification must be \"\"). "
        "Use transitional_hub to bridge gaps; use interval_set for timed work/rest; use vinyasa_loop for repeated flowing cycles (e.g. Cat–Cow)."
    )

    return "\n".join(sections)
