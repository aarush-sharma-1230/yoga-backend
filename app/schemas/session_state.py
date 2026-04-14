"""Request models for updating persisted session playback state on the session document."""

from __future__ import annotations

from typing import Annotated, Literal, Optional, Union

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, ConfigDict, Field, field_validator


SessionPlayStatus = Literal["not_started", "in_progress", "completed"]


class CurrentPositionIntro(BaseModel):
    """Client is in the intro segment."""

    model_config = ConfigDict(extra="forbid")

    segment_kind: Literal["intro"] = "intro"

class CurrentPositionEnding(BaseModel):
    """Client is in the intro segment."""

    model_config = ConfigDict(extra="forbid")

    segment_kind: Literal["ending"] = "ending"


class CurrentPositionPosture(BaseModel):
    """Client is in a sequence posture segment."""

    model_config = ConfigDict(extra="forbid")

    segment_kind: Literal["posture"] = "posture"
    sequence_posture_id: str

    @field_validator("sequence_posture_id")
    @classmethod
    def validate_sequence_posture_id(cls, value: str) -> str:
        """Ensure sequence_posture_id is a valid MongoDB ObjectId string."""
        try:
            ObjectId(value)
        except InvalidId as exc:
            raise ValueError("sequence_posture_id must be a valid ObjectId string") from exc
        return value


CurrentPosition = Annotated[
    Union[CurrentPositionIntro, CurrentPositionPosture, CurrentPositionEnding],
    Field(discriminator="segment_kind"),
]


class CurrentSessionStateRequest(BaseModel):
    """Payload for POST /session/{session_id}/current_session_state."""

    model_config = ConfigDict(extra="forbid")

    session_play_status: SessionPlayStatus
    current_position: Optional[CurrentPosition]
