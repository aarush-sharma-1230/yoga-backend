"""Auth-related request/response Pydantic models."""

from typing import Literal, Optional

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