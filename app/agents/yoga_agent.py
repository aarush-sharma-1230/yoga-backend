import asyncio
from typing import Any, Dict, Optional

from app.prompts.developer import get_developer_prompt


class YogaAgent:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service
        self.max_words = 100

    async def _build_developer_prompt(self, user_id: Optional[str] = None) -> str:
        """Fetch profile from AuthService, extract summaries, and build developer prompt."""
        if not user_id:
            return get_developer_prompt()
        try:
            user = await self.auth_service.get_profile(str(user_id))
        except RuntimeError:
            return get_developer_prompt()

        profile = user.get("profile") or {}
        hard = profile.get("hard_priority_summary") or ""
        medium = profile.get("medium_priority_summary") or ""
        return get_developer_prompt(hard, medium)

    async def generate_structured_text(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Return structured micro-instructions from the LLM. Fetches profile and builds developer prompt internally."""
        dp = await self._build_developer_prompt(user_id)
        response = await asyncio.to_thread(self.llm_client.generate_structured_text, prompt=prompt, developer_prompt=dp)
        return response

    async def generate_text(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate text from LLM. Fetches profile and builds developer prompt internally."""
        dp = await self._build_developer_prompt(user_id)
        response = await asyncio.to_thread(self.llm_client.generate_text, prompt=prompt, developer_prompt=dp)
        text = self._extract_text(response)
        return {
            **response,
            "text": text,
            "message_id": response.get("output", [{}])[0].get("id"),
        }

    def generate_audio_from_text(self, text: str):
        """Generate audio from already-generated text."""
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
