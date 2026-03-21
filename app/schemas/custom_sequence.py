"""Schema for LLM-generated custom yoga sequence."""

from pydantic import BaseModel, Field


class SequencePosture(BaseModel):
    """A posture in the sequence with optional transitional poses before it."""

    posture_id: str = Field(
        description="The main posture client_id (e.g. p_mountain, p_warrior_1_left). Must be valid from the catalogue. This is the pose the practitioner will hold."
    )
    entry_transitions: list[str] = Field(
        default_factory=list,
        description="ONLY when the previous held pose has no direct link to this one (per typical_entries/typical_exits): list client_ids from the catalogue that bridge the gap. Use only valid catalogue IDs. Leave empty when the previous pose connects directly.",
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
        description="Ordered list of postures to hold. Each has posture_id (main pose to hold), entry_transitions (transitional poses to flow through before it), and recommended_modification. Use entry_transitions for poses that should not be held long—e.g. passing through downward dog on the way to warrior. Must use valid client_ids from the catalogue."
    )
