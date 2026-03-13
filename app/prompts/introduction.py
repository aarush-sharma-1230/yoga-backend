from langchain_core.prompts import PromptTemplate


def get_introduction_prompt(sequence_name: str, user_name: str, first_posture_name: str = ""):
    """first_posture_name: name of first posture in sequence, for pose_instruction teaser."""
    template = f"""Your task is to generate a short spoken introduction for a yoga sequence.

INPUT
Sequence Name: {sequence_name}
User's Name: {user_name}
GOAL
Welcome the user into the session and guide them into a relaxed mental state before beginning the sequence.

STRUCTURE

1. Welcome

* Warmly welcome the user by their name to the session.
* Mention the sequence name naturally.
* Acknowledge and appreciate that the user showed up to practice.

2. Encouragement

* Offer a short, gentle word of encouragement for taking this time for themselves.

3. Breathing Preparation
   Guide the user into a simple calming breath exercise.

* Ask the user to sit or stand comfortably.
* Invite them to gently close their eyes or soften their gaze.

4. Breathing Guidance
   Guide a slow breathing pattern:

* Inhale slowly through the nose.
* Exhale slowly through the mouth or nose.
* The exhale should be slightly longer than the inhale.

While guiding the breath:

* Occasionally direct the user's attention to sensations such as the rise of the chest, the movement of the belly, or the feeling of air passing through the nose.
* Keep the pacing calm and spacious.

5. Independent Practice
   Tell the user to continue this breathing rhythm on their own for about 2–3 minutes before beginning the sequence.

STRUCTURED OUTPUT FORMAT

Return a JSON object with up to five optional fields. Each field, if present, must have "text".

Keep each instruction to one or two short lines maximum (roughly 15–25 words each).

- movement_instruction (required): All body positioning and movement guidance in one combined text (e.g., "sit comfortably", "close your eyes"). May use transitional phrases like "now", "alright", "let's" since it marks a new phase.
- alignment_instruction: Posture refinement cues
- breath_instruction: All breathing guidance in one combined text
- awareness_instruction: Attention to sensations, gaze, inner focus

PHRASING RULES

- movement_instruction: May use "now", "alright", "let's", "so" or similar phrases that signal a new phase or change. It comes first and can set the scene.
- alignment_instruction, breath_instruction, awareness_instruction: Do NOT use "now", "alright", "let's", "so", "next" or words that imply a new beginning. These are continuous refinements within the same moment—flow directly into the guidance without transitional openers.
</think>
"""
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()
