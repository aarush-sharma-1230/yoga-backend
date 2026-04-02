"""Schemas for the RequestReviewer agent: LLM output and client-side answer models."""

from typing import Literal

from pydantic import BaseModel, Field


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
