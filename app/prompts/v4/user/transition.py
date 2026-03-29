"""v4 user prompt: transition guidance as composable sections over TransitionRequestContext."""

from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_VINYASA_LOOP,
)
from app.session.transition_request import TransitionRequestContext


def _section_core_task() -> str:
    return """## YOUR TASK
You are writing a **spoken audio script** for a yoga session. The practitioner will hear your words as continuous guidance—clear, calm, and natural, as in a live class.
When **transitional hubs** are listed before `<target_block>`, you must script movement **through them in order** (transition one, two, …) and then arrive at the **final** posture or block described in `<target_block>`.
"""


def _section_output_schema(expected_step_count: int) -> str:
    """Describe the exact JSON shape and step count."""
    return f"""## OUTPUT (JSON ONLY — ARRAY OF STEPS)
Return **only** a valid JSON object of this form (no markdown fences, no text before or after):

{{
  "steps": [
    {{
      "instruction": "string — the spoken line(s) for this step: movement, pose names, alignment, timing as needed",
      "sensory_cue": "string or null — breath / body awareness; use null when not needed for this step"
    }}
  ]
}}

* `steps` is an **array** of objects. Each object has **exactly** these two keys: `instruction`, `sensory_cue`.
* You **MUST** include exactly **{expected_step_count}** element(s) in `steps`, in playback order. Each element becomes one audio segment."""


def _section_session_state(ctx: TransitionRequestContext) -> str:
    note = (
        "(Each line lists its posture type: static_hold, transitional_hub, interval_set, or vinyasa_loop; "
        "interval and vinyasa rows are spelled out, not a single slot name.)"
    )
    if ctx.is_initial:
        return f"""<SESSION_STATE>
<full_sequence_context>
{ctx.full_sequence}
</full_sequence_context>
{note}

<target_block>{ctx.to_posture_name}</target_block>
</SESSION_STATE>"""

    return f"""<SESSION_STATE>
<full_sequence_context>
{ctx.full_sequence}
</full_sequence_context>
{note}

<current_posture>{ctx.from_posture_name}</current_posture>
<target_block>{ctx.to_posture_name}</target_block>
</SESSION_STATE>"""


def _section_preceding_transitional_hubs(ctx: TransitionRequestContext) -> str | None:
    names = ctx.preceding_transitional_hub_names
    if not names:
        return None
    numbered = "\n".join(f"{i + 1}. {name}" for i, name in enumerate(names))
    return f"""<TRANSITIONAL_HUBS>
Before reaching `<target_block>`, the practitioner must move **in order** through these transitional hubs:
{numbered}
Script the **instruction** so they pass hub 1, then hub 2, then … with clear spoken cues (you may say “transition one”, “transition two”, or name the postures naturally).
</TRANSITIONAL_HUBS>"""


def _section_static_resources(ctx: TransitionRequestContext) -> str:
    parts = [_section_preceding_transitional_hubs(ctx)]
    parts.append(
        f"""<TARGET_RESOURCES>
<recommended_modifications>{ctx.recommended_modification}</recommended_modifications>
<sensory_cues_for_hold>{ctx.sensory_cues_formatted}</sensory_cues_for_hold>
</TARGET_RESOURCES>"""
    )
    return "\n\n".join(p for p in parts if p)


def _section_static_objective_initial(ctx: TransitionRequestContext) -> str:
    hub_extra = ""
    if ctx.preceding_transitional_hub_names:
        hub_extra = (
            " The **single** `instruction` must move through every listed transitional hub in order, then complete the arrival into the hold in `<target_block>`."
        )
    return f"""## OBJECTIVE (FIRST MAIN POSTURE)
Guide the practitioner from the opening centering phase into `<target_block>`.
* Welcome them back, invite them to open the eyes when ready.{hub_extra}
* Weave `<recommended_modifications>` naturally into alignment language.
* Return **one** object in `steps`: `instruction` = full spoken path{"" if not ctx.preceding_transitional_hub_names else " (hubs + final hold)"}; `sensory_cue` = awareness for **holding** the final posture in `<target_block>`, using `<sensory_cues_for_hold>`."""


def _section_static_objective_transition(ctx: TransitionRequestContext) -> str:
    hub_extra = ""
    if ctx.preceding_transitional_hub_names:
        hub_extra = " The **single** `instruction` must pass through each transitional hub in order, then settle into the hold in `<target_block>`."
    return f"""## OBJECTIVE (STATIC HOLD)
From the posture in `<current_posture>` (or the opening phase if not applicable) into the hold in `<target_block>`.{hub_extra}
* Weave `<recommended_modifications>` into alignment.
* Return **one** object in `steps`: `instruction` = full arrival; `sensory_cue` = awareness for the **final hold** from `<sensory_cues_for_hold>`."""


