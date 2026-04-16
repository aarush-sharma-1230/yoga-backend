"""User prompt: pre-sequence request review.

Prompt function receives pre-computed values only. No function calls inside.
All data fetching and processing is done upstream by the orchestration graph.
"""


def get_request_review_prompt(
    session_briefing: str,
    theme: dict,
    duration_minutes: int,
) -> str:
    """
    Build the user prompt for the request reviewer.

    Receives a single ``session_briefing`` paragraph (produced by the briefing
    node) that already blends practitioner profile, theme, and user notes.
    """
    sections: list[str] = []

    sections.append("<SESSION_BRIEFING>")
    sections.append(session_briefing)
    sections.append("</SESSION_BRIEFING>")

    sections.append("")
    display_name = theme.get("display_name") or ""
    functional_category = theme.get("functional_category") or ""
    description = theme.get("description") or ""
    sections.append("<SESSION_REQUEST>")
    sections.append(f"Theme: {display_name} ({functional_category}). {description}")
    sections.append(f"Duration: {duration_minutes} minutes")
    sections.append("</SESSION_REQUEST>")

    sections.append("")
    sections.append(
        "Review the session briefing against the session request. "
        "Identify any conflicts, ambiguities, or missing information that could affect sequence safety or quality. "
        "Return your assessment as the structured JSON output described in your instructions."
    )

    return "\n".join(sections)
