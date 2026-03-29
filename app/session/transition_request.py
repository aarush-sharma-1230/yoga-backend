"""
Session-built DTO for transition generation: raw posture data and prompt-facing strings.
YogaCoordinator consumes this; no LLM schema selection here.
"""

from dataclasses import dataclass

from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_TRANSITIONAL_HUB,
    POSTURE_INTENT_VINYASA_LOOP,
)


def _default_intent(p: dict) -> str:
    return p.get("posture_intent") or POSTURE_INTENT_STATIC_HOLD


def _format_sensory_cues(sensory_cues: list[dict]) -> str:
    if not sensory_cues:
        return "None provided."
    return "\n".join(f"- {sc.get('area', '')}: {sc.get('cue', '')}" for sc in sensory_cues)


def _entry_transitions_for_static_target(postures: list, target_idx: int) -> list[str]:
    if target_idx <= 0:
        return []
    to_posture = postures[target_idx]
    if _default_intent(to_posture) != POSTURE_INTENT_STATIC_HOLD:
        return []
    result = []
    for j in range(target_idx - 1, -1, -1):
        if _default_intent(postures[j]) == POSTURE_INTENT_TRANSITIONAL_HUB:
            result.insert(0, postures[j].get("name", "?"))
        else:
            break
    return result


def should_skip_transition_for_index(postures: list, target_idx: int) -> bool:
    """Skip LLM when this hub row is continued from the previous hub (one call covers the run)."""
    if target_idx < 0 or target_idx >= len(postures):
        return True
    if _default_intent(postures[target_idx]) != POSTURE_INTENT_TRANSITIONAL_HUB:
        return False
    if target_idx > 0 and _default_intent(postures[target_idx - 1]) == POSTURE_INTENT_TRANSITIONAL_HUB:
        return True
    return False


def _collect_hub_chain_names(postures: list, start_idx: int) -> list[str]:
    names: list[str] = []
    j = start_idx
    n = len(postures)
    while j < n and _default_intent(postures[j]) == POSTURE_INTENT_TRANSITIONAL_HUB:
        names.append(postures[j].get("name", "?"))
        j += 1
    return names


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


def _hub_block_label(chain: list[str], dest: str | None) -> str:
    arrow = " → ".join(chain)
    if dest:
        return f"{arrow} → {dest}"
    return arrow


def _primary_client_id_for_destination_sensory(row: dict | None) -> str | None:
    if not row:
        return None
    intent = _default_intent(row)
    if intent == POSTURE_INTENT_INTERVAL_SET:
        return (row.get("work_posture") or {}).get("client_id")
    if intent == POSTURE_INTENT_VINYASA_LOOP:
        cyc = row.get("cycle_postures") or []
        if cyc:
            return cyc[0].get("client_id")
        return None
    return row.get("client_id")


def _destination_mod_summary(row: dict | None) -> str:
    if not row:
        return "None"
    intent = _default_intent(row)
    if intent == POSTURE_INTENT_INTERVAL_SET:
        return (row.get("work_posture") or {}).get("recommended_modification") or "None"
    if intent == POSTURE_INTENT_VINYASA_LOOP:
        cyc = row.get("cycle_postures") or []
        if cyc:
            return cyc[0].get("recommended_modification") or "None"
        return "None"
    return row.get("recommended_modification") or "None"


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
    entry_transition_names: list[str]
    recommended_modification: str
    sensory_cues_formatted: str
    hub_chain_names: list[str]
    destination_hold_summary: str | None
    destination_recommended_modification: str
    destination_sensory_cues_formatted: str
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
    is_initial = target_idx == 0
    from_posture_name = (
        None
        if is_initial
        else _row_display_name(postures[target_idx - 1]) or postures[target_idx - 1].get("name", "?")
    )
    full_sequence = _format_full_sequence_context(postures)

    hub_chain_names: list[str] = []
    destination_hold_summary: str | None = None
    destination_recommended_modification = "None"
    destination_sensory_cues_formatted = "None provided."
    timed_flow_outline = ""
    expected_step_count = 0

    entry_transition_names: list[str] = []
    if intent == POSTURE_INTENT_STATIC_HOLD:
        entry_transition_names = _entry_transitions_for_static_target(postures, target_idx)
        expected_step_count = 1
    elif intent == POSTURE_INTENT_TRANSITIONAL_HUB:
        hub_chain_names = _collect_hub_chain_names(postures, target_idx)
        j = target_idx + len(hub_chain_names)
        following = postures[j] if j < len(postures) else None
        destination_hold_summary = _row_display_name(following)
        destination_recommended_modification = _destination_mod_summary(following)
        dest_cid = _primary_client_id_for_destination_sensory(following)
        destination_sensory_cues_formatted = _format_sensory_cues(sensory_cues_map.get(dest_cid or "", []))
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

    if intent == POSTURE_INTENT_TRANSITIONAL_HUB:
        to_posture_name = _hub_block_label(hub_chain_names, destination_hold_summary)
        recommended_modification = "None"
    else:
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
        entry_transition_names=entry_transition_names,
        recommended_modification=recommended_modification,
        sensory_cues_formatted=sensory_cues_formatted,
        hub_chain_names=hub_chain_names,
        destination_hold_summary=destination_hold_summary,
        destination_recommended_modification=destination_recommended_modification,
        destination_sensory_cues_formatted=destination_sensory_cues_formatted,
        timed_flow_outline=timed_flow_outline,
        expected_step_count=expected_step_count,
    )
