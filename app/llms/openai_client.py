import json
import uuid
from typing import Type, TypeVar

import openai
from openai import APIError, OpenAI
from pydantic import BaseModel

from app.globals.errors import AIDependencyError, InternalAppError

from app.logs.api_call_logger import log_api_call
from app.usage import constants
from app.usage.request_cost_context import add_request_llm_cost_micro, is_request_llm_cost_tracking

T = TypeVar("T", bound=BaseModel)


def compute_llm_cost_micro_usd(
    *,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    reasoning_tokens: int | None = None,
    model: str,
    input_usd_per_million: float | None = None,
    output_usd_per_million: float | None = None,
    reasoning_usd_per_million: float | None = None,
) -> int:
    """
    Compute billed cost for one LLM call as integer micro-USD from token counts and per-million rates.

    Formula: ``round(input * R_in + output * R_out + reasoning * R_reason)`` where each ``R`` is
    USD per **million** tokens of that kind (so the sum is already micro-USD for that unit).

    ``model`` is reserved for future per-model rate tables.
    """
    _ = model
    r_in = input_usd_per_million if input_usd_per_million is not None else constants.INPUT_USD_PER_MILLION_TOKENS
    r_out = output_usd_per_million if output_usd_per_million is not None else constants.OUTPUT_USD_PER_MILLION_TOKENS
    r_reas = reasoning_usd_per_million if reasoning_usd_per_million is not None else constants.REASONING_USD_PER_MILLION_TOKENS
    inp = int(input_tokens or 0)
    out = int(output_tokens or 0)
    reas = int(reasoning_tokens or 0)
    total_micro = inp * r_in + out * r_out + reas * r_reas
    return int(round(total_micro))


DEFAULT_YOGA_TTS_INSTRUCTIONS = (
    "Speak as a calm, experienced yoga teacher guiding a live class. Use a warm, unhurried pace, "
    "clear articulation, and natural pauses. Gentle, encouraging intonation—never robotic, rushed, or sales-like. "
    "Fit short movement and breath cues."
)

ENERGETIC_YOGA_TTS_INSTRUCTIONS = (
    "Speak as a warm, motivating yoga teacher leading a live class. Use a slightly brighter, more upbeat energy than "
    "usual—still grounded and clear, never shouty or sales-like. Crisp cueing, confident pacing with natural pauses, "
    "encouraging tone suited to building movement and focus. Fit short movement and breath cues."
)

DEFAULT_TTS_VOICE = "sage"


