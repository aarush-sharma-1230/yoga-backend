"""Schema for LLM-generated custom yoga sequence."""

from pydantic import BaseModel, Field


class CustomSequenceOutput(BaseModel):
    """Structured output for a custom yoga sequence."""

    name: str = Field(description="A short, descriptive name for the sequence (e.g. 'Morning Flow', 'Hip Opener')")
    posture_ids: list[str] = Field(description="Ordered list of posture client_ids (e.g. p_mountain, p_downward_dog). Must be valid IDs from the catalogue.")
