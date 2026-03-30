"""Format posture catalogue for inclusion in prompts (e.g. developer prompt)."""


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
    raw_name = posture.get("name")
    english = raw_name if isinstance(raw_name, str) and raw_name else "Unknown"
    sanskrit = posture.get("sanskrit_name") or ""
    aliases = posture.get("aliases") or []
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

    title = f"{client_id}: {english}"
    if sanskrit:
        title += f" ({sanskrit})"

    lines = [title]
    if aliases:
        lines.append(f"  aliases: {', '.join(str(a) for a in aliases)}")
    lines.extend(
        [
            f"  inverted: {'yes' if is_inverted else 'no'} | spinal_shape: {spinal_shape}",
            f"  {lat_str}",
            f"  {counter_str}",
            f"  {ip_str}",
        ]
    )

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


def format_posture_catalogue(postures: list) -> str:
    """Format the posture catalogue for inclusion in the developer prompt."""
    blocks = [_format_posture_entry(p) for p in postures]
    return "\n---\n".join(blocks)
