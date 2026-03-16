def get_yoga_laws_context(profile_data: dict) -> str:
    """
    Generates a targeted 'Laws' string based on the user's 
    actual medical conditions and pain areas.
    """
    laws = ["MANDATORY MODIFICATION LAWS"]
    
    meds = profile_data.get('medical_conditions', [])
    pain = profile_data.get('chronic_pain_areas', [])
    
    # Logic for Inversions
    if any(m in ['hypertension', 'glaucoma', 'heart_condition'] for m in meds):
        laws.append("- LAW OF INVERSIONS: Strictly forbid head-below-heart poses. Substitute with head-elevated variations.")
    
    # Logic for Spine
    if 'herniated_disc' in meds or 'osteoporosis' in meds or 'lower_back' in pain:
        laws.append("- LAW OF THE SPINE: Forbid spinal flexion (rounding). Require neutral spine and micro-bent knees.")
        
    # Logic for Balance/Vestibular
    if 'vertigo' in meds or 'epilepsy' in meds:
        laws.append("- LAW OF VESTIBULAR SAFETY: Slow down transitions by 2x. Add stabilization pauses between floor and standing.")
        
    # Logic for Weight-Bearing
    if any(p in ['wrists', 'shoulders', 'ankles'] for p in pain):
        laws.append("- LAW OF WEIGHT-BEARING: Offer forearm/fist alternatives. Avoid long holds on affected joints.")
        
    # Logic for Joint Flexion/Pregnancy
    if any(p in ['knees', 'hips'] for p in pain) or 'pregnancy' in meds:
        laws.append("- LAW OF JOINT FLEXION: Forbid deep compression. Always suggest props (blocks/blankets). Avoid prone poses if pregnant.")

    return "\n".join(laws)