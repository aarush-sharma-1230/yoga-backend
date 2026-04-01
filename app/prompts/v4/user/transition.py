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

def _section_speech_cadence() -> str:
    return """
<VOICE_CADENCE_GUIDE>
* **Micro-Pause (`...`):** Insert for 1-second breaths (e.g., "Inhale... reaching up...")
* **Phase Break (`\n\n`):** Insert between movement and alignment (e.g., "Step forward. \n\n Keep the knee over the ankle.")
* **Softeners:** Use "just," "gently," and "maybe" to reduce "command fatigue."
* **Discourse Markers:** Use "alright," "now," and "there we go" to sound human.
</VOICE_CADENCE_GUIDE>
"""


def _section_output_schema(expected_step_count: int) -> str:
    """Describe the exact JSON shape and step count."""
    return f"""## OUTPUT (JSON ONLY — ARRAY OF STEPS)
Return **only** a valid JSON object of this form (no markdown fences, no text before or after):

{{
  "steps": [
    {{
      "instruction": "string — brief spoken line(s) for this step (Naturally mention posture name followed by movement and alignment cues as needed.) Sound more fresh like start of a new phase or posture.",
      "sensory_cue": "string or null — brief breath or body awareness when it adds value; use null when not needed. Sound like continuation of the same phase"
    }}
  ]
}}

* `steps` is an **array** of objects. Each object has **exactly** these two keys: `instruction`, `sensory_cue`.
* **`instruction` and `sensory_cue` (when not null) should be brief** but still complete the necessary guidance needed. Make it sound natural and human and imperfect using natural discourse markers sometimes ("alright", "from here", "gently", "slowly", "come on").
* You **MUST** include exactly **{expected_step_count}** element(s) in `steps`, in playback order. Each step’s `instruction` and `sensory_cue` are **separate** spoken clips: keep each one self-contained and easy to hear in sequence."""


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


def _optional_recommended_modifications_tag(ctx: TransitionRequestContext) -> str | None:
    """Subtle prompt tag when interval/vinyasa rows carry nested recommended_modification values."""
    hint = (ctx.modifications_hint or "").strip()
    if not hint:
        return None
    return (
        "<RECOMMENDED_MODIFICATIONS_HINT>\n"
        f"{hint}\n"
        "</RECOMMENDED_MODIFICATIONS_HINT>"
    )


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
    parts = [_section_preceding_transitional_hubs(ctx), _optional_recommended_modifications_tag(ctx)]
    parts.append(
        f"""<TIMED_FLOW>
{ctx.timed_flow_outline}
</TIMED_FLOW>"""
    )
    return "\n\n".join(p for p in parts if p)


def _section_interval_objective(ctx: TransitionRequestContext) -> str:
    rounds = ctx.expected_step_count // 2 if ctx.expected_step_count else 0
    
    # Text for handling the Hub entry
    hub_logic = ""
    if ctx.preceding_transitional_hub_names:
        hub_logic = """
### HUB TRAVEL & ROUND 1 ENTRY
When transitional hubs are listed above, the **first** object in `steps` must:
1. **The Lead-in:** Guide the user through every hub in order (e.g., "From Child's Pose, ripple through Table Top...") into the `<target_block>`.
2. **The Work Entry:** Immediately begin **Round 1, WORK** in the same audio beat.
3. **The Script Style:** Follow the 'Foundation' style below (Anatomical Setup). 
Do **not** repeat the hub travel after `steps[0]`.
"""

    return f"""
## OBJECTIVE (INTERVAL SET EVOLUTION)
There are {rounds} work/recovery round(s). The session expects **{ctx.expected_step_count}** objects in `steps`.

{hub_logic}

### INSTRUCTIONAL EVOLUTION RULES
You must evolve the narrative depth across the steps. Do not repeat the same technical setup in every round.

1. **ROUND 1 (The Foundation):** Use for `steps[0]`. Focus on **Alignment and Safety**. Use a 'Lead-in + Anatomical Setup' structure. Ensure the practitioner is stable in the shape. Weave `<recommended_modifications>` into the instruction.
   * *Example:* "Alright... finding your Boat Pose... just lifting the chest and keeping the spine long... maybe shins are parallel to the floor."

2. **ROUND 2 (The Sensory Engagement):** Focus on **Internal Effort**. Describe where they should feel the work and how to engage the breath to support the intensity.
   * *Example:* "Round two... noticing that fire in the core now... \n\n Can you lift the heart just an inch higher... as you keep that steady breath flowing?"

3. **ROUND 3+ (The Endurance & Focus):** Focus on **Psychological Staying Power**. Instructions should be sparse, using markers to help them stay present through the "burn."
   * *Example:* "Final push here... staying with that heat... \n\n Just finding stillness in the effort... you've got this... three more breaths."

4. **RECOVERY STEPS:** For every recovery step, use a soft discourse marker to signal the release (e.g., "And just... let that go," "Finding your rest here...").

### FORMATTING REQUIREMENT
* **Phonetic Pacing:** Use `...` for 1-second breaths and `\n\n` to separate movement from detail.
* **Steps Alignment:** If no hubs exist, `steps` matches `<TIMED_FLOW>` in order (Work then Recovery). Each `instruction` is the spoken script; `sensory_cue` is for internal awareness."
"""

