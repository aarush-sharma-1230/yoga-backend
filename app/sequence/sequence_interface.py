from typing import Optional

from pydantic import BaseModel


class SequenceData(BaseModel):
    sequence_id: str


class CreateCustomSequenceData(BaseModel):
    """Request body for creating a custom sequence."""

    user_id: str
    duration_minutes: Optional[int] = None
    focus: Optional[str] = None


class CreateManualSequenceData(BaseModel):
    """Request body for creating a manual sequence designed by the user."""

    name: str
    posture_client_ids: list[str]
