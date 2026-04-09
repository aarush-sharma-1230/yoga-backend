"""Request and LLM output models for pose landmark correction."""

from __future__ import annotations

from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


UserOrientation = Literal["facing_camera", "facing_away", "left_profile", "right_profile"]


class WorldLandmark(BaseModel):
    """One MediaPipe-style world landmark."""

    model_config = ConfigDict(extra="ignore")

    x: float
    y: float
    z: float
    visibility: float


class PostureCheckResultBase(BaseModel):
    """Shared fields for a single geometric check result."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    type: str
    name: str
    description: str


class AngleCheckResult(PostureCheckResultBase):
    """Angle check: measured value vs ideal range."""

    type: Literal["angle"] = "angle"
    measured_value: float = Field(alias="measuredValue")
    ideal_range: tuple[float, float] = Field(alias="idealRange")
    projection: str


class VerticalAlignmentCheckResult(PostureCheckResultBase):
    """Alignment to a vertical reference (e.g. world up) vs ideal range."""

    type: Literal["vertical_alignment"] = "vertical_alignment"
    measured_value: float = Field(alias="measuredValue")
    ideal_range: tuple[float, float] = Field(alias="idealRange")
    basis: str


PoseCheckResult = Annotated[
    Union[AngleCheckResult, VerticalAlignmentCheckResult],
    Field(discriminator="type"),
]


class PoseLandmarksRequest(BaseModel):
    """Client payload for POST /session/{sessionId}/pose_landmarks."""

    model_config = ConfigDict(populate_by_name=True)

    posture_client_id: str
    orientation: UserOrientation
    world_landmarks: list[WorldLandmark] = Field(
        ...,
        description="Typically 33 points; order matches the client landmark schema.",
    )
    checks: list[PoseCheckResult] = Field(..., min_length=1)


class PostureCorrectionInstructionOutput(BaseModel):
    """Structured LLM output: optional short combined cue; the model decides when feedback is warranted."""

    instruction: Optional[str] = Field(
        default=None,
        description=(
            "Short combined spoken-style cue for issues that matter for this practitioner, or null/empty when "
            "the posture is acceptable and no verbal feedback is needed. No bullet lists."
        ),
    )
