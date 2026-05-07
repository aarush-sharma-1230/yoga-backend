"""User prompts: profile strategy summarization and session briefings."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from langchain_core.prompts import PromptTemplate

if TYPE_CHECKING:
    from app.prompts.v4.developer.profile_context import ProfileContext


def get_session_briefing_prompt(
    ctx: ProfileContext,
    theme: dict,
    user_notes: str | None,
) -> str:
    """
    Build a prompt that distils the practitioner profile, session theme, and
    user notes into a single focused briefing paragraph.

    The output is consumed by the reviewer and composer agents as their sole
    source of practitioner context. When user notes are present, they outrank
    theme and general profile emphasis for session intent, except non-negotiable
    medical/safety constraints.
    """
    sections: list[str] = []

    sections.append(
        "Your task is to write a concise session briefing that merges a yoga practitioner's profile "
        "with their current session request. When the practitioner has provided user notes for this "
        "session, those notes are the strongest signal for what they want—prioritize them over the "
        "theme wording and over general goals/experience summaries from the stored profile, except "
        "where mandatory medical or safety constraints from the profile must still apply."
    )
    sections.append("")
    sections.append("## PRACTITIONER PROFILE")
    if ctx.user_medical_profile_summary:
        sections.append(f"User medical profile summary: {ctx.user_medical_profile_summary}")
    if ctx.user_goals_summary:
        sections.append(f"User goals summary: {ctx.user_goals_summary}")
    if ctx.laws_context:
        sections.append(f"\n{ctx.laws_context}")

    sections.append("")
    sections.append("## SESSION REQUEST")
    display_name = theme.get("display_name") or ""
    functional_category = theme.get("functional_category") or ""
    description = theme.get("description") or ""
    sections.append(f"Theme: {display_name} ({functional_category}). {description}")
    if user_notes:
        sections.append(f"User notes (highest priority for this session's intent): {user_notes}")

    sections.append("")
    sections.append(
        "## OUTPUT REQUIREMENTS\n"
        "Write a single paragraph of 80–120 words that:\n"
        "- If user notes are present, foreground them: the briefing must reflect what the practitioner "
        "asked for in those notes ahead of theme emphasis or generic profile goals, while still "
        "respecting non-negotiable medical/safety constraints from the profile\n"
        "- Highlights medical constraints specifically relevant to THIS theme (omit irrelevant ones)\n"
        "- Notes any tension between the practitioner's goals and the chosen theme\n"
        "- Distils user notes into actionable intent (when provided, this is the primary lens)\n"
        "- States the practitioner's experience level\n"
        "- Is written in third person (e.g. 'Practitioner has…')\n"
        "- Contains no filler, no bullet points, no headings — just a single plain-text paragraph"
    )

    return "\n".join(sections)


def get_user_medical_profile_summary_prompt(user_medical_profile: dict) -> str:
    """Build prompt to summarize user medical profile (medical/contraindication) for session use."""
    template = """Your task is to write a brief, actionable summary of a yoga practitioner's health and safety constraints.

USER MEDICAL PROFILE (JSON):
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
    strategy_json = json.dumps(user_medical_profile, indent=2)
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format(strategy_json=strategy_json)


def get_user_goals_summary_prompt(user_goals: dict) -> str:
    """Build prompt to summarize user goals (experience, activity, primary goals) for session use."""
    template = """Your task is to write a brief, actionable summary of a yoga practitioner's experience and goals.

USER GOALS (JSON):
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
    strategy_json = json.dumps(user_goals, indent=2)
    prompt_template = PromptTemplate(template=template)
    return prompt_template.format(strategy_json=strategy_json)
