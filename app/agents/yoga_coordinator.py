"""
Yoga Coordinator: guides practitioners through yoga sessions.

Fetches user profile context and passes it to prompt builders. Responsible for
spoken guidance (intro, transitions, ending), text generation for user queries,
and TTS.
"""

import asyncio
from typing import Any, Dict, Optional

from app.prompts.active import (
    extract_profile_context,
    get_transition_prompt,
    get_yoga_coordinator_developer_prompt,
)
from app.schemas.transition_guidance import TransitionGuidanceOutput
from app.session.transition_request import TransitionRequestContext


class YogaCoordinator:
    def __init__(self, llm_client, auth_service):
        self.llm_client = llm_client
        self.auth_service = auth_service
        self.model = "gpt-5.4-mini"

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

    async def generate_intro_or_ending(self, prompt: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate spoken guidance text from the LLM."""
        dp = await self._get_developer_prompt(user_id)
        response = await asyncio.to_thread(self.llm_client.generate_text, prompt=prompt, developer_prompt=dp, model=self.model)
        text = self._extract_text(response)
        return {
            **response,
            "text": text,
            "message_id": response.get("output", [{}])[0].get("id"),
        }

    async def generate_transition_guidance(
        self,
        ctx: TransitionRequestContext,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build v4 transition prompts, call the LLM with TransitionGuidanceOutput, validate step count,
        and return serialized steps (no flattening to legacy instruction rows).
        """
        prompt = get_transition_prompt(ctx)
        dp = await self._get_developer_prompt(user_id)
        parsed, message_id = await asyncio.to_thread(
            self.llm_client.generate_with_schema_meta,
            prompt=prompt,
            developer_prompt=dp,
            response_format=TransitionGuidanceOutput,
            model=self.model,
            temperature=0.7,
        )
        if parsed is None:
            raise RuntimeError("LLM returned no parsed transition guidance")
        steps = parsed.steps
        expected = ctx.expected_step_count
        if expected > 0 and len(steps) != expected:
            raise RuntimeError(
                f"Transition step count mismatch for index {ctx.target_idx}: expected {expected}, got {len(steps)}"
            )
        return {
            "message_id": message_id,
            "steps": [s.model_dump() for s in steps],
        }

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
