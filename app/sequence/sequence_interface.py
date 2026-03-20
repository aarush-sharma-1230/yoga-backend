from typing import Optional

from pydantic import BaseModel


class SequenceData(BaseModel):
    sequence_id: str


class GenerateSequenceData(BaseModel):
    """Request body for generating a sequence via LLM.

    duration_minutes, focus, intensity_level are optional in the API body.
    Defaults are applied when omitted; downstream they are passed compulsorily.
    """

    duration_minutes: Optional[int] = 30
    focus: Optional[str] = "strength_and_flexibility_balanced"
    intensity_level: Optional[str] = "balanced"
    user_notes: Optional[str] = None


class CreateManualSequenceData(BaseModel):
    """Request body for creating a manual sequence designed by the user."""

    name: str
    posture_client_ids: list[str]
