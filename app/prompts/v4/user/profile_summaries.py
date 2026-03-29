"""User prompts: profile strategy summarization."""

import json

from langchain_core.prompts import PromptTemplate


def get_hard_priority_summary_prompt(hard_priority_strategy: dict) -> str:
    """Build prompt to summarize HardPriorityStrategy (medical/contraindication) for session use."""
    template = """Your task is to write a brief, actionable summary of a yoga practitioner's health and safety constraints.

INPUT (JSON):
{strategy_json}

CONTEXT:
This summary will be included in prompts when a yoga session starts. It guides the instructor (LLM) to:
- Avoid or modify postures that could harm the practitioner (e.g. inversions for hypertension, spine flexion for herniated disc)
- Offer gentler alternatives for chronic pain areas (e.g. neck, lower back, knees)
- Respect recent surgery recovery

REQUIREMENTS:
- 2–4 concise sentences (40–80 words total)
- Focus only on what matters for posture selection and modification
- Mention specific conditions, pain areas, and any surgery-related cautions
- No filler or generic advice
- Written in third person (e.g. "Practitioner has...", "Avoid...")

OUTPUT:
A single paragraph of plain text, no bullet points."""
    strategy_json = json.dumps(hard_priority_strategy, indent=2)
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format(strategy_json=strategy_json)


def get_medium_priority_summary_prompt(medium_priority_strategy: dict) -> str:
    """Build prompt to summarize MediumPriorityStrategy (experience, goals) for session use."""
    template = """Your task is to write a brief, actionable summary of a yoga practitioner's experience and goals.

INPUT (JSON):
{strategy_json}

CONTEXT:
This summary will be included in prompts when a yoga session starts. It guides the instructor (LLM) to:
- Match cue complexity and pose intensity to experience level (beginner/intermediate/advanced)
- Emphasize goals (flexibility, strength, stress relief, spiritual practice)
- Account for general activity level (sedentary vs active)

REQUIREMENTS:
- 2–4 concise sentences (40–80 words total)
- Focus only on what matters for session personalization
- Mention experience level, activity level, primary goals
- No filler or generic advice
- Written in third person (e.g. "Practitioner is...", "Focus on...")

OUTPUT:
A single paragraph of plain text, no bullet points."""
    strategy_json = json.dumps(medium_priority_strategy, indent=2)
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format(strategy_json=strategy_json)
