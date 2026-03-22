from typing import Optional

from pydantic import BaseModel, Field


class InstructionBlock(BaseModel):
    """Single instruction block with text."""

    text: str


class StructuredInstructionOutput(BaseModel):
    """
    Ordered instruction blocks for transitioning into a posture.

    When the target posture has entry_transitions, list brief movement cues to pass through each.
    basic_instruction covers the main posture (name, movement, alignment).
    sensory_cue draws from the posture's sensory cues for mindful awareness.
    """

    transition_movements: list[InstructionBlock] = Field(
        default_factory=list,
        max_length=3,
        description="Brief movement instructions to pass through transitional postures (entry_transitions). One per posture. Leave empty when the previous pose connects directly.",
    )
    basic_instruction: InstructionBlock = Field(
        description="Posture name, movement, and alignment for the main posture to hold.",
    )
    sensory_cue: Optional[InstructionBlock] = Field(
        default=None,
        description="Sensory or awareness cue for the main posture. Draw from provided sensory_cues or adapt for the practitioner.",
    )
