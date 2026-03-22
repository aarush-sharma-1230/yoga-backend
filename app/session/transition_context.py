"""
Transition context: builds pre-computed context for transition prompts.

All data fetching and formatting is done here. Prompt builders receive
pre-computed values only—no function calls inside prompts.
"""

from dataclasses import dataclass


def _format_sensory_cues(sensory_cues: list[dict]) -> str:
    """Format sensory cues from posture doc for prompt context."""
    if not sensory_cues:
        return "None provided."
    lines = []
    for sc in sensory_cues:
        area = sc.get("area", "")
        cue = sc.get("cue", "")
        lines.append(f"- {area}: {cue}")
    return "\n".join(lines)


def _entry_transition_names(entry_transitions: list) -> list[str]:
    """Extract names from entry_transitions (objects or legacy client_id strings)."""
    names = []
    for e in entry_transitions or []:
        if isinstance(e, dict):
            names.append(e.get("name", "?"))
        else:
            names.append(str(e))
    return names


@dataclass
class TransitionContext:
    """
    Pre-computed context for a single transition prompt.
    Built by the session service; consumed by the prompt template.
    """

    is_initial: bool
    full_sequence: str
    from_posture_name: str | None
    to_posture_name: str
    entry_transition_names: list[str]
    has_entry_transitions: bool
    recommended_modification: str
    sensory_cues_formatted: str


def build_transition_context(
    transition_from_idx: int,
    postures: list,
    sensory_cues_map: dict[str, list[dict]],
) -> TransitionContext:
    """
    Build fully resolved context for a transition prompt.
    Call from session service before passing to get_transition_prompt.
    """
    postures_context = ", ".join([p.get("name", "?") for p in postures])
    is_initial = transition_from_idx == -1

    if is_initial:
        to_posture = postures[0]
        from_posture_name = None
    else:
        from_posture = postures[transition_from_idx]
        to_posture = postures[transition_from_idx + 1]
        from_posture_name = from_posture.get("name", "?")

    to_posture_name = to_posture.get("name", "?")
    entry_transitions = to_posture.get("entry_transitions") or []
    entry_transition_names = _entry_transition_names(entry_transitions)
    has_entry_transitions = len(entry_transition_names) > 0
    recommended_mod = to_posture.get("recommended_modification") or ""
    sensory_cues = sensory_cues_map.get(to_posture.get("client_id", ""), [])
    sensory_cues_formatted = _format_sensory_cues(sensory_cues)

    return TransitionContext(
        is_initial=is_initial,
        full_sequence=postures_context,
        from_posture_name=from_posture_name,
        to_posture_name=to_posture_name,
        entry_transition_names=entry_transition_names,
        has_entry_transitions=has_entry_transitions,
        recommended_modification=recommended_mod or "None",
        sensory_cues_formatted=sensory_cues_formatted,
    )
