"""
Sequence Composer: designs custom yoga sequences for practitioners.

Responsible for selecting and ordering postures from the catalogue based on
user profile, safety laws, and optional constraints. Uses sequence-mode
developer prompt and structured output.
"""

import asyncio
from typing import Type, TypeVar

from pydantic import BaseModel

from app.prompts.developer import build_developer_prompt

T = TypeVar("T", bound=BaseModel)


class SequenceComposer:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service

    async def compose_sequence(
        self,
        prompt: str,
        response_format: Type[T],
        user_id: str | None = None,
    ) -> T:
        """Generate a structured sequence (e.g. CustomSequenceOutput) from the LLM."""
        dp = await build_developer_prompt(self.auth_service, user_id, mode="sequence")
        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=prompt,
            developer_prompt=dp,
            response_format=response_format,
        )
