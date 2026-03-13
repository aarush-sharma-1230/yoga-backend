from langchain_core.prompts import PromptTemplate


def get_introduction_prompt(sequence_name: str, user_name: str):
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

Return a JSON object with up to four optional fields. Each field, if present, must have "text" and "wait_time_in_seconds".

- movement_instruction: All body positioning and movement guidance in one combined text (e.g., "sit comfortably", "close your eyes")
- alignment_instruction: Posture refinement cues
- breath_instruction: All breathing guidance in one combined text
- awareness_instruction: Attention to sensations, gaze, inner focus

Use at most one object per type. Combine all guidance of the same intent into a single text. Choose wait_time_in_seconds (15-60) based on complexity. Order: movement, alignment, breath, awareness.
"""
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()
