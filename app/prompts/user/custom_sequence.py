"""User prompt: custom yoga sequence generation."""

from typing import Optional

from app.prompts.user.sequence_intensity import get_intensity_spec


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
    """Build a structured posture entry with anatomical data, intensity_profile, contraindications and chronic_pain."""
    name = posture.get("name") or {}
    english = name.get("english", "Unknown")
    client_id = posture.get("client_id", "")
    sig = posture.get("anatomical_signature") or {}
    is_inverted = sig.get("is_inverted", False)
    spinal_shape = sig.get("spinal_shape", "neutral")

    # Laterality (symmetry/asymmetry)
    laterality = sig.get("laterality") or {}
    lat_type = laterality.get("type", "symmetrical")
    active_side = laterality.get("active_side", "neutral")
    paired_pose = laterality.get("paired_pose", "")
    lat_str = f"laterality: {lat_type}"
    if lat_type == "asymmetrical":
        lat_str += f" | active_side: {active_side}"
        if paired_pose:
            lat_str += f" | paired_pose: {paired_pose}"

    # Counterpose
    requires_counter = sig.get("requires_counter_pose", False)
    counter_poses = sig.get("recommended_counter_poses") or []
    counter_str = f"requires_counter_pose: {'yes' if requires_counter else 'no'}"
    if counter_poses:
        counter_str += f" | recommended: {', '.join(counter_poses)}"
    else:
        counter_str += " | recommended: none"

    # Intensity profile (1–5 scale: targets and demands per area)
    ip = posture.get("intensity_profile") or {}
    musc = ip.get("muscular_load") or {}
    mob = ip.get("mobility_load") or {}
    ip_str = (
        f"intensity: exertion={ip.get('overall_exertion', 1)} balance={ip.get('balance_requirement', 1)} | "
        f"muscular: core={musc.get('core', 1)} upper={musc.get('upper_body', 1)} lower={musc.get('lower_body', 1)} | "
        f"mobility: posterior_chain={mob.get('posterior_chain', 1)} hips={mob.get('hips_and_pelvis', 1)} "
        f"spine={mob.get('spine', 1)} shoulders={mob.get('shoulders_and_chest', 1)}"
    )

    lines = [
        f"{client_id}: {english}",
        f"  inverted: {'yes' if is_inverted else 'no'} | spinal_shape: {spinal_shape}",
        f"  {lat_str}",
        f"  {counter_str}",
        f"  {ip_str}",
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
    intensity_level: Optional[str] = None,
) -> str:
    """Build the user prompt for custom sequence generation."""
    catalogue_blocks = [_format_posture_entry(p) for p in postures]
    catalogue = "\n---\n".join(catalogue_blocks)

    constraints = []
    if duration_minutes:
        constraints.append(f"- Target duration: approximately {duration_minutes} minutes.")
    if focus:
        constraints.append(f"- Primary focus: {focus}.")

    if intensity_level:
        spec = get_intensity_spec(intensity_level, duration_minutes)
        constraints.append("Intensity distribution (select postures whose overall_exertion matches these targets):")
        constraints.append(spec.to_prompt_text())

    constraints_block = "\n".join(constraints) if constraints else "- No specific duration or focus; design a balanced sequence."

    return f"""Your task is to design a custom yoga sequence for the practitioner.

AVAILABLE POSTURES (use client_id exactly as shown)

{catalogue}

CONSTRAINTS

{constraints_block}

- Select ONLY from the postures listed above. Use their client_id exactly.
- Respect the practitioner's profile and safety laws in the system prompt. Match practitioner conditions against each posture's contraindications and chronic_pain. For contraindications: avoid = exclude pose, modify/caution = use recommended_modification or substitute.
- Use intensity_profile to match postures to the practitioner's conditions: mobility (posterior_chain, hips, spine, shoulders) = stretch demand—caution with stretch-sensitive areas (e.g. groin injury: avoid high hips mobility). Muscular (core, upper, lower) = strength/load demand—strengthening can sometimes help, but avoid heavy load on acutely injured areas.
- Use inverted and spinal_shape when applying safety rules: e.g. avoid inverted poses for hypertension/glaucoma; avoid flexion for herniated_disc; avoid extension for certain back issues.
- Use laterality for asymmetrical poses: include both sides (e.g. p_tree_left and p_tree_right) where applicable; paired_pose indicates the opposite-side variant for sequencing.
- For poses with requires_counter_pose: yes, include one of the recommended_counter_poses shortly after to balance the body.
- Create a logical flow: strictly use typical_entries and typical_exits (shown as flow) to chain poses.
- Include a mix of categories (standing, seated, supine, prone) for balance unless focus dictates otherwise.
- Sequence length: aim for 6–12 postures for a typical session (or follow the intensity distribution above when specified). Adjust for duration if specified.
- Start with grounding (e.g. Mountain, Easy Pose) and end with rest (e.g. Child's Pose, Corpse Pose).

OUTPUT

Return a JSON object with:
- reasoning: High-level reasoning for your sequence design. Briefly explain: (1) why you chose these postures for this practitioner, (2) how you addressed their profile/conditions and safety laws, (3) how the sequence meets the requested constraints (duration, focus, intensity), and (4) the logic behind the flow order.
- name: a short, descriptive sequence name (e.g. "Morning Wake-Up", "Hip Release Flow")
- posture_ids: ordered list of client_ids in the sequence (e.g. ["p_mountain", "p_upward_salute", "p_forward_fold", ...])
"""
