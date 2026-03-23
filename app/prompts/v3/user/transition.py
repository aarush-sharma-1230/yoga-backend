"""User prompt: transition between yoga postures.

Prompt receives pre-computed TransitionContext only. No function calls inside.
All data fetching and formatting is done in the session layer (transition_context).
"""

from app.session.transition_context import TransitionContext


def get_transition_prompt(ctx: TransitionContext) -> str:
    """
    Build the transition prompt from pre-computed context.
    Pure template—no logic, no function calls.
    """
    entry_list = ", ".join(ctx.entry_transition_names) if ctx.entry_transition_names else "None"

    if ctx.is_initial:
        return f"""Your task is to guide the practitioner from the initial breathing phase into the first posture of the yoga sequence.

<SESSION_STATE>
<full_sequence_context>{ctx.full_sequence}</full_sequence_context>
<target_posture>{ctx.to_posture_name}</target_posture>
</SESSION_STATE>

<TARGET_RESOURCES>
<entry_transitions>Entry Transitions (postures to pass through before the next): {entry_list}</entry_transitions>
<recommended_modifications>Recommended Modification for this practitioner: {ctx.recommended_modification}</recommended_modifications>
<sensory_cues>Sensory Cues (available for the next posture): {ctx.sensory_cues_formatted}</sensory_cues>
<TARGET_RESOURCES>

## 1. CORE OBJECTIVE (THE AWAKENING)
Your task is to choreograph the spoken audio script that transitions the practitioner out of their initial centering/breathing phase and guides them safely into their very first `<target_posture>`.

## 2. TARGET POSTURE (THE FIRST ARRIVAL)
Guide the practitioner into the `<target_posture>` using two distinct cues:
* **[Basic Instruction]:** Naturally guide the practioner first by welcoming the user back from their grounding phase and asking them to open their eyes, then telling the next posture name, and then how to position the body, the primary alignment. If a `<recommended_modification>` is present, you MUST seamlessly weave it into this instruction as a natural suggestion, not a clinical warning.
* **[Sensory Cue]:** Select or adapt one awareness cue from `<available_sensory_cues>` to ground the practitioner in this first physical hold.

## 3. OUTPUT SCHEMA
You must return ONLY a valid JSON object matching this exact structure. Do not include markdown formatting (like ```json) or conversational text.

{{
  "basic_instruction": {{
    "text": "String (15-25 words. eye-opening cue, posture name, movement, alignment, modifications)"
  }},
  "sensory_cue": {{
    "text": "String (15-25 words focusing on breath or body awareness) or null"
  }}
}}
"""

    # Non-initial transition (from one posture to the next)
    return f"""
<SESSION_STATE>
<full_sequence_context>{ctx.full_sequence}</full_sequence_context>
<current_posture>{ctx.from_posture_name}</current_posture>
<target_posture>{ctx.to_posture_name}</target_posture>
</SESSION_STATE>

<TARGET_RESOURCES>
<entry_transitions>Entry Transitions (postures to pass through before the next): {entry_list}</entry_transitions>
<recommended_modifications>Recommended Modification for this practitioner: {ctx.recommended_modification}</recommended_modifications>
<sensory_cues>Sensory Cues (available for the next posture): {ctx.sensory_cues_formatted}</sensory_cues>
<TARGET_RESOURCES>

## 1. CORE OBJECTIVE
Your task is to choreograph the spoken audio script guiding the practitioner safely from the `<current_posture>` into the `<target_posture>`.

##2. ENTRY TRANSITIONS (THE BRIDGE)
When entry_transitions contains postures (i.e., the list above is NOT "None"), you MUST produce transition_movement instructions—exactly one per posture in the list. When entry_transitions is empty, transition_movements must be an empty array.

## 3. TARGET POSTURE (THE ARRIVAL)
Once routing is complete, you must guide the practitioner into the `<target_posture>` using two distinct cues:
* **[Basic Instruction]:** Naturally guide the practioner first by telling the next posture name and then how to position the body, the primary alignment. If a `<recommended_modification>` is present, you MUST seamlessly weave it into this instruction as a natural suggestion, not a clinical warning.
* **[Sensory Cue]:** Select or adapt one awareness cue from the `<available_sensory_cues>` to ground the practitioner once they have arrived in the pose.

## 4. OUTPUT FORMAT

You must return ONLY a valid JSON object matching this exact structure. Do not include markdown formatting (like ```json) or conversational text.

RETURN JSON
{{
  "transition_movements": [
    {{
      "text": "String (15-25 words guiding through the transitional hub)"
    }}
  ],
  "basic_instruction": {{
    "text": "String (25-40 words covering name, movement, alignment, and modifications)"
  }},
  "sensory_cue": {{
    "text": "String (15-25 words focusing on breath or body awareness) or null"
  }}
}}
"""
