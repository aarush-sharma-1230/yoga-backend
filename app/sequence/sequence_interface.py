from typing import Optional

from pydantic import BaseModel


class SequenceData(BaseModel):
    sequence_id: str


class GenerateSequenceData(BaseModel):
    """Request body for generating a sequence via LLM."""

    duration_minutes: Optional[int] = None
    focus: Optional[str] = None


class CreateManualSequenceData(BaseModel):
    """Request body for creating a manual sequence designed by the user."""

    name: str
    posture_client_ids: list[str]
