"""Auth-related request/response Pydantic models."""

from typing import Any, Literal, Optional

from pydantic import BaseModel

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


class GoogleLoginRequest(BaseModel):
    """Google Identity Services ID token from the client."""

    id_token: str


class UserMedicalProfile(BaseModel):
    medical_conditions: list[MedicalCondition]
    chronic_pain_areas: list[ChronicPainArea]
    recent_surgery: Optional[bool] = None
    user_notes: Optional[str] = None


class UserGoals(BaseModel):
    experience_level: Optional[ExperienceLevel] = None
    activity_level: Optional[ActivityLevel] = None
    primary_goal: list[PrimaryGoal]
    user_notes: Optional[str] = None


USER_MEDICAL_PROFILE_FIELD = "user_medical_profile"
USER_GOALS_FIELD = "user_goals"
USER_MEDICAL_PROFILE_SUMMARY_FIELD = "user_medical_profile_summary"
USER_GOALS_SUMMARY_FIELD = "user_goals_summary"

_LEGACY_HARD_STRATEGY_FIELD = "hard_priority_strategy"
_LEGACY_MEDIUM_STRATEGY_FIELD = "medium_priority_strategy"
_LEGACY_HARD_SUMMARY_FIELD = "hard_priority_summary"
_LEGACY_MEDIUM_SUMMARY_FIELD = "medium_priority_summary"


def resolve_user_medical_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Return persisted medical profile dict, preferring current keys with legacy fallback."""

    return (
        profile.get(USER_MEDICAL_PROFILE_FIELD)
        or profile.get(_LEGACY_HARD_STRATEGY_FIELD)
        or {}
    )


def resolve_user_goals(profile: dict[str, Any]) -> dict[str, Any]:
    """Return persisted goals dict, preferring current keys with legacy fallback."""

    return profile.get(USER_GOALS_FIELD) or profile.get(_LEGACY_MEDIUM_STRATEGY_FIELD) or {}


def resolve_user_medical_profile_summary(profile: dict[str, Any]) -> str:
    """Return LLM summary for medical profile, preferring current keys with legacy fallback."""

    return (
        profile.get(USER_MEDICAL_PROFILE_SUMMARY_FIELD)
        or profile.get(_LEGACY_HARD_SUMMARY_FIELD)
        or ""
    )


def resolve_user_goals_summary(profile: dict[str, Any]) -> str:
    """Return LLM summary for goals, preferring current keys with legacy fallback."""

    return profile.get(USER_GOALS_SUMMARY_FIELD) or profile.get(_LEGACY_MEDIUM_SUMMARY_FIELD) or ""


def default_user_profile() -> dict[str, Any]:
    """
    Nested profile shape for new users: nested objects match persisted models; summaries are empty strings.

    Orchestration and prompts read ``user_medical_profile``, ``user_goals``,
    ``user_medical_profile_summary``, and ``user_goals_summary`` from the user document.
    """

    return {
        USER_MEDICAL_PROFILE_FIELD: UserMedicalProfile(
            medical_conditions=[],
            chronic_pain_areas=[],
            recent_surgery=None,
            user_notes=None,
        ).model_dump(),
        USER_GOALS_FIELD: UserGoals(
            experience_level=None,
            activity_level=None,
            primary_goal=[],
            user_notes=None,
        ).model_dump(),
        USER_MEDICAL_PROFILE_SUMMARY_FIELD: "",
        USER_GOALS_SUMMARY_FIELD: "",
    }
