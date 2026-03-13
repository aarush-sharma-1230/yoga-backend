from langchain_core.prompts import PromptTemplate

def get_ending_prompt(sequence_name: str):
    template = f"""Your task is to generate the closing guidance for a yoga session.

INPUT

Sequence Name: {sequence_name}

GOAL

Gently close the yoga session and allow the practitioner to leave the practice feeling calm, grounded, and appreciative of the time they spent practicing.

INSTRUCTIONS

Begin by acknowledging the completion of the yoga sequence.

Invite the practitioner to take a few slow and comfortable breaths and notice how their body feels after the practice.

Encourage them to briefly observe sensations such as:

* the steadiness of their breath
* the feeling of relaxation or openness in the body
* the sense of calm or quiet in the mind

Offer a short reflection that appreciates the time they gave to their practice and to their own well-being.

End the session with a gentle closing message that leaves the practitioner feeling grounded and ready to return to the rest of their day.
"""
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format()