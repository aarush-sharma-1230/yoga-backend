"""
Sequence Composer: designs custom yoga sequences for practitioners.

Agent responsibility: receive pre-digested session briefing, call helpers, build prompts.
Prompt functions receive pre-computed values only; no function calls inside prompts.
"""

import asyncio
from typing import Type, TypeVar

from pydantic import BaseModel

from app.posture_docs.all_postures import ALL_POSTURES
from app.prompts.active import (
    duration_to_posture_range,
    format_posture_catalogue,
    get_sequence_composer_developer_prompt,
    get_sequence_user_prompt,
)

T = TypeVar("T", bound=BaseModel)


class SequenceComposer:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.model = "gpt-5.1"

    async def compose_sequence(
        self,
        response_format: Type[T],
        session_briefing: str,
        duration_minutes: int,
        theme: dict,
        review_qa_context: str | None = None,
    ) -> T:
        """
        Generate a structured sequence (e.g. CustomSequenceOutput) from the LLM.

        Receives a pre-digested session briefing (produced by the briefing node)
        instead of raw profile data.
        """
        posture_range_lo, posture_range_hi = duration_to_posture_range(duration_minutes)
        catalogue = format_posture_catalogue(ALL_POSTURES)

        developer_prompt = get_sequence_composer_developer_prompt(catalogue)
        user_prompt = get_sequence_user_prompt(
            session_briefing=session_briefing,
            posture_range_lo=posture_range_lo,
            posture_range_hi=posture_range_hi,
            theme=theme,
            review_qa_context=review_qa_context,
        )

        return await asyncio.to_thread(
            self.llm_client.generate_with_schema,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
            response_format=response_format,
        )
