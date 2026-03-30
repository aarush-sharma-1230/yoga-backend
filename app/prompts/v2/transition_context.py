"""
Legacy transition context for v2 transition prompts only.

Pre-computed context for a flat posture array (static_hold | transitional_hub).
"""

from dataclasses import dataclass

from app.schemas.custom_sequence import POSTURE_INTENT_TRANSITIONAL_HUB


def _format_sensory_cues(sensory_cues: list[dict]) -> str:
    """Format sensory cues from posture doc for prompt context."""
    if not sensory_cues:
        return "None provided."
    return "\n".join(f"- {sc.get('area', '')}: {sc.get('cue', '')}" for sc in sensory_cues)


def _entry_transitions_for_target(postures: list, target_idx: int) -> list[str]:
    """
    For a static_hold target: transitional_hub postures immediately before it.
    For transitional_hub target: empty (we pass through, nothing to pass through before).
    """
    if target_idx <= 0:
        return []
    to_posture = postures[target_idx]
    if to_posture.get("posture_intent") == POSTURE_INTENT_TRANSITIONAL_HUB:
        return []

    result = []
    for j in range(target_idx - 1, -1, -1):
        if postures[j].get("posture_intent") == POSTURE_INTENT_TRANSITIONAL_HUB:
            result.insert(0, postures[j].get("name", "?"))
        else:
            break
    return result


@dataclass
class TransitionContext:
    """Pre-computed context for a single transition prompt."""

    is_initial: bool
    full_sequence: str
    from_posture_name: str | None
    to_posture_name: str
    entry_transition_names: list[str]
    has_entry_transitions: bool
    recommended_modification: str
    sensory_cues_formatted: str


def build_transition_context(
    target_idx: int,
    postures: list,
    sensory_cues_map: dict[str, list[dict]],
) -> TransitionContext:
    """
    Build context for transitioning into the posture at target_idx.
    One transition per posture in the flat array.
    """
    to_posture = postures[target_idx]
    is_initial = target_idx == 0
    entry_transition_names = _entry_transitions_for_target(postures, target_idx)

    from_posture_name = None if is_initial else postures[target_idx - 1].get("name", "?")
    full_sequence = ", ".join(p.get("name", "?") for p in postures)

    return TransitionContext(
        is_initial=is_initial,
        full_sequence=full_sequence,
        from_posture_name=from_posture_name,
        to_posture_name=to_posture.get("name", "?"),
        entry_transition_names=entry_transition_names,
        has_entry_transitions=len(entry_transition_names) > 0,
        recommended_modification=to_posture.get("recommended_modification") or "None",
        sensory_cues_formatted=_format_sensory_cues(
            sensory_cues_map.get(to_posture.get("client_id", ""), [])
        ),
    )
