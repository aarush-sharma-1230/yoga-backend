"""User prompt: introduction to yoga session."""

from langchain_core.prompts import PromptTemplate


def get_introduction_prompt(sequence_name: str, user_name: str) -> str:
    """Introduction to yoga session prompt."""
    template = f"""Your task is to generate a short spoken introduction for a yoga sequence.

INPUT
Sequence Name: {sequence_name}
User's Name: {user_name}

GOAL
Welcome the user into the session and guide them into a relaxed mental state before beginning the sequence.

STRUCTURE

1. Welcome
    Warmly welcome the user by their name to the session, and acknowledge their presence to this practice.

2. Breathing Preparation
   Invite the user to a simple calming breath exercise in a comfortable position before the sequence is started.

3. Breathing Guidance
   Guide a slow breathing pattern:

* Inhale through the nose.
* Exhale through the mouth or nose a little slower than the inhale

While guiding the breath, occasionally direct the user's attention to sensations such as the rise of the chest, the movement of the belly, or the feeling of air passing through the nose.

4. Independent Practice
   Tell the user to continue this breathing rhythm on their own for about 2–3 minutes before beginning the sequence.

OUTPUT REQUIREMENTS

* 80-100 words
* Written as spoken guidance
* No bullet points
* No numbered lists
* Natural pacing suitable for voice narration

EXAMPLE STYLE (not to be copied verbatim)
"Alright… welcome to today's session. I'm really glad you're here…"
"""
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()