class OpenAIClient:
    """OpenAI chat / responses / TTS client with optional per-request micro-USD accumulation."""

    def __init__(self, openai_api_key: str):
        self.is_text_enabled = True
        self.is_audio_enabled = True
        self.api_key = openai_api_key
        self.audio_model = "gpt-4o-mini-tts-2025-12-15"
        self.tts_voice = DEFAULT_TTS_VOICE
        self.temperature = 0.7
        openai.api_key = openai_api_key
        self._client = OpenAI(api_key=openai_api_key)

    def _micro_usd_for_chat_completion(self, completion, model: str) -> int:
        inp, out, reasoning = self._extract_usage_from_chat_completion(completion)
        return compute_llm_cost_micro_usd(
            input_tokens=inp,
            output_tokens=out,
            reasoning_tokens=reasoning,
            model=model,
        )

    def _micro_usd_for_responses_dict(self, resp_dict: dict, model: str) -> int:
        inp, out, reasoning = self._extract_usage_from_response_dict(resp_dict)
        return compute_llm_cost_micro_usd(
            input_tokens=inp,
            output_tokens=out,
            reasoning_tokens=reasoning,
            model=model,
        )

    def _track_micro_usd(self, micro: int) -> None:
        if is_request_llm_cost_tracking():
            add_request_llm_cost_micro(micro)

    def generate_with_schema_meta(
        self,
        prompt: str,
        developer_prompt: str,
        response_format: Type[T],
        model: str,
        temperature: float = 0.5,
    ) -> tuple[T, str]:
        """
        Parse chat completion into the given schema.

        Returns ``(parsed_model, message_id)``. When request-level cost tracking is active,
        ``OpenAIClient`` records micro-USD for this call via request-level cost tracking helpers.
        """
        messages = [
            {"role": "system", "content": developer_prompt},
            {"role": "user", "content": prompt},
        ]
        try:
            completion = self._client.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_format,
                temperature=temperature,
            )
        except APIError as exc:
            raise AIDependencyError() from exc
        parsed = completion.choices[0].message.parsed
        message_id = getattr(completion, "id", None) or f"msg_{uuid.uuid4().hex}"
        input_tokens, output_tokens, _reasoning = self._extract_usage_from_chat_completion(completion)
        output_str = parsed.model_dump_json(indent=2) if hasattr(parsed, "model_dump_json") else str(parsed)
        self._log_api_call(
            "generate_with_schema",
            developer_prompt,
            prompt,
            input_tokens,
            output_tokens,
            output=output_str,
        )
        micro = self._micro_usd_for_chat_completion(completion, model)
        self._track_micro_usd(micro)
        return parsed, message_id

    def generate_with_schema(
        self,
        prompt: str,
        developer_prompt: str,
        response_format: Type[T],
        model: str,
        temperature: float = 0.5,
    ) -> T:
        """Generate structured output conforming to the given Pydantic schema."""
        parsed, _message_id = self.generate_with_schema_meta(
            prompt=prompt,
            developer_prompt=developer_prompt,
            response_format=response_format,
            model=model,
            temperature=temperature,
        )
        return parsed

    def generate_text(
        self,
        prompt: str,
        developer_prompt: str,
        model: str,
        temperature: float = 0.7,
    ) -> dict:
        """
        Call the Responses API and return the response dict.

        When request-level cost tracking is enabled, accumulates micro-USD for this call.
        """
        if self.is_text_enabled:
            input = [{"role": "developer", "content": developer_prompt}, {"role": "user", "content": prompt}]
            try:
                response = openai.responses.create(model=model, input=input, temperature=temperature)
            except APIError as exc:
                raise AIDependencyError() from exc
            resp_dict = response.to_dict()
            input_tokens, output_tokens, _reasoning = self._extract_usage_from_response_dict(resp_dict)
            self._log_api_call(
                "generate_text",
                developer_prompt,
                prompt,
                input_tokens,
                output_tokens,
                output=json.dumps(resp_dict, indent=2),
            )
            micro = self._micro_usd_for_responses_dict(resp_dict, model)
            self._track_micro_usd(micro)
            return resp_dict
        raise InternalAppError()

    def generate_audio(
        self,
        text: str,
        instructions: str | None = None,
        model: str | None = None,
        voice: str | None = None,
    ):
        """Stream TTS audio chunks using gpt-4o-mini-tts steering and default yoga delivery instructions."""
        if not self.is_audio_enabled:
            raise InternalAppError()
        speech_model = model or self.audio_model
        speech_voice = voice if voice is not None else self.tts_voice
        speech_instructions = DEFAULT_YOGA_TTS_INSTRUCTIONS if instructions is None else instructions
        try:
            with self._client.audio.speech.with_streaming_response.create(
                model=speech_model,
                voice=speech_voice,
                input=text,
                instructions=speech_instructions,
            ) as response:
                for chunk in response.iter_bytes():
                    yield chunk
        except APIError as exc:
            raise AIDependencyError() from exc

    def _extract_usage_from_chat_completion(self, completion) -> tuple[int | None, int | None, int | None]:
        """Extract input, output, and optional reasoning token counts from a ChatCompletion."""
        usage = getattr(completion, "usage", None)
        if not usage:
            return (None, None, None)
        input_tokens = getattr(usage, "prompt_tokens", None)
        output_tokens = getattr(usage, "completion_tokens", None)
        reasoning = getattr(usage, "reasoning_tokens", None)
        if reasoning is None and hasattr(usage, "model_dump"):
            udict = usage.model_dump()
            reasoning = udict.get("reasoning_tokens")
        return (input_tokens, output_tokens, reasoning)

    def _extract_usage_from_response_dict(self, resp_dict: dict) -> tuple[int | None, int | None, int | None]:
        """Extract input, output, and optional reasoning token counts from a Responses API response dict."""
        usage = resp_dict.get("usage") or (resp_dict.get("output") or [{}])[0].get("usage")
        if not isinstance(usage, dict):
            return (None, None, None)
        input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens")
        output_tokens = usage.get("output_tokens") or usage.get("completion_tokens")
        reasoning = usage.get("reasoning_tokens")
        return (input_tokens, output_tokens, reasoning)

    def _log_api_call(
        self,
        call_type: str,
        developer_prompt: str,
        user_prompt: str,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        output: str | None = None,
    ) -> None:
        """Log an API call to disk (including output for non-audio calls)."""
        log_api_call(
            call_type=call_type,
            developer_prompt=developer_prompt,
            user_prompt=user_prompt,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            output=output,
        )
