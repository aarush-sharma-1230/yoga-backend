"""
Yoga Coordinator: guides practitioners through yoga sessions.

Responsible for spoken guidance (intro, transitions, ending), text generation
for user queries, and TTS. Uses session-mode developer prompt.
"""

import asyncio
from typing import Any, Dict, Optional

from app.prompts.developer import build_developer_prompt


class YogaCoordinator:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service

    async def generate_text(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate spoken guidance text from the LLM."""
        dp = await build_developer_prompt(self.auth_service, user_id, mode="session")
        response = await asyncio.to_thread(self.llm_client.generate_text, prompt=prompt, developer_prompt=dp)
        text = self._extract_text(response)
        return {
            **response,
            "text": text,
            "message_id": response.get("output", [{}])[0].get("id"),
        }

    async def generate_structured_text(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Return structured micro-instructions (movement, breath, awareness) for transitions."""
        dp = await build_developer_prompt(self.auth_service, user_id, mode="session")
        return await asyncio.to_thread(
            self.llm_client.generate_structured_text,
            prompt=prompt,
            developer_prompt=dp,
        )

    def generate_audio_from_text(self, text: str):
        """Generate audio chunks from text via TTS."""
        for chunk in self.llm_client.generate_audio(text=text):
            yield chunk

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
