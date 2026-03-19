"""User prompt: custom yoga sequence generation."""

from typing import Optional


def _format_contraindication(c: dict) -> str:
    """Format a single contraindication: action(condition): reason → modification."""
    action = c.get("action", "")
    condition = c.get("condition", "")
    reason = c.get("reason", "")
    mod = c.get("recommended_modification") or "none"
    return f"{action}({condition}): {reason} → {mod}"


def _format_chronic_pain(p: dict) -> str:
    """Format a single chronic pain item: action(condition): reason → modification."""
    action = p.get("action", "")
    condition = p.get("condition", "")
    reason = p.get("reason", "")
    mod = p.get("recommended_modification") or "none"
    return f"{action}({condition}): {reason} → {mod}"


def _format_posture_entry(posture: dict) -> str:
    """Build a structured posture entry with inverted, spinal_shape, full contraindications and chronic_pain."""
    name = posture.get("name") or {}
    english = name.get("english", "Unknown")
    client_id = posture.get("client_id", "")
    sig = posture.get("anatomical_signature") or {}
    is_inverted = sig.get("is_inverted", False)
    spinal_shape = sig.get("spinal_shape", "neutral")

    lines = [
        f"{client_id}: {english}",
        f"  inverted: {'yes' if is_inverted else 'no'} | spinal_shape: {spinal_shape}",
    ]

    contra = posture.get("contraindications") or []
    if contra:
        lines.append("  contraindications:")
        for c in contra:
            if isinstance(c, dict):
                lines.append(f"    {_format_contraindication(c)}")
    else:
        lines.append("  contraindications: none")

    pain = posture.get("chronic_pain") or []
    if pain:
        lines.append("  chronic_pain:")
        for p in pain:
            if isinstance(p, dict):
                lines.append(f"    {_format_chronic_pain(p)}")
    else:
        lines.append("  chronic_pain: none")

    entries = posture.get("typical_entries") or []
    exits = posture.get("typical_exits") or []
    flow = f"entries: {', '.join(entries)} | exits: {', '.join(exits)}" if entries or exits else ""
    if flow:
        lines.append(f"  flow: {flow}")

    return "\n".join(lines)


def get_custom_sequence_prompt(
    postures: list,
    duration_minutes: Optional[int] = None,
    focus: Optional[str] = None,
) -> str:
    """Build the user prompt for custom sequence generation."""
    catalogue_blocks = [_format_posture_entry(p) for p in postures]
    catalogue = "\n---\n".join(catalogue_blocks)

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
- Respect the practitioner's profile and safety laws in the system prompt. Match practitioner conditions against each posture's contraindications and chronic_pain. For contraindications: avoid = exclude pose, modify/caution = use recommended_modification or substitute.
- Use inverted and spinal_shape when applying safety rules: e.g. avoid inverted poses for hypertension/glaucoma; avoid flexion for herniated_disc; avoid extension for certain back issues.
- Create a logical flow: strictly use typical_entries and typical_exits (shown as flow) to chain poses.
- Include a mix of categories (standing, seated, supine, prone) for balance unless focus dictates otherwise.
- Sequence length: aim for 6–12 postures for a typical session. Adjust for duration if specified.
- Start with grounding (e.g. Mountain, Easy Pose) and end with rest (e.g. Child's Pose, Corpse Pose).

OUTPUT

Return a JSON object with:
- name: a short, descriptive sequence name (e.g. "Morning Wake-Up", "Hip Release Flow")
- posture_ids: ordered list of client_ids in the sequence (e.g. ["p_mountain", "p_upward_salute", "p_forward_fold", ...])
"""
