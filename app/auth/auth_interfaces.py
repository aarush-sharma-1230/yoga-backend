from typing import Literal, Optional

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


class GetUserData(BaseModel):
    user_id: str


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
