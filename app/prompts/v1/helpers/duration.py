"""Duration-to-posture helpers for sequence generation."""


def duration_to_posture_count(duration_minutes: int) -> int:
    """
    Convert session duration (minutes) to approximate posture count.

    Uses ~2.5 minutes per posture on average (including transitions).
    Minimum 5 postures for very short sessions.
    """
    count = round(duration_minutes / 2.5)
    return max(5, count)


def posture_count_range(posture_count: int) -> tuple[int, int]:
    """Return (min, max) for a flexible posture count range (±2, min 5)."""
    lo = max(5, posture_count - 2)
    hi = posture_count + 2
    return (lo, hi)


def duration_to_posture_range(duration_minutes: int) -> tuple[int, int]:
    """
    Convert session duration to posture count range (lo, hi).

    Single call for the agent: duration → (posture_range_lo, posture_range_hi).
    """
    posture_count = duration_to_posture_count(duration_minutes)
    return posture_count_range(posture_count)
