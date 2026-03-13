from typing import Literal

from pydantic import BaseModel

MicroInstructionType = Literal[
    "movement_instruction",
    "alignment_instruction",
    "breath_instruction",
    "awareness_instruction",
]


class MicroInstruction(BaseModel):
    type: MicroInstructionType
    text: str
    wait_time_in_seconds: int


class MicroInstructionList(BaseModel):
    instructions: list[MicroInstruction]
