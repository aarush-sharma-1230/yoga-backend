"""Agent for summarizing user profile data (medical, experience) into concise summaries."""

import asyncio
from typing import Any, Dict

from app.prompts.summary_system import SUMMARY_SYSTEM_PROMPT


class SummaryAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    async def generate_summary(self, prompt: str) -> Dict[str, Any]:
        """Generate a summary from the given prompt. Uses a summarizer system prompt."""
        response = await asyncio.to_thread(
            self.llm_client.generate_text,
            prompt=prompt,
            developer_prompt=SUMMARY_SYSTEM_PROMPT,
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
