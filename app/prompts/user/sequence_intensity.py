"""
Convert user's vague intensity preference (Mild, Balanced, Intense) into a
deterministic specification for sequence generation.

Uses duration and intensity level to produce concrete targets for how many
postures at each exertion band (1-2 low, 3 mid, 4-5 high) should appear.
These targets are passed to the LLM to guide posture selection.
"""

from dataclasses import dataclass
from typing import Literal, Optional


IntensityLevel = Literal["mild", "balanced", "intense"]


@dataclass
class IntensitySpec:
    """Deterministic spec derived from user's intensity preference and duration."""

    total_postures_min: int
    total_postures_max: int
    high_exertion_min: int  # 4-5 on overall_exertion
    high_exertion_max: int
    mid_exertion_min: int  # 3 on overall_exertion
    mid_exertion_max: int
    low_exertion_min: int  # 1-2 on overall_exertion
    low_exertion_max: int

    def to_prompt_text(self) -> str:
        """Format the spec as instructions for the LLM."""
        lines = [
            f"- Total postures: {self.total_postures_min}–{self.total_postures_max}.",
            f"- High exertion (overall_exertion 4–5): {self.high_exertion_min}–{self.high_exertion_max} postures.",
            f"- Mid exertion (overall_exertion 3): {self.mid_exertion_min}–{self.mid_exertion_max} postures.",
            f"- Low exertion (overall_exertion 1–2): {self.low_exertion_min}–{self.low_exertion_max} postures.",
        ]
        return "\n".join(lines)


def _posture_count_range(duration_minutes: Optional[int]) -> tuple[int, int]:
    """Map duration to min–max posture count. ~2–3 postures per 10 minutes."""
    if duration_minutes is None:
        return 6, 10
    if duration_minutes <= 15:
        return 4, 6
    if duration_minutes <= 25:
        return 5, 8
    if duration_minutes <= 35:
        return 6, 9
    if duration_minutes <= 45:
        return 8, 10
    return 10, 12


def get_intensity_spec(
    intensity_level: str,
    duration_minutes: Optional[int] = None,
) -> IntensitySpec:
    """
    Convert user's intensity preference and duration into a deterministic spec.

    Args:
        intensity_level: "mild" | "balanced" | "intense" (case-insensitive)
        duration_minutes: Session length; affects total posture count.

    Returns:
        IntensitySpec with ranges for total postures and exertion distribution.
    """
    level = (intensity_level or "").strip().lower()
    if level not in ("mild", "balanced", "intense"):
        level = "balanced"
    total_min, total_max = _posture_count_range(duration_minutes)
    mid = (total_min + total_max) // 2

    if level == "mild":
        return IntensitySpec(
            total_postures_min=total_min,
            total_postures_max=total_max,
            high_exertion_min=0,
            high_exertion_max=0,
            mid_exertion_min=0,
            mid_exertion_max=min(1, mid),
            low_exertion_min=max(0, total_min - 1),
            low_exertion_max=total_max,
        )

    if level == "balanced":
        return IntensitySpec(
            total_postures_min=total_min,
            total_postures_max=total_max,
            high_exertion_min=1,
            high_exertion_max=min(2, mid),
            mid_exertion_min=max(1, mid // 2),
            mid_exertion_max=min(4, mid),
            low_exertion_min=max(1, total_min - 3),
            low_exertion_max=max(2, total_max - 2),
        )

    # intense
    return IntensitySpec(
        total_postures_min=total_min,
        total_postures_max=total_max,
        high_exertion_min=min(2, mid),
        high_exertion_max=min(4, mid),
        mid_exertion_min=max(1, mid // 2),
        mid_exertion_max=min(4, mid),
        low_exertion_min=1,
        low_exertion_max=min(3, total_max // 2),
    )
