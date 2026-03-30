"""
Session entrypoint for building v4 transition request DTOs.

Implements `build_transition_request` in app.prompts.v4.transition_request; SessionService
imports from here so session orchestration keeps a stable module path.
"""

from dataclasses import dataclass

from app.schemas.custom_sequence import POSTURE_INTENT_INTERVAL_SET, POSTURE_INTENT_STATIC_HOLD, POSTURE_INTENT_TRANSITIONAL_HUB, POSTURE_INTENT_VINYASA_LOOP

def _default_intent(p: dict) -> str:
    return p.get("posture_intent") or POSTURE_INTENT_STATIC_HOLD


def should_skip_transition_for_index(postures: list, target_idx: int) -> bool:
    """Skip LLM for transitional_hub rows; they are folded into the next real posture's prompt."""
    if target_idx < 0 or target_idx >= len(postures):
        return True
    return _default_intent(postures[target_idx]) == POSTURE_INTENT_TRANSITIONAL_HUB

def _first_non_hub_index(postures: list) -> int | None:
    """Index of the first posture that is not a transitional hub (first guided block)."""
    for i, p in enumerate(postures):
        if _default_intent(p) != POSTURE_INTENT_TRANSITIONAL_HUB:
            return i
    return None

def _last_non_hub_index_before_target(postures: list, target_idx: int) -> int | None:
    """Last held / main row before target, skipping a trailing run of transitional hubs."""
    j = target_idx - 1
    while j >= 0:
        if _default_intent(postures[j]) != POSTURE_INTENT_TRANSITIONAL_HUB:
            return j
        j -= 1
    return None

def _row_display_name(p: dict | None) -> str | None:
    if not p:
        return None
    intent = _default_intent(p)
    if intent == POSTURE_INTENT_INTERVAL_SET:
        w = (p.get("work_posture") or {}).get("name", "?")
        r = (p.get("recovery_posture") or {}).get("name", "?")
        return f"Interval set ({w} / {r})"
    if intent == POSTURE_INTENT_VINYASA_LOOP:
        names = [x.get("name", "?") for x in (p.get("cycle_postures") or [])]
        return f"Vinyasa loop ({' → '.join(names)})"
    return p.get("name")

def _format_sequence_context_entry(index: int, p: dict) -> str:
    """One line in the full-sequence summary, typed for interval/vinyasa/static/hub."""
    intent = _default_intent(p)
    n = index + 1
    if intent == POSTURE_INTENT_INTERVAL_SET:
        wp = (p.get("work_posture") or {}).get("name", "?")
        rp = (p.get("recovery_posture") or {}).get("name", "?")
        r = p.get("rounds")
        h = p.get("hold_time_seconds")
        rest = p.get("rest_time_seconds")
        return (
            f"{n}. [interval_set] work: {wp} ({h}s) / recovery: {rp} ({rest}s) — {r} round(s)"
        )
    if intent == POSTURE_INTENT_VINYASA_LOOP:
        names = " → ".join((x.get("name", "?") for x in (p.get("cycle_postures") or [])))
        r = p.get("rounds")
        return f"{n}. [vinyasa_loop] cycle: {names} — {r} round(s)"
    if intent == POSTURE_INTENT_TRANSITIONAL_HUB:
        return f"{n}. [transitional_hub] {p.get('name', '?')}"
    hold = p.get("hold_time_seconds")
    hold_part = f", hold {hold}s" if hold is not None else ""
    return f"{n}. [static_hold] {p.get('name', '?')}{hold_part}"

def _format_full_sequence_context(postures: list) -> str:
    """Human-readable sequence outline; interval and vinyasa rows are expanded, not a single name."""
    return "\n".join(_format_sequence_context_entry(i, p) for i, p in enumerate(postures))

def _preceding_transitional_hub_names(postures: list, target_idx: int) -> list[str]:
    """Consecutive transitional hubs immediately before target_idx (in order)."""
    if target_idx <= 0:
        return []
    result: list[str] = []
    for j in range(target_idx - 1, -1, -1):
        if _default_intent(postures[j]) == POSTURE_INTENT_TRANSITIONAL_HUB:
            result.insert(0, postures[j].get("name", "?"))
        else:
            break
    return result

