import traceback
import uuid
from typing import Type, TypeVar

import openai
from openai import OpenAI
from pydantic import BaseModel

from app.logs.api_call_logger import log_api_call
from app.schemas.micro_instruction import StructuredInstructionOutput

T = TypeVar("T", bound=BaseModel)


class OpenAIClient:
    def __init__(self, openai_api_key: str):
        self.is_api_enabled = True
        self.api_key = openai_api_key
        self.text_model = "gpt-4o-mini"
        self.audio_model = "gpt-4o-mini-tts"
        self.temperature = 0.7
        openai.api_key = openai_api_key
        self._client = OpenAI(api_key=openai_api_key)

    def generate_structured_text(
        self,
        prompt: str,
        developer_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ) -> dict:
        """Return structured micro-instructions: at most one per type (movement, alignment, awareness, breath)."""
        messages = [{"role": "system", "content": developer_prompt}, {"role": "user", "content": prompt}]
        completion = self._client.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=StructuredInstructionOutput,
            temperature=temperature,
        )

        parsed = completion.choices[0].message.parsed
        message_id = getattr(completion, "id", None) or f"msg_{uuid.uuid4().hex}"

        input_tokens, output_tokens = self._extract_usage_from_chat_completion(completion)
        self._log_api_call("generate_structured_text", developer_prompt, prompt, input_tokens, output_tokens)

        instructions = []
        for type_name, block in [
            ("movement_instruction", parsed.movement_instruction),
            ("breath_instruction", parsed.breath_instruction),
            ("awareness_instruction", parsed.awareness_instruction),
        ]:
            if block is not None:
                instructions.append({"type": type_name, "text": block.text})

        return {"instructions": instructions, "message_id": message_id}

    def generate_with_schema(
        self,
        prompt: str,
        developer_prompt: str,
        response_format: Type[T],
        model: str = "gpt-4o-mini",
        temperature: float = 0.5,
    ) -> T:
        """Generate structured output conforming to the given Pydantic schema."""
        messages = [
            {"role": "system", "content": developer_prompt},
            {"role": "user", "content": prompt},
        ]
        completion = self._client.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format,
            temperature=temperature,
        )
        parsed = completion.choices[0].message.parsed
        input_tokens, output_tokens = self._extract_usage_from_chat_completion(completion)
        self._log_api_call("generate_with_schema", developer_prompt, prompt, input_tokens, output_tokens)
        return parsed

    def generate_text(
        self,
        prompt: str,
        developer_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ) -> str:
        if self.is_api_enabled:
            input = [{"role": "developer", "content": developer_prompt}, {"role": "user", "content": prompt}]
            response = openai.responses.create(model=model, input=input, temperature=temperature)
            resp_dict = response.to_dict()
            input_tokens, output_tokens = self._extract_usage_from_response_dict(resp_dict)
            self._log_api_call("generate_text", developer_prompt, prompt, input_tokens, output_tokens)
            return resp_dict

    def generate_audio(self, text: str, instructions: str | None = None, model: str = "gpt-4o-mini-tts", voice: str = "nova"):
        if self.is_api_enabled:
            with openai.audio.speech.with_streaming_response.create(model=model, voice=voice, input=text) as response:
                for chunk in response.iter_bytes():
                    yield chunk

    def _extract_usage_from_chat_completion(self, completion) -> tuple[int | None, int | None]:
        """Extract input and output token counts from a ChatCompletion."""
        usage = getattr(completion, "usage", None)
        if not usage:
            return (None, None)
        input_tokens = getattr(usage, "prompt_tokens", None)
        output_tokens = getattr(usage, "completion_tokens", None)
        return (input_tokens, output_tokens)

    def _extract_usage_from_response_dict(self, resp_dict: dict) -> tuple[int | None, int | None]:
        """Extract input and output token counts from a Responses API response dict."""
        usage = resp_dict.get("usage") or (resp_dict.get("output") or [{}])[0].get("usage")
        if not isinstance(usage, dict):
            return (None, None)
        input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens")
        output_tokens = usage.get("output_tokens") or usage.get("completion_tokens")
        return (input_tokens, output_tokens)

    def _log_api_call(
        self,
        call_type: str,
        developer_prompt: str,
        user_prompt: str,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
    ) -> None:
        """Log an API call to disk."""
        log_api_call(
            call_type=call_type,
            developer_prompt=developer_prompt,
            user_prompt=user_prompt,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
