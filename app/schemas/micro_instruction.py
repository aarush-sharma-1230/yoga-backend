from typing import Literal, Optional

from pydantic import BaseModel

MicroInstructionType = Literal[
    "pose_instruction",
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
    Up to five instruction blocks. pose_instruction comes first when applicable.
    Movement instruction is required; others are optional.
    """

    pose_instruction: InstructionBlock
    movement_instruction: InstructionBlock
    alignment_instruction: Optional[InstructionBlock] = None
    breath_instruction: Optional[InstructionBlock] = None
    awareness_instruction: Optional[InstructionBlock] = None
