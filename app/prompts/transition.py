from langchain_core.prompts import PromptTemplate


def get_transition_prompt(transition_from_idx: int, postures: list):
    postures_context = ", ".join([f"{posture['name']}" for posture in postures])

    if transition_from_idx == -1:
        template = f"""
        Your task is to guide the practitioner from the initial breathing phase into the first posture of the yoga sequence.

INPUT

Full Sequence: {postures_context}

First Posture: {postures[0]['name']}

GOAL

Gently transition the practitioner from a calm breathing state into the first posture of the yoga sequence.

INSTRUCTIONS

Begin by softly bringing the practitioner’s awareness back from the breathing exercise.

Invite them to slowly deepen their breath and become aware of their body again.

If their eyes are closed, gently invite them to open their eyes.

Guide them to notice their posture and grounding, such as the contact of the feet with the floor or the steadiness of their seat.

Mention the first posture the user will transition into and begin guiding the movement toward the first posture of the sequence..

Describe clearly how the practitioner should position their body to arrive in the first posture. Guide the movement step by step, helping them place their feet, hands, hips, and spine appropriately.

Once they arrive in the posture, provide a few important alignment cues that help establish the shape of the pose.

Then guide their attention inward again by suggesting where the gaze may rest and what sensations they may notice in the body.

Encourage the practitioner to take a few calm breaths in this first posture before continuing the sequence.

OUTPUT FORMAT

Return a JSON object with up to five optional fields. Each field, if present, must have "text".
Use at most one object per type. Combine all guidance of the same intent into a single text.

Keep each instruction to one or two short lines maximum (roughly 15–25 words each).

- pose_instruction (required): One line only. Names the upcoming posture, e.g. "Next up: Warrior One." or "We'll move into Downward Dog." May use "now", "alright", "let's" since it marks a new posture or phase.
- movement_instruction (required): All body positioning and movement guidance in one combined text (how to move into the posture). 
- alignment_instruction: All posture refinement cues in one combined text
- breath_instruction: All breathing guidance in one combined text
- awareness_instruction: Attention to sensations, gaze, inner focus

PHRASING RULES

- pose_instruction: One line only. Simply state the next posture name. May use "now", "alright", "let's", "so" to signal the transition into a new posture.
- movement_instruction, alignment_instruction, breath_instruction, awareness_instruction: Do NOT use "now", "alright", "let's", "so", "next". These are refinements within the same posture—flow directly without transitional openers.

The guidance should smoothly shift from stillness into the first posture.
        """

    else:
        template = f"""
    Your task is to guide the practitioner from one yoga posture to the next.

INPUT

Full Sequence: {postures_context}

Current Posture: {postures[transition_from_idx]['name']}

Next Posture: {postures[transition_from_idx + 1]['name']}

GOAL

Guide the practitioner smoothly and safely from the current posture into the next posture.

INSTRUCTIONS

Mention the posture the user will transition into.

Begin by gently preparing the practitioner to move out of the current posture.

Then guide the transition step by step in the natural order of body movement.

Describe clearly how different parts of the body move during the transition, such as:

* shifting weight
* repositioning hands or feet
* lifting or lowering the hips
* bending or straightening the legs
* lengthening the spine

Once the practitioner arrives in the next posture, provide a few important alignment cues that help refine the posture. Focus on the most meaningful details, such as the placement of the knees, hips, spine, shoulders, or feet.

After the posture is established, guide the practitioner to settle into it.

Suggest where the gaze may rest and invite them to notice sensations in the body such as areas of stability, stretch, or grounding.

Encourage a few slow and steady breaths in the posture.

OUTPUT FORMAT

Return a JSON object with up to five optional fields. Each field, if present, must have "text".
Use at most one object per type. Combine all guidance of the same intent into a single text.

Keep each instruction to one or two short lines maximum (roughly 15–25 words each).

- pose_instruction (required): One line only. Names the upcoming posture, e.g. "Next up: Warrior One." or "We'll move into Downward Dog." May use "now", "alright", "let's" since it marks a new posture or phase.
- movement_instruction (required): All body positioning and movement guidance in one combined text (how to move into the posture). 
- alignment_instruction: All posture refinement cues in one combined text
- breath_instruction: All breathing guidance in one combined text
- awareness_instruction: Attention to sensations, gaze, inner focus

PHRASING RULES

- pose_instruction: One line only. Simply state the next posture name. May use "now", "alright", "let's", "so" to signal the transition into a new posture.
- movement_instruction, alignment_instruction, breath_instruction, awareness_instruction: Do NOT use "now", "alright", "let's", "so", "next". These are refinements within the same posture—flow directly without transitional openers.

Clearly guide movement and allow the practitioner to settle into the final posture.
"""
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()