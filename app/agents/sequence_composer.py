"""
Sequence Composer: designs custom yoga sequences for practitioners.

Fetches user profile context and passes it to prompt builders. Responsible for
selecting and ordering postures from the catalogue based on profile and safety laws.
"""

import asyncio
from typing import Type, TypeVar

from pydantic import BaseModel

from app.prompts.developer import (
    extract_profile_context,
    get_sequence_composer_developer_prompt,
)

T = TypeVar("T", bound=BaseModel)


class SequenceComposer:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service
        self.model = "gpt-5.1"

    async def _get_developer_prompt(self, user_id: str | None) -> str:
        """Fetch profile, extract context, build developer prompt."""
        user = None
        if user_id:
            try:
                user = await self.auth_service.get_profile(str(user_id))
            except RuntimeError:
                pass
        ctx = extract_profile_context(user)
        return get_sequence_composer_developer_prompt(ctx)

    async def compose_sequence(
        self,
        prompt: str,
        response_format: Type[T],
        user_id: str | None = None,
    ) -> T:
        """Generate a structured sequence (e.g. CustomSequenceOutput) from the LLM."""
        dp = await self._get_developer_prompt(user_id)
        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=prompt,
            model=self.model,
            developer_prompt=dp,
            response_format=response_format,
        )
