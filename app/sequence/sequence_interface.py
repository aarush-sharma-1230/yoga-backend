from typing import Optional

from pydantic import BaseModel

from app.schemas.request_review import ReviewQuestionAnswered


class SequenceData(BaseModel):
    sequence_id: str


class GenerateSequenceData(BaseModel):
    """Request body for generating a sequence via LLM."""

    practice_theme_id: str
    duration_minutes: int
    user_notes: Optional[str] = None
    questions: Optional[list[ReviewQuestionAnswered]] = None


class CreateManualSequenceData(BaseModel):
    """Request body for creating a manual sequence designed by the user."""

    name: str
    posture_client_ids: list[str]
