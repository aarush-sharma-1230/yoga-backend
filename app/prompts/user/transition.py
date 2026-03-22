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

INPUT

Full Sequence: {ctx.full_sequence}
First Posture (to hold): {ctx.to_posture_name}
Entry Transitions (postures to pass through before the first): {entry_list}
Recommended Modification for this practitioner: {ctx.recommended_modification}

Sensory Cues (available for the first posture):
{ctx.sensory_cues_formatted}

CRITICAL: ENTRY TRANSITIONS RULE
When entry_transitions contains postures (i.e., the list above is NOT "None"), you MUST produce transition_movement instructions—exactly one per posture in the list. Do NOT skip them. When entry_transitions is empty, transition_movements must be an empty array.

GOAL

Gently transition the practitioner from a calm breathing state into the first posture.

If there are entry_transitions, first give brief movement cues to pass through each transitional posture. Then guide into the main posture with a basic instruction and a sensory cue.

INSTRUCTIONS

Begin by bringing awareness back from breathing.
If their eyes are closed, invite them to open their eyes.

If there are entry_transitions: for EACH posture in the list, produce one transition_movement with a short movement cue (how to move through it)—no alignment detail or sensory cues. Keep each to one or two sentences.

For the main posture: provide a basic_instruction (posture name, body positioning, movement, key alignment) and a sensory_cue (select or adapt from the sensory cues above).

Incorporate the recommended_modification in your alignment guidance when present.

OUTPUT FORMAT

Return JSON:
- transition_movements: Array of {{"text": "..."}} — exactly one per entry_transition when the list has postures; EMPTY array when there are none.
- basic_instruction: {{"text": "..."}} — posture name, movement, alignment for the main posture.
- sensory_cue: {{"text": "..."}} or null — awareness cue for the main posture.

Keep each instruction to one or two short lines (roughly 15–25 words). Sound like spoken guidance.
"""

    # Non-initial transition (from one posture to the next)
    return f"""Your task is to guide the practitioner from one yoga posture to the next.

INPUT

Full Sequence: {ctx.full_sequence}
Current Posture (leaving): {ctx.from_posture_name}
Next Posture (to hold): {ctx.to_posture_name}
Entry Transitions (postures to pass through before the next): {entry_list}
Recommended Modification for this practitioner: {ctx.recommended_modification}

Sensory Cues (available for the next posture):
{ctx.sensory_cues_formatted}

CRITICAL: ENTRY TRANSITIONS RULE
When entry_transitions contains postures (i.e., the list above is NOT "None"), you MUST produce transition_movement instructions—exactly one per posture in the list. Do NOT skip them. When entry_transitions is empty, transition_movements must be an empty array.

GOAL

Guide the practitioner smoothly and safely from the current posture into the next.

If there are entry_transitions, the previous pose does not connect directly. First give brief movement cues to pass through each transitional posture. Then guide into the main posture with a basic instruction and a sensory cue.

INSTRUCTIONS

Prepare the practitioner to move out of the current posture.

If there are entry_transitions: for EACH posture in the list, produce one transition_movement with a short movement cue (how to move through it)—no alignment detail or sensory cues. Keep each to one or two sentences.

For the main posture: provide a basic_instruction (posture name, body positioning, movement, key alignment) and a sensory_cue (select or adapt from the sensory cues above).

Incorporate the recommended_modification in your alignment guidance when present.

OUTPUT FORMAT

Return JSON:
- transition_movements: Array of {{"text": "..."}} — exactly one per entry_transition when the list has postures; EMPTY array when there are none.
- basic_instruction: {{"text": "..."}} — posture name, movement, alignment for the main posture.
- sensory_cue: {{"text": "..."}} or null — awareness cue for the main posture.

Keep each instruction to one or two short lines (roughly 15–25 words). Sound like spoken guidance.
"""
