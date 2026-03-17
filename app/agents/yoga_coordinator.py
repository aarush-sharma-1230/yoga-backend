"""
Yoga Coordinator: guides practitioners through yoga sessions.

Fetches user profile context and passes it to prompt builders. Responsible for
spoken guidance (intro, transitions, ending), text generation for user queries,
and TTS.
"""

import asyncio
from typing import Any, Dict, Optional

from app.prompts.developer import (
    extract_profile_context,
    get_yoga_coordinator_developer_prompt,
)


class YogaCoordinator:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service

    async def _get_developer_prompt(self, user_id: Optional[str]) -> str:
        """Fetch profile, extract context, build developer prompt."""
        user = None
        if user_id:
            try:
                user = await self.auth_service.get_profile(str(user_id))
            except RuntimeError:
                pass
        ctx = extract_profile_context(user)
        return get_yoga_coordinator_developer_prompt(ctx)

    async def generate_text(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate spoken guidance text from the LLM."""
        dp = await self._get_developer_prompt(user_id)
        response = await asyncio.to_thread(self.llm_client.generate_text, prompt=prompt, developer_prompt=dp)
        text = self._extract_text(response)
        return {
            **response,
            "text": text,
            "message_id": response.get("output", [{}])[0].get("id"),
        }

    async def generate_structured_text(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Return structured micro-instructions (movement, breath, awareness) for transitions."""
        dp = await self._get_developer_prompt(user_id)
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
