"""Schemas for requirement and sequence reviewer agents and client-side answer models."""

from typing import Literal, Optional

from pydantic import BaseModel, Field

ALIGNMENT_SCORE_THRESHOLD = 7
"""Minimum alignment score (1–10) required for a sequence to pass, when ``safety_pass`` is True."""


class ReviewQuestionOption(BaseModel):
    """One selectable option within a review question."""

    id: str = Field(description="Short identifier, e.g. 'a', 'b', 'c'")
    description: str = Field(description="Human-readable option text")


class ReviewQuestion(BaseModel):
    """A single clarification question surfaced by the reviewer."""

    id: str = Field(description="Unique question identifier")
    question: str = Field(description="The question text to display")
    type: Literal["single_select", "multi_select"] = Field(
        description="Whether the user may pick one or multiple options"
    )
    options: list[ReviewQuestionOption] = Field(description="Available answer choices")


class RequestReviewOutput(BaseModel):
    """Structured LLM output from the RequestReviewer agent."""

    status: bool = Field(
        description="True when requirements are clear and sequence generation can proceed; False when clarification is needed"
    )
    questions: list[ReviewQuestion] = Field(
        description="Clarification questions for the practitioner; empty when status is True"
    )


class ReviewQuestionAnswered(BaseModel):
    """One answered question sent back by the client on the second call."""

    question: str = Field(description="The original question string")
    answer: list[str] = Field(description="Selected answer description(s)")


class SequenceReviewOutput(BaseModel):
    """Structured LLM output from the sequence safety and alignment reviewer."""

    safety_pass: bool = Field(description="False if any serious safety issue makes the sequence unacceptable as-is")
    safety_issues: list[str] = Field(
        default_factory=list,
        description="Concrete safety problems; empty when safety_pass is True",
    )
    safety_score_1_to_10: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Diagnostic only; gating uses safety_pass, not this score",
    )
    alignment_score_1_to_10: int = Field(
        ge=1,
        le=10,
        description="How well the sequence matches theme, duration, and briefing intent (non-safety)",
    )
    alignment_notes: str = Field(default="", description="Brief justification for the alignment score")
    feedback_for_composer: str = Field(
        default="",
        description="Actionable revision instructions when the sequence does not pass overall",
    )


def sequence_review_passes(output: SequenceReviewOutput) -> bool:
    """Whether the sequence meets safety and alignment bars."""
    return output.safety_pass and output.alignment_score_1_to_10 >= ALIGNMENT_SCORE_THRESHOLD
