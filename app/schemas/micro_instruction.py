from typing import Literal, Optional

from pydantic import BaseModel

MicroInstructionType = Literal[
    "movement_instruction",
    "alignment_instruction",
    "breath_instruction",
    "awareness_instruction",
]


class InstructionBlock(BaseModel):
    """Single instruction block with text. One per type."""
    text: str


class StructuredInstructionOutput(BaseModel):
    """
    Exactly four optional instruction blocks. At most one of each type.
    Movement instruction contains ALL movement guidance combined into one text.
    """

    movement_instruction: InstructionBlock
    alignment_instruction: Optional[InstructionBlock] = None
    awareness_instruction: Optional[InstructionBlock] = None
    breath_instruction: Optional[InstructionBlock] = None
