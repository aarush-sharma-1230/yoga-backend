"""Schema for LLM-generated custom yoga sequence."""

from pydantic import BaseModel, Field


class CustomSequenceOutput(BaseModel):
    """Structured output for a custom yoga sequence."""

    reasoning: str = Field(
        description="High-level reasoning explaining your sequence design: why you selected these postures, how you considered the practitioner's profile/safety, how you met the constraints, and the logic behind the flow."
    )
    name: str = Field(description="A short, descriptive name for the sequence (e.g. 'Morning Flow', 'Hip Opener')")
    posture_ids: list[str] = Field(description="Ordered list of posture client_ids (e.g. p_mountain, p_downward_dog). Must be valid IDs from the catalogue.")
