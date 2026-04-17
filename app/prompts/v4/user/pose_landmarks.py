"""User prompt for pose landmark correction (v4). Import this submodule directly; it is not re-exported from ``v4.user``."""

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
Produce a single JSON object with one key: `instruction` (string or null).
* Compare the `checks` array to this practitioner's profile, goals, safety, and medical notes.
* Keep any spoken feedback **as short as possible** while covering what is **not** being performed correctly.
* Give **high-priority** feedback only when the posture is **meaningfully** off; if alignment is acceptable for this person, return **null** (or empty string) for `instruction`.

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

## CHECKS (full array; you judge which issues merit feedback)
{checks_json}

## REQUIRED OUTPUT SHAPE
Return **only** valid JSON:
{{
  "instruction": "<short combined cue, or null if no feedback is needed>"
}}
"""
