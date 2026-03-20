"""
Convert user's vague intensity preference (Mild, Balanced, Intense) into a
simple instruction for sequence generation.

Only specifies how many hard postures (overall_exertion 4–5) to include.
Total length, mix of medium/easy, and flow are left to the LLM.
"""

from typing import Optional


def get_intensity_instruction(
    intensity_level: str,
    duration_minutes: Optional[int] = None,
) -> str:
    """
    Return a single instruction about hard postures. Duration is passed through
    separately; we only constrain the number of hard postures here.

    Args:
        intensity_level: "mild" | "balanced" | "intense" (case-insensitive)
        duration_minutes: Unused; kept for API compatibility.

    Returns:
        A one-line instruction for the LLM.
    """
    level = (intensity_level or "").strip().lower()
    if level not in ("mild", "balanced", "intense"):
        level = "balanced"

    if level == "mild":
        return "Include 0 hard postures (overall_exertion 4–5). Use only light to moderate postures. Decide total length and flow based on duration."
    if level == "balanced":
        return "Include 1–2 hard postures (overall_exertion 4–5). Decide the rest of the sequence (total length, medium/easy mix, flow) based on duration and smooth transitions."
    # intense
    return "Include 2–4 hard postures (overall_exertion 4–5). Decide the rest of the sequence (total length, medium/easy mix, flow) based on duration and smooth transitions."
