"""
Convert user's intensity preference (Mild, Balanced, Intense) into a flexible
instruction for sequence generation. Scales with session duration.

Specifies approximate ranges for hard postures (overall_exertion 4–5).
A 15-minute session vs 1-hour session will have different hard posture counts
for the same intensity level.
"""


def get_intensity_instruction(intensity_level: str, duration_minutes: int) -> str:
    """
    Return a flexible instruction about hard postures. Uses approximate ranges
    that scale with duration so the LLM can prioritize smooth transitions.

    Args:
        intensity_level: "mild" | "balanced" | "intense" (case-insensitive)
        duration_minutes: Session duration; longer sessions allow more hard postures.

    Returns:
        A one-line instruction for the LLM.
    """
    level = (intensity_level or "").strip().lower()
    if level not in ("mild", "balanced", "intense"):
        level = "balanced"

    # Scale factor: 30 min = 1.0 (baseline)
    scale = duration_minutes / 30.0

    if level == "mild":
        return "Include 0 hard postures (overall_exertion 4–5). Use only light to moderate postures. Fill the rest with a mix that supports smooth flow."

    if level == "balanced":
        min_hard = max(0, round(0.5 * scale))
        max_hard = min(4, max(1, round(2 * scale)))
        if min_hard == max_hard:
            return f"Include roughly {min_hard} hard postures (overall_exertion 4–5). Fill the rest with a mix that supports smooth transitions."
        return f"Include roughly {min_hard}–{max_hard} hard postures (overall_exertion 4–5). Fill the rest with a mix that supports smooth transitions."

    # intense
    min_hard = max(1, round(1 * scale))
    max_hard = min(8, max(2, round(4 * scale)))
    if min_hard == max_hard:
        return f"Include roughly {min_hard} hard postures (overall_exertion 4–5). Fill the rest with a mix that supports smooth transitions."
    return f"Include roughly {min_hard}–{max_hard} hard postures (overall_exertion 4–5). Fill the rest with a mix that supports smooth transitions."
