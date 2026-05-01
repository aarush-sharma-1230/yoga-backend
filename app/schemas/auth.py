"""Auth-related request/response Pydantic models."""

from typing import Any, Literal, Optional

from pydantic import BaseModel, EmailStr

MedicalCondition = Literal[
    "hypertension",
    "glaucoma",
    "vertigo",
    "herniated_disc",
    "osteoporosis",
    "heart_condition",
    "pregnancy",
]
ChronicPainArea = Literal["neck", "shoulders", "lower_back", "wrists", "knees", "ankles"]
ExperienceLevel = Literal["beginner", "intermediate", "advanced"]
ActivityLevel = Literal["sedentary", "active", "fleet"]
PrimaryGoal = Literal["flexibility", "strength", "stress_relief", "spiritual"]


class CreateUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class GoogleLoginRequest(BaseModel):
    """Google Identity Services ID token from the client."""

    id_token: str


class HardPriorityStrategy(BaseModel):
    medical_conditions: list[MedicalCondition]
    chronic_pain_areas: list[ChronicPainArea]
    recent_surgery: Optional[bool] = None
    user_notes: Optional[str] = None


class MediumPriorityStrategy(BaseModel):
    experience_level: Optional[ExperienceLevel] = None
    activity_level: Optional[ActivityLevel] = None
    primary_goal: list[PrimaryGoal]
    user_notes: Optional[str] = None


def default_user_profile() -> dict[str, Any]:
    """
    Nested profile shape for new users: strategies match persisted models; summaries are empty strings.

    Orchestration and prompts read ``hard_priority_strategy``, ``medium_priority_strategy``,
    ``hard_priority_summary``, and ``medium_priority_summary`` from the user document.
    """

    return {
        "hard_priority_strategy": HardPriorityStrategy(
            medical_conditions=[],
            chronic_pain_areas=[],
            recent_surgery=None,
            user_notes=None,
        ).model_dump(),
        "medium_priority_strategy": MediumPriorityStrategy(
            experience_level=None,
            activity_level=None,
            primary_goal=[],
            user_notes=None,
        ).model_dump(),
        "hard_priority_summary": "",
        "medium_priority_summary": "",
    }
