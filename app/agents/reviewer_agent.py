"""
Reviewer agent: requirement intake review and sequence safety/alignment review.

Uses the same LLM client with different developer and user prompts per task.
"""

import asyncio

from app.prompts.active import (
    get_request_review_prompt,
    get_request_reviewer_developer_prompt,
    get_sequence_review_user_prompt,
    get_sequence_reviewer_developer_prompt,
)
from app.schemas.request_review import RequestReviewOutput, SequenceReviewOutput


class ReviewerAgent:
    """Runs requirement review before composition and sequence review after composition."""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.model = "gpt-5.4-mini"

    async def review_requirements(
        self,
        session_briefing: str,
        duration_minutes: int,
        theme: dict,
    ) -> RequestReviewOutput:
        """
        Review the session request for conflicts or ambiguities before sequence design.

        Receives a pre-digested session briefing from the briefing node.
        """
        developer_prompt = get_request_reviewer_developer_prompt()
        user_prompt = get_request_review_prompt(
            session_briefing=session_briefing,
            theme=theme,
            duration_minutes=duration_minutes,
        )

        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
            response_format=RequestReviewOutput,
        )

    async def review_sequence(
        self,
        session_briefing: str,
        duration_minutes: int,
        theme: dict,
        composer_output: dict,
    ) -> SequenceReviewOutput:
        """
        Review a proposed sequence for safety and alignment with the briefing and request.
        """
        developer_prompt = get_sequence_reviewer_developer_prompt()
        user_prompt = get_sequence_review_user_prompt(
            session_briefing=session_briefing,
            theme=theme,
            duration_minutes=duration_minutes,
            composer_output=composer_output,
        )

        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
            response_format=SequenceReviewOutput,
        )
