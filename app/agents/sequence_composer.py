"""
Sequence Composer: designs custom yoga sequences for practitioners.

Builds developer prompt (catalogue + fixed rules) and user prompt (profile + session params).
Fetches user profile and passes session parameters to prompt builders.
"""

import asyncio
from pydantic import BaseModel
from typing import Type, TypeVar
from app.posture_docs.all_postures import ALL_POSTURES
from app.prompts.developer import (extract_profile_context, get_sequence_composer_developer_prompt)
from app.prompts.posture_catalogue import format_posture_catalogue
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
        focus: str,
        intensity_level: str,
    ) -> T:
        """
        Generate a structured sequence (e.g. CustomSequenceOutput) from the LLM.

        Developer prompt: catalogue + fixed rules (role, intensity matching, design rules).
        User prompt: practitioner profile + session parameters (duration, focus, intensity).
        """
        catalogue = format_posture_catalogue(ALL_POSTURES)
        developer_prompt = get_sequence_composer_developer_prompt(catalogue)
        ctx = await self._get_profile_context(user_id)
        user_prompt = get_sequence_user_prompt(
            ctx=ctx,
            duration_minutes=duration_minutes,
            focus=focus,
            intensity_level=intensity_level,
        )
        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
            response_format=response_format,
        )
