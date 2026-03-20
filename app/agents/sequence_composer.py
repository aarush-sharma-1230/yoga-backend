"""
Sequence Composer: designs custom yoga sequences for practitioners.

Agent responsibility: fetch data, call helpers, process information, build prompts.
Prompt functions receive pre-computed values only; no function calls inside prompts.
"""

import asyncio
from typing import Type, TypeVar

from pydantic import BaseModel

from app.posture_docs.all_postures import ALL_POSTURES
from app.prompts.developer import extract_profile_context, get_sequence_composer_developer_prompt
from app.prompts.helpers import (
    duration_to_posture_range,
    format_posture_catalogue,
    get_intensity_instruction,
)
from app.prompts.user import get_sequence_user_prompt

T = TypeVar("T", bound=BaseModel)


class SequenceComposer:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service
        self.model = "gpt-5.1"

    async def _get_profile_context(self, user_id: str):
        """Fetch profile and extract context."""
        user = await self.auth_service.get_profile(str(user_id))
        return extract_profile_context(user)

    async def compose_sequence(
        self,
        response_format: Type[T],
        user_id: str,
        duration_minutes: int,
        focus: str | None,
        intensity_level: str,
    ) -> T:
        """
        Generate a structured sequence (e.g. CustomSequenceOutput) from the LLM.

        Agent fetches posture count from duration, computes all prompt inputs,
        and passes pre-computed values to prompt builders.
        """
        # Agent: fetch and process all data
        posture_range_lo, posture_range_hi = duration_to_posture_range(duration_minutes)
        intensity_instruction = get_intensity_instruction(intensity_level, duration_minutes)
        catalogue = format_posture_catalogue(ALL_POSTURES)
        ctx = await self._get_profile_context(user_id)

        # Build prompts with pre-computed values (no function calls inside)
        developer_prompt = get_sequence_composer_developer_prompt(catalogue)
        user_prompt = get_sequence_user_prompt(
            ctx=ctx,
            posture_range_lo=posture_range_lo,
            posture_range_hi=posture_range_hi,
            focus=focus,
            intensity_instruction=intensity_instruction,
        )

        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
            response_format=response_format,
        )
