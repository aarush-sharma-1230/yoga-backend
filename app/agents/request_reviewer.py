"""
Request Reviewer: reviews practitioner profile against session preferences before sequence design.

Agent responsibility: receive pre-digested session briefing, build prompts, call LLM for structured review output.
Prompt functions receive pre-computed values only; no function calls inside prompts.
"""

import asyncio

from app.prompts.active import (
    get_request_review_prompt,
    get_request_reviewer_developer_prompt,
)
from app.schemas.request_review import RequestReviewOutput


class RequestReviewer:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.model = "gpt-5.4-mini"

    async def review_request(
        self,
        session_briefing: str,
        duration_minutes: int,
        theme: dict,
    ) -> RequestReviewOutput:
        """
        Review a sequence generation request for conflicts or ambiguities.

        Receives a pre-digested session briefing (produced by the briefing node)
        instead of raw profile data.
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
