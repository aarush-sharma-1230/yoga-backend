"""User prompt: custom yoga sequence generation.

Prompt functions receive pre-computed values only. No function calls inside.
All data fetching and processing is done upstream by the orchestration graph.
"""


def get_sequence_user_prompt(
    session_briefing: str,
    posture_range_lo: int,
    posture_range_hi: int,
    theme: dict,
    review_qa_context: str | None = None,
    sequence_review_feedback: str | None = None,
) -> str:
    """
    Build the user prompt for sequence generation.

    Receives a single ``session_briefing`` paragraph (produced by the briefing
    node) that already blends practitioner profile, theme, and user notes.
    """
    sections: list[str] = []

    if session_briefing:
        sections.append("PRACTITIONER BRIEFING FOR THIS SESSION")
        sections.append("")
        sections.append(session_briefing)
        sections.append("")

    if review_qa_context:
        sections.append("PRIORITY REVIEW CLARIFICATIONS (from practitioner intake)")
        sections.append("")
        sections.append(review_qa_context)
        sections.append("")

    if sequence_review_feedback:
        sections.append("SEQUENCE REVISION FEEDBACK (from automated safety/alignment review)")
        sections.append("")
        sections.append(sequence_review_feedback)
        sections.append("")

    sections.append("SESSION PARAMETERS")
    sections.append("")
    params = []
    params.append(
        f"- Aim for approximately {posture_range_lo}\u2013{posture_range_hi} postures total. Prioritize smooth transitions over hitting an exact count."
    )
    display_name = theme.get("display_name") or ""
    functional_category = theme.get("functional_category") or ""
    description = theme.get("description") or ""
    params.append(f"- Practice theme: {display_name} ({functional_category}). {description}")
    sections.extend(params)
    sections.append("")
    sections.append(
        "Design a sequence for this practitioner that fits the requested theme and session length. "
        "Warm-up and early grounding should feel easy on the joints: choose gentler catalogue options and shorter static_hold times there; build intensity gradually. "
        "Return JSON with reasoning, name, and postures (flat array in flow order). "
        "Each item has posture_intent: static_hold (posture_id, recommended_modification, hold_time_seconds > 0), "
        "transitional_hub (posture_id, recommended_modification only\u2014no hold_time_seconds), "
        "interval_set (rounds, hold_time_seconds > 0, rest_time_seconds >= 0, work_posture and recovery_posture each with posture_id and recommended_modification only), "
        'or vinyasa_loop (rounds >= 1, cycle_postures with at least 2 entries each with posture_id and recommended_modification; parent recommended_modification must be ""). '
        "Use transitional_hub to bridge gaps; use interval_set for timed work/rest; use vinyasa_loop for repeated flowing cycles (e.g. Cat\u2013Cow)."
    )

    return "\n".join(sections)
