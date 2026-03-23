"""Rule-based modification laws derived from user's medical conditions and chronic pain areas."""


def get_yoga_laws_context(profile_data: dict) -> str:
    """
    Generates a targeted 'Laws' string based on the user's medical conditions and pain areas.
    Expects profile_data to be hard_priority_strategy dict with: medical_conditions, chronic_pain_areas, recent_surgery.
    Returns empty string if no constraints apply.
    """
    meds = profile_data.get("medical_conditions") or []
    pain = profile_data.get("chronic_pain_areas") or []
    recent_surgery = profile_data.get("recent_surgery") is True

    laws: list[str] = []

    # Inversions: contraindicated for hypertension, glaucoma, heart conditions
    if any(m in ("hypertension", "glaucoma", "heart_condition") for m in meds):
        laws.append("- LAW OF INVERSIONS: Strictly forbid head-below-heart poses. Substitute with head-elevated variations.")

    # Spine: herniated disc, osteoporosis, lower back pain
    if "herniated_disc" in meds or "osteoporosis" in meds or "lower_back" in pain:
        laws.append("- LAW OF THE SPINE: Forbid spinal flexion (rounding). Require neutral spine and micro-bent knees.")

    # Vestibular: vertigo (removed epilepsy - not in schema)
    if "vertigo" in meds:
        laws.append("- LAW OF VESTIBULAR SAFETY: Slow down transitions by 2x. Add stabilization pauses between floor and standing.")

    # Weight-bearing: wrists, shoulders, ankles
    if any(p in ("wrists", "shoulders", "ankles") for p in pain):
        laws.append("- LAW OF WEIGHT-BEARING: Offer forearm/fist alternatives. Avoid long holds on affected joints.")

    # Knee pain: deep flexion, compression
    if "knees" in pain:
        laws.append("- LAW OF KNEE SAFETY: Avoid deep knee flexion. Suggest blocks under knees in poses. Micro-bend when needed.")

    # Neck: careful with head movements, inversions
    if "neck" in pain:
        laws.append("- LAW OF NECK SAFETY: Avoid sudden head drops. Keep cervical spine neutral. No shoulder stand or plow.")

    # Pregnancy: no prone, no deep compression, no inversions
    if "pregnancy" in meds:
        laws.append("- LAW OF PREGNANCY: Avoid prone poses and deep compression. Suggest props. No inversions.")

    # Recent surgery: conservative approach
    if recent_surgery:
        laws.append("- LAW OF RECOVERY: Proceed conservatively. Avoid strenuous transitions. Prioritize gentle, supported poses.")

    if not laws:
        return ""

    return "MANDATORY MODIFICATION LAWS\n" + "\n".join(laws)