def _section_vinyasa_resources(ctx: TransitionRequestContext) -> str:
    parts = [_section_preceding_transitional_hubs(ctx), _optional_recommended_modifications_tag(ctx)]
    parts.append(
        f"""<TIMED_FLOW>
{ctx.timed_flow_outline}
</TIMED_FLOW>"""
    )
    return "\n\n".join(p for p in parts if p)


def _section_vinyasa_objective(ctx: TransitionRequestContext) -> str:
    # Logic for handling the movement from Hubs into the first pose of the loop
    hub_logic = ""
    if ctx.preceding_transitional_hub_names:
        hub_logic = """
### HUB TRAVEL & ROUND 1 ENTRY
When transitional hubs are listed above, the **first** object in `steps` must:
1. **The Lead-in:** Guide through every hub in order (e.g., "From Downward Dog, rippling through Plank...") into the `<target_block>`.
2. **The Flow Entry:** Immediately perform the **first** posture named on Line 1 of `<TIMED_FLOW>` (this is the start of Round 1 — one audio beat).
3. **The Script Style:** Use the 'Foundation' style below (Anatomical Detail). 
Do **not** repeat the hub travel after `steps[0]`.
"""

    return f"""
## OBJECTIVE (VINYASA LOOP EVOLUTION)
Produce exactly **{ctx.expected_step_count}** objects in `steps`, aligned with `<TIMED_FLOW>` overall.

{hub_logic}

### INSTRUCTIONAL EVOLUTION RULES
You must differentiate the "Instructional Depth" between the initial setup and the repetitive flow.

1. **ROUND 1 (The Foundation):** Provide full anatomical guidance for every pose in this first cycle. Use a 'Lead-in + Action + Alignment Detail' structure. Focus on where the limbs go and how to stabilize the joints. Weave `<recommended_modifications>` into alignment.
   * *Example:* "Alright... as you inhale... reaching the arms up for a High Lunge... just making sure that front knee stays right over the ankle."

2. **SUBSEQUENT ROUNDS (The Rhythm):** Once the first cycle is complete, transition to **'Breath-First' coaching**. Strip away the alignment details. Focus purely on the sync between the movement and the inhale/exhale. Keep these punchy and rhythmic.
   * *Example:* "Inhale... reaching up. \n\n Exhale... sinking deep."

3. **THE LOOP RULE (Phonetic Pacing):** Every cycle—even the short rhythmic ones—must still use `...` for 1-second breaths and `\n\n` for phase breaks to maintain the human texture.

### FORMATTING REQUIREMENT
If there are **no** transitional hubs, each step matches `<TIMED_FLOW>` in order. Each `instruction` is the spoken script; `sensory_cue` may be null or a brief awareness line during the 'Foundation' round.
"""



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

    parts.append(_section_speech_cadence())
    parts.append(_section_output_schema(ctx.expected_step_count))
    return "\n\n".join(parts)
