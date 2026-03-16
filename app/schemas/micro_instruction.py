from typing import Literal, Optional

from pydantic import BaseModel

MicroInstructionType = Literal[
    "movement_instruction",
    "breath_instruction",
    "awareness_instruction",
]


class InstructionBlock(BaseModel):
    """Single instruction block with text. One per type."""

    text: str


class StructuredInstructionOutput(BaseModel):
    """
    Up to three instruction blocks. Movement instruction is required; others are optional.
    """

    movement_instruction: InstructionBlock
    breath_instruction: Optional[InstructionBlock] = None
    awareness_instruction: Optional[InstructionBlock] = None
