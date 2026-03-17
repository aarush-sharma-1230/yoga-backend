"""Prompt for generating a custom yoga sequence from user profile and posture catalogue."""

from typing import Optional


def _format_posture_entry(posture: dict) -> str:
    """Build a compact one-line summary of a posture for the catalogue."""
    name = posture.get("name") or {}
    english = name.get("english", "Unknown")
    client_id = posture.get("client_id", "")
    sig = posture.get("anatomical_signature") or {}
    inverted = "INVERTED" if sig.get("is_inverted") else ""
    contra = [c.get("condition", "") for c in (posture.get("contraindications") or []) if isinstance(c, dict)]
    pain = [p.get("condition", "") for p in (posture.get("chronic_pain") or []) if isinstance(p, dict)]
    entries = posture.get("typical_entries") or []
    exits = posture.get("typical_exits") or []
    intent = posture.get("pose_intent") or []
    intent_str = "; ".join(intent[:2]) if intent else ""
    safety = []
    if contra:
        safety.append(f"avoid/modify for: {', '.join(contra[:4])}")
    if pain:
        safety.append(f"adjust for: {', '.join(pain[:4])}")
    safety_str = " | ".join(safety) if safety else "generally safe"
    flow = f"entries: {', '.join(entries[:3])} | exits: {', '.join(exits[:3])}" if entries or exits else ""
    parts = [f"{client_id}: {english} {inverted}".strip(), safety_str]
    if intent_str:
        parts.append(intent_str)
    if flow:
        parts.append(flow)
    return " | ".join(parts)


def get_custom_sequence_prompt(
    postures: list,
    duration_minutes: Optional[int] = None,
    focus: Optional[str] = None,
) -> str:
    """
    Build the user prompt for custom sequence generation.
    The developer prompt (from get_developer_prompt) already contains user profile and safety laws.
    """
    catalogue_lines = [_format_posture_entry(p) for p in postures]
    catalogue = "\n".join(catalogue_lines)

    constraints = []
    if duration_minutes:
        constraints.append(f"- Target duration: approximately {duration_minutes} minutes.")
    if focus:
        constraints.append(f"- Primary focus: {focus}.")

    constraints_block = "\n".join(constraints) if constraints else "- No specific duration or focus; design a balanced sequence."

    return f"""Your task is to design a custom yoga sequence for the practitioner.

AVAILABLE POSTURES (use client_id exactly as shown)

{catalogue}

CONSTRAINTS

{constraints_block}

- Select ONLY from the postures listed above. Use their client_id exactly.
- Respect the practitioner's profile and safety laws in the system prompt. Exclude, substitute or modify any pose that contraindicates their conditions.
- Create a logical flow: use typical_entries and typical_exits to chain poses (e.g. from Mountain you can go to Upward Salute or Forward Fold).
- Include a mix of categories (standing, seated, supine, prone) for balance unless focus dictates otherwise.
- Sequence length: aim for 6–12 postures for a typical session. Adjust for duration if specified.
- Start with grounding (e.g. Mountain, Easy Pose) and end with rest (e.g. Child's Pose, Corpse Pose).

OUTPUT

Return a JSON object with:
- name: a short, descriptive sequence name (e.g. "Morning Wake-Up", "Hip Release Flow")
- posture_ids: ordered list of client_ids in the sequence (e.g. ["p_mountain", "p_upward_salute", "p_forward_fold", ...])
"""