def _format_sensory_cues(sensory_cues: list[dict]) -> str:
    if not sensory_cues:
        return "None provided."
    return "\n".join(f"- {sc.get('area', '')}: {sc.get('cue', '')}" for sc in sensory_cues)

def _format_interval_outline(p: dict) -> str:
    work = p.get("work_posture") or {}
    rec = p.get("recovery_posture") or {}
    rounds = int(p.get("rounds") or 0)
    wsec = p.get("hold_time_seconds")
    rsec = p.get("rest_time_seconds")
    lines: list[str] = []
    step = 1
    for r in range(rounds):
        lines.append(f"Step {step}: WORK — {work.get('name', '?')} — {wsec}s")
        step += 1
        lines.append(f"Step {step}: RECOVERY — {rec.get('name', '?')} — {rsec}s")
        step += 1
    return "\n".join(lines) if lines else ""

def _format_vinyasa_outline(p: dict) -> str:
    rounds = int(p.get("rounds") or 0)
    cyc = p.get("cycle_postures") or []
    lines: list[str] = []
    step = 1
    for r in range(rounds):
        for pose in cyc:
            lines.append(f"Step {step}: {pose.get('name', '?')} — round {r + 1} of {rounds}")
            step += 1
    return "\n".join(lines) if lines else ""





@dataclass
class TransitionRequestContext:
    """Data-only context for the YogaCoordinator to build transition prompts."""

    target_idx: int
    is_initial: bool
    full_sequence: str
    from_posture_name: str | None
    target_posture_intent: str
    to_posture_name: str
    preceding_transitional_hub_names: list[str]
    recommended_modification: str
    sensory_cues_formatted: str
    timed_flow_outline: str
    expected_step_count: int


def build_transition_request(
    target_idx: int,
    postures: list,
    sensory_cues_map: dict[str, list[dict]],
) -> TransitionRequestContext | None:
    if should_skip_transition_for_index(postures, target_idx):
        return None

    to_posture = postures[target_idx]
    intent = _default_intent(to_posture)
    first_real_idx = _first_non_hub_index(postures)
    is_initial = first_real_idx is not None and target_idx == first_real_idx

    prev_hold_idx = _last_non_hub_index_before_target(postures, target_idx)
    if is_initial:
        from_posture_name = None
    elif prev_hold_idx is not None:
        from_posture_name = _row_display_name(postures[prev_hold_idx]) or postures[prev_hold_idx].get("name", "?")
    else:
        from_posture_name = None

    full_sequence = _format_full_sequence_context(postures)
    preceding_transitional_hub_names = _preceding_transitional_hub_names(postures, target_idx)

    timed_flow_outline = ""
    expected_step_count = 0

    if intent == POSTURE_INTENT_STATIC_HOLD:
        expected_step_count = 1
    elif intent == POSTURE_INTENT_INTERVAL_SET:
        timed_flow_outline = _format_interval_outline(to_posture)
        r = int(to_posture.get("rounds") or 0)
        expected_step_count = 2 * r
    elif intent == POSTURE_INTENT_VINYASA_LOOP:
        timed_flow_outline = _format_vinyasa_outline(to_posture)
        r = int(to_posture.get("rounds") or 0)
        cyc = to_posture.get("cycle_postures") or []
        expected_step_count = r * len(cyc)

    to_posture_name = _row_display_name(to_posture) or to_posture.get("name", "?")
    recommended_modification = to_posture.get("recommended_modification") or "None"

    target_cid = to_posture.get("client_id") if intent == POSTURE_INTENT_STATIC_HOLD else None
    if intent == POSTURE_INTENT_STATIC_HOLD:
        sensory_cues_formatted = _format_sensory_cues(sensory_cues_map.get(target_cid or "", []))
    else:
        sensory_cues_formatted = "None provided."

    return TransitionRequestContext(
        target_idx=target_idx,
        is_initial=is_initial,
        full_sequence=full_sequence,
        from_posture_name=from_posture_name,
        target_posture_intent=intent,
        to_posture_name=to_posture_name or "?",
        preceding_transitional_hub_names=preceding_transitional_hub_names,
        recommended_modification=recommended_modification,
        sensory_cues_formatted=sensory_cues_formatted,
        timed_flow_outline=timed_flow_outline,
        expected_step_count=expected_step_count,
    )
