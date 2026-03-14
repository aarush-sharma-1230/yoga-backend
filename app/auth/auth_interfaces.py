from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class GetUserData(BaseModel):
    user_id: str


class HardPriorityStrategy(BaseModel):
    medical_conditions: list[str]
    chronic_pain_areas: list[str]
    recent_surgery: Optional[str] = None


class MediumPriorityStrategy(BaseModel):
    experience_level: Optional[str] = None
    activity_level: Optional[str] = None
    primary_goal: list[str]
    mobility_limitations: list[str]


class UserProfilePayload(BaseModel):
    hard_priority_strategy: HardPriorityStrategy
    medium_priority_strategy: MediumPriorityStrategy
