"""v4 user prompt: transition guidance as composable sections over TransitionRequestContext."""

from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_TRANSITIONAL_HUB,
    POSTURE_INTENT_VINYASA_LOOP,
)
from app.session.transition_request import TransitionRequestContext


def _section_core_task() -> str:
    return """## YOUR TASK
You are writing a **spoken audio script** for a yoga session. The practitioner will hear your words as continuous guidance—clear, calm, and natural, as in a live class.
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
    if ctx.is_initial:
        return f"""<SESSION_STATE>
<full_sequence_context>
{ctx.full_sequence}
</full_sequence_context>

<target_block>{ctx.to_posture_name}</target_block>
</SESSION_STATE>"""

    else:
        return f"""<SESSION_STATE>
<full_sequence_context>
{ctx.full_sequence}
</full_sequence_context>

<current_posture>{ctx.from_posture_name}</current_posture>
<target_block>{ctx.to_posture_name}</target_block>
</SESSION_STATE>"""


def _section_static_resources(ctx: TransitionRequestContext) -> str:
    hub_list = ", ".join(ctx.entry_transition_names) if ctx.entry_transition_names else "None"
    return f"""<TARGET_RESOURCES>
<transitional_hubs>Transitional hub postures to pass through (in order) before the main hold: {hub_list}</transitional_hubs>
<recommended_modifications>{ctx.recommended_modification}</recommended_modifications>
<sensory_cues_for_hold>{ctx.sensory_cues_formatted}</sensory_cues_for_hold>
</TARGET_RESOURCES>"""


def _section_static_objective_initial(ctx: TransitionRequestContext) -> str:
    return """## OBJECTIVE (FIRST POSTURE)
Guide the practitioner from the opening centering phase into the first hold in `<target_block>`.
* Welcome them back, invite them to open the eyes when ready, then move through any **transitional hubs** (if listed) briefly on the way into the posture.
* Weave `<recommended_modifications>` naturally into alignment language.
* Return **one** object in `steps`: `instruction` = full spoken arrival; `sensory_cue` = awareness for **holding** the final posture, using `<sensory_cues_for_hold>`."""


def _section_static_objective_transition(ctx: TransitionRequestContext) -> str:
    return """## OBJECTIVE (STATIC HOLD)
From `<current_posture>` into the hold described in `<target_block>`.
* If **transitional hubs** are listed, fold brief travel through them in order into the single `instruction`.
* Weave `<recommended_modifications>` into alignment.
* Return **one** object in `steps`: `instruction` = full arrival; `sensory_cue` = awareness for the **final hold** from `<sensory_cues_for_hold>`."""


def _section_hub_resources(ctx: TransitionRequestContext) -> str:
    dest_mod = ctx.destination_recommended_modification
    chain = ctx.hub_chain_names
    numbered = "\n".join(f"{i + 1}. {name}" for i, name in enumerate(chain)) if chain else "None"
    return f"""<TARGET_RESOURCES>
<transitional_hubs_list>
Ordered transitional hubs (you will script movement through each, then into the target):
{numbered}
</transitional_hubs_list>
<target_posture_after_hubs>{ctx.destination_hold_summary or "Unknown"}</target_posture_after_hubs>
<target_modifications>{dest_mod}</target_modifications>
<sensory_cues_for_target_posture>{ctx.destination_sensory_cues_formatted}</sensory_cues_for_target_posture>
</TARGET_RESOURCES>"""


def _section_hub_objective(ctx: TransitionRequestContext) -> str:
    n = len(ctx.hub_chain_names)
    steps_enum = ", ".join(f"transitional hub {i + 1}" for i in range(n)) if n else "no hubs"
    if ctx.is_initial:
        opening = """The practitioner is finishing the opening centering phase (eyes may still be closed). """
    else:
        opening = "The practitioner is currently in `<current_posture>`. "
    return f"""## OBJECTIVE (TRANSITIONAL HUBS → TARGET POSTURE)
{opening}You must produce **one combined spoken script** in a **single** `steps` entry (one object in the array).
* **instruction**: Guide them **in order** through {steps_enum}, then settle them into **<target_posture_after_hubs>** with clear alignment. Name each segment naturally (e.g. “transition one … transition two …”) so the path is obvious. If this is the very start of the sequence, welcome them out of centering and open the movement gradually. Apply **target_modifications** when describing the final posture.
* **sensory_cue**: Awareness for **holding** the **target posture only** (after all hubs), using `<sensory_cues_for_target_posture>`.

Return exactly **one** object in `steps`."""


def _section_interval_resources(ctx: TransitionRequestContext) -> str:
    return f"""<TIMED_FLOW>
{ctx.timed_flow_outline}
</TIMED_FLOW>"""


def _section_interval_objective(ctx: TransitionRequestContext) -> str:
    rounds = ctx.expected_step_count // 2 if ctx.expected_step_count else 0
    return f"""## OBJECTIVE (INTERVAL SET)
There are {rounds} work/recovery round(s). Produce **{ctx.expected_step_count}** objects in `steps`: for each round, first **WORK**, then **RECOVERY**, in order.
Each object's `instruction` is the spoken script for that step (posture name and timing); `sensory_cue` may be null or a short awareness line when it helps."""


def _section_vinyasa_resources(ctx: TransitionRequestContext) -> str:
    return f"""<TIMED_FLOW>
{ctx.timed_flow_outline}
</TIMED_FLOW>"""


def _section_vinyasa_objective(ctx: TransitionRequestContext) -> str:
    return f"""## OBJECTIVE (VINYASA LOOP)
Produce exactly **{ctx.expected_step_count}** objects in `steps`, in the same order as `<TIMED_FLOW>`: one step per line (each posture in the cycle, each round).
Each `instruction` covers movement and alignment for that step; `sensory_cue` is null or a brief cue when useful."""


def get_transition_prompt(ctx: TransitionRequestContext) -> str:
    """
    Build the transition user prompt from session-built context.
    Composes sections by `target_posture_intent`; no I/O.
    """
    intent = ctx.target_posture_intent
    parts: list[str] = [_section_core_task(), _section_session_state(ctx)]

    if intent == POSTURE_INTENT_STATIC_HOLD:
        parts.append(_section_static_resources(ctx))
        parts.append(_section_static_objective_initial(ctx) if ctx.is_initial else _section_static_objective_transition(ctx))
    elif intent == POSTURE_INTENT_TRANSITIONAL_HUB:
        parts.append(_section_hub_resources(ctx))
        parts.append(_section_hub_objective(ctx))
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
