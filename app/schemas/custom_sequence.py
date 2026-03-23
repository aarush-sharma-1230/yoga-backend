"""Schema for LLM-generated custom yoga sequence."""

from typing import Literal

from pydantic import BaseModel, Field

POSTURE_INTENT_STATIC_HOLD = "static_hold"
POSTURE_INTENT_TRANSITIONAL_HUB = "transitional_hub"

PostureIntent = Literal["static_hold", "transitional_hub"]


class SequencePosture(BaseModel):
    """A posture in a flat sequence. Order in the array is flow order."""

    posture_id: str = Field(
        description="The posture client_id (e.g. p_mountain, p_downward_dog). Must be valid from the catalogue."
    )
    posture_intent: PostureIntent = Field(
        default=POSTURE_INTENT_STATIC_HOLD,
        description="static_hold = main posture to hold (default). transitional_hub = pass-through posture to bridge gaps between two main postures.",
    )
    recommended_modification: str = Field(
        default="",
        description="Any modification for this practitioner (from contraindications/chronic_pain) or leave empty.",
    )


class CustomSequenceOutput(BaseModel):
    """Structured output for a custom yoga sequence."""

    reasoning: str = Field(
        description="High-level reasoning explaining your sequence design: why you selected these postures, how you considered the practitioner's profile/safety, how you met the constraints, and the logic behind the flow."
    )
    name: str = Field(description="A short, descriptive name for the sequence (e.g. 'Morning Flow', 'Hip Opener')")
    postures: list[SequencePosture] = Field(
        description="Flat ordered list of postures in flow order. Each has posture_id, posture_intent (static_hold or transitional_hub), recommended_modification. Use static_hold for main poses to hold; use transitional_hub when injecting pass-through poses to bridge gaps (e.g. downward dog between warrior and forward fold). Must use valid client_ids from the catalogue."
    )