def _section_interval_resources(ctx: TransitionRequestContext) -> str:
    parts = [_section_preceding_transitional_hubs(ctx)]
    parts.append(
        f"""<TIMED_FLOW>
{ctx.timed_flow_outline}
</TIMED_FLOW>"""
    )
    return "\n\n".join(p for p in parts if p)


def _section_interval_objective(ctx: TransitionRequestContext) -> str:
    rounds = ctx.expected_step_count // 2 if ctx.expected_step_count else 0
    hub_first = ""
    if ctx.preceding_transitional_hub_names:
        hub_first = """
When transitional hubs are listed above, the **first** object in `steps` must do **both** in one `instruction`: (1) guide through every hub in order into `<target_block>`, and (2) immediately begin **round 1, WORK** as defined on the first line of `<TIMED_FLOW>` (same step — one audio beat). Its `sensory_cue` may be null or brief.

The **remaining** `steps` follow `<TIMED_FLOW>` in order for the rest of the work/recovery pairs (step 2 onward in the timed flow corresponds to `steps[1]`, etc.). Do **not** repeat the hub travel after `steps[0]`.
"""
    return f"""## OBJECTIVE (INTERVAL SET)
There are {rounds} work/recovery round(s). The session expects **{ctx.expected_step_count}** objects in `steps`.{hub_first}
If there are **no** transitional hubs, each step matches `<TIMED_FLOW>` in order: for each round, **WORK** then **RECOVERY**.

Each object's `instruction` is the spoken script for that step (posture name and timing); `sensory_cue` may be null or a short awareness line when it helps (except as noted above for the first step when hubs are present)."""


def _section_vinyasa_resources(ctx: TransitionRequestContext) -> str:
    parts = [_section_preceding_transitional_hubs(ctx)]
    parts.append(
        f"""<TIMED_FLOW>
{ctx.timed_flow_outline}
</TIMED_FLOW>"""
    )
    return "\n\n".join(p for p in parts if p)


def _section_vinyasa_objective(ctx: TransitionRequestContext) -> str:
    hub_first = ""
    if ctx.preceding_transitional_hub_names:
        hub_first = """
When transitional hubs are listed above, the **first** object in `steps` must do **both** in one `instruction`: (1) guide through every hub in order into `<target_block>`, and (2) immediately perform the **first** posture named on line 1 of `<TIMED_FLOW>` (start of round 1 of the vinyasa cycle — one audio beat). Its `sensory_cue` may be null or brief.

The **remaining** `steps` follow `<TIMED_FLOW>` in order (line 2 → `steps[1]`, etc.). Do **not** repeat the hub travel after `steps[0]`.
"""
    return f"""## OBJECTIVE (VINYASA LOOP)
Produce exactly **{ctx.expected_step_count}** objects in `steps`, aligned with `<TIMED_FLOW>` overall.{hub_first}
If there are **no** transitional hubs, each step is one line of `<TIMED_FLOW>` in order.

Each `instruction` covers movement and alignment for that step; `sensory_cue` is null or a brief cue when useful."""


def get_transition_prompt(ctx: TransitionRequestContext) -> str:
    """
    Build the transition user prompt from session-built context.
    Composes sections by `target_posture_intent`. Transitional hubs are never the target row;
    they appear only in `preceding_transitional_hub_names` for the next real posture.
    """
    intent = ctx.target_posture_intent
    parts: list[str] = [_section_core_task(), _section_session_state(ctx)]

    if intent == POSTURE_INTENT_STATIC_HOLD:
        parts.append(_section_static_resources(ctx))
        parts.append(_section_static_objective_initial(ctx) if ctx.is_initial else _section_static_objective_transition(ctx))
    elif intent == POSTURE_INTENT_INTERVAL_SET:
        parts.append(_section_interval_resources(ctx))
        parts.append(_section_interval_objective(ctx))
    elif intent == POSTURE_INTENT_VINYASA_LOOP:
        parts.append(_section_vinyasa_resources(ctx))
        parts.append(_section_vinyasa_objective(ctx))
    else:
        parts.append(_section_static_resources(ctx))
        parts.append(_section_static_objective_transition(ctx))

    parts.append(_section_output_schema(ctx.expected_step_count))
    return "\n\n".join(parts)
