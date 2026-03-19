"""
Summary Agent: summarizes user profile strategies into concise text.

Fetches context (strategy dict) from caller and passes it to user prompt builder.
Uses static developer prompt. Parallel with YogaCoordinator and SequenceComposer.
"""

import asyncio
from typing import Any, Dict, Literal

from app.prompts.developer import get_summary_developer_prompt
from app.prompts.user.profile_summaries import (
    get_hard_priority_summary_prompt,
    get_medium_priority_summary_prompt,
)


class SummaryAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.model = "gpt-5.4-mini"

    async def generate_summary(
        self,
        strategy: dict,
        summary_type: Literal["hard", "medium"],
    ) -> Dict[str, Any]:
        """Generate a summary from the given strategy. Fetches prompts and calls LLM."""
        if summary_type == "hard":
            user_prompt = get_hard_priority_summary_prompt(strategy)
        else:
            user_prompt = get_medium_priority_summary_prompt(strategy)
        developer_prompt = get_summary_developer_prompt()
        response = await asyncio.to_thread(
            self.llm_client.generate_text,
            prompt=user_prompt,
            model=self.model,
            developer_prompt=developer_prompt,
        )
        text = self._extract_text(response)
        return {"text": text, "message_id": response.get("output", [{}])[0].get("id")}

    def _extract_text(self, response: Dict[str, Any]) -> str:
        output = response.get("output", [])
        if not output:
            raise RuntimeError("LLM response has no output")
        content = output[0].get("content", [])
        if not content:
            raise RuntimeError("LLM response has no content")
        text = content[0].get("text", "")
        if not text:
            raise RuntimeError("LLM response has empty text")
        return text
