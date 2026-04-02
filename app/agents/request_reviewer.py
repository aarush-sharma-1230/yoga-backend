"""
Request Reviewer: reviews practitioner profile against session preferences before sequence design.

Agent responsibility: fetch profile, build prompts, call LLM for structured review output.
Prompt functions receive pre-computed values only; no function calls inside prompts.
"""

import asyncio

from app.prompts.active import (
    extract_profile_context,
    get_request_review_prompt,
    get_request_reviewer_developer_prompt,
)
from app.schemas.request_review import RequestReviewOutput


class RequestReviewer:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service
        self.model = "gpt-5.4-mini"

    async def review_request(
        self,
        user_id: str,
        duration_minutes: int,
        theme: dict,
        user_notes: str | None = None,
    ) -> RequestReviewOutput:
        """
        Review a sequence generation request for conflicts or ambiguities.

        Fetches the user profile, cross-references it with session preferences,
        and returns structured questions (if any) plus a request summary.
        """
        user = await self.auth_service.get_profile(str(user_id))
        ctx = extract_profile_context(user)

        profile = user.get("profile") or {} if user else {}
        hard_strategy = profile.get("hard_priority_strategy") or {}
        medium_strategy = profile.get("medium_priority_strategy") or {}

        developer_prompt = get_request_reviewer_developer_prompt()
        user_prompt = get_request_review_prompt(
            ctx=ctx,
            hard_strategy=hard_strategy,
            medium_strategy=medium_strategy,
            theme=theme,
            duration_minutes=duration_minutes,
            user_notes=user_notes,
        )

        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
            response_format=RequestReviewOutput,
        )
