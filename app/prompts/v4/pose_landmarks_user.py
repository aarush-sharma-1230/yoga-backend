"""User prompt for pose landmark correction (v4). Kept outside v4/user/ to avoid heavy package imports."""

from __future__ import annotations

import json
from typing import Any


def get_posture_correction_user_prompt(
    *,
    sequence_name: str | None,
    session_theme_summary: str | None,
    user_notes: str | None,
    review_qa_context: str | None,
    posture_catalogue_json: dict[str, Any] | None,
    posture_client_id: str,
    orientation: str,
    world_landmarks: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> str:
    """
    Build the user message for combined alignment instruction.

    All fetching is done by the agent; this string is self-contained.
    """
    theme_block = session_theme_summary or "(No theme summary available.)"
    notes_block = user_notes.strip() if user_notes and user_notes.strip() else "(None.)"
    review_block = (
        review_qa_context.strip()
        if review_qa_context and review_qa_context.strip()
        else "(No review Q&A stored for this sequence.)"
    )
    posture_block = (
        json.dumps(posture_catalogue_json, indent=2)
        if posture_catalogue_json
        else "(No matching posture catalogue document for this client_id.)"
    )

    landmarks_json = json.dumps(world_landmarks, indent=2)
    checks_json = json.dumps(checks, indent=2)

    return f"""## TASK
You will produce a single JSON object with exactly one key: `instruction` (string).
The instruction is combined real-time alignment feedback for **all** checks below, tailored to this practitioner and session.

## SESSION CONTEXT
- **Sequence name:** {sequence_name or "(unknown)"}
- **Theme / focus (for this session):**
{theme_block}

- **User notes (priority when they conflict with generic goals):**
{notes_block}

- **Questions answered when creating the session (if any):**
{review_block}

## POSTURE CATALOGUE (reference)
Client ID: `{posture_client_id}`
{posture_block}

## CAPTURE
- **Camera orientation:** {orientation}

## LANDMARKS (world space, client order)
{landmarks_json}

## CHECKS TO ADDRESS (all in one instruction)
{checks_json}

## REQUIRED OUTPUT SHAPE
Return **only** valid JSON:
{{
  "instruction": "<one combined spoken-style correction addressing every check>"
}}
"""
