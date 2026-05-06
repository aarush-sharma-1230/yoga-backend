import json
import uuid
from typing import Type, TypeVar

import openai
from openai import APIResponseValidationError, LengthFinishReasonError, OpenAI
from pydantic import BaseModel

from app.globals.errors import InternalAppError

from app.llms.openai_policy import (
    DEFAULT_TTS_VOICE,
    DEFAULT_YOGA_TTS_INSTRUCTIONS,
    MAX_STRUCTURED_OUTPUT_ATTEMPTS,
    compute_llm_cost_micro_usd,
    extract_usage_from_chat_completion,
    extract_usage_from_response_dict,
    raise_openai_validation_exhausted,
    responses_dict_has_usable_text,
    run_with_transport_retries,
    sleep_between_output_validation_attempts,
)
from app.logs.api_call_logger import log_api_call
from app.usage.request_cost_context import add_request_llm_cost_micro, is_request_llm_cost_tracking

T = TypeVar("T", bound=BaseModel)


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
        self._client = OpenAI(api_key=openai_api_key, max_retries=0)

    def _micro_usd_for_chat_completion(self, completion, model: str) -> int:
        """Return micro-USD cost for a chat completion from its usage fields."""
        inp, out, reasoning = extract_usage_from_chat_completion(completion)
        return compute_llm_cost_micro_usd(
            input_tokens=inp,
            output_tokens=out,
            reasoning_tokens=reasoning,
            model=model,
        )

    def _micro_usd_for_responses_dict(self, resp_dict: dict, model: str) -> int:
        """Return micro-USD cost for a Responses API payload from its usage fields."""
        inp, out, reasoning = extract_usage_from_response_dict(resp_dict)
        return compute_llm_cost_micro_usd(
            input_tokens=inp,
            output_tokens=out,
            reasoning_tokens=reasoning,
            model=model,
        )

    def _track_micro_usd(self, micro: int) -> None:
        """Accumulate micro-USD into request-level cost tracking when enabled."""
        if is_request_llm_cost_tracking():
            add_request_llm_cost_micro(micro)

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

    def _complete_schema_parse_attempt(
        self,
        *,
        model: str,
        messages: list,
        response_format: Type[T],
        temperature: float,
    ):
        """Run one structured chat parse with transport retries."""
        def _parse_once():
            return self._client.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_format,
                temperature=temperature,
            )

        return run_with_transport_retries(_parse_once)

    def _handle_schema_retryable_exc(self, val_i: int, exc: BaseException) -> None:
        """Raise validation exhaustion on last attempt; otherwise backoff before retry."""
        if val_i >= MAX_STRUCTURED_OUTPUT_ATTEMPTS - 1:
            raise_openai_validation_exhausted(exc)
        sleep_between_output_validation_attempts(val_i)

    def _finalize_schema_success(
        self,
        completion,
        *,
        model: str,
        parsed: T,
        developer_prompt: str,
        prompt: str,
    ) -> tuple[T, str]:
        """Log the call, record cost, and return the parsed model and message id."""
        message_id = getattr(completion, "id", None) or f"msg_{uuid.uuid4().hex}"
        input_tokens, output_tokens, _ = extract_usage_from_chat_completion(completion)
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
        last_exc: BaseException | None = None

        for val_i in range(MAX_STRUCTURED_OUTPUT_ATTEMPTS):
            try:
                completion = self._complete_schema_parse_attempt(
                    model=model,
                    messages=messages,
                    response_format=response_format,
                    temperature=temperature,
                )
            except (APIResponseValidationError, LengthFinishReasonError) as exc:
                last_exc = exc
                self._handle_schema_retryable_exc(val_i, exc)
                continue

            parsed = completion.choices[0].message.parsed
            if parsed is None:
                last_exc = RuntimeError("Structured chat completion returned no parsed content")
                if val_i >= MAX_STRUCTURED_OUTPUT_ATTEMPTS - 1:
                    raise_openai_validation_exhausted(last_exc)
                sleep_between_output_validation_attempts(val_i)
                continue

            return self._finalize_schema_success(
                completion,
                model=model,
                parsed=parsed,
                developer_prompt=developer_prompt,
                prompt=prompt,
            )

        raise_openai_validation_exhausted(last_exc)

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

    def _responses_create_dict(self, *, model: str, input_msgs: list, temperature: float) -> dict:
        """Call Responses API and return a dict, with transport retries."""
        def _responses_once():
            response = openai.responses.create(model=model, input=input_msgs, temperature=temperature)
            return response.to_dict()

        return run_with_transport_retries(_responses_once)

    def _finalize_generate_text_success(
        self, resp_dict: dict, *, model: str, developer_prompt: str, prompt: str
    ) -> dict:
        """Log the Responses call, record cost, and return the response dict."""
        input_tokens, output_tokens, _reasoning = extract_usage_from_response_dict(resp_dict)
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
        if not self.is_text_enabled:
            raise InternalAppError()

        input_msgs = [{"role": "developer", "content": developer_prompt}, {"role": "user", "content": prompt}]
        last_exc: BaseException | None = None

        for val_i in range(MAX_STRUCTURED_OUTPUT_ATTEMPTS):
            try:
                resp_dict = self._responses_create_dict(
                    model=model, input_msgs=input_msgs, temperature=temperature
                )
            except APIResponseValidationError as exc:
                last_exc = exc
                if val_i >= MAX_STRUCTURED_OUTPUT_ATTEMPTS - 1:
                    raise_openai_validation_exhausted(exc)
                sleep_between_output_validation_attempts(val_i)
                continue

            if responses_dict_has_usable_text(resp_dict):
                return self._finalize_generate_text_success(
                    resp_dict, model=model, developer_prompt=developer_prompt, prompt=prompt
                )

            last_exc = RuntimeError("Responses API returned no usable assistant text")
            if val_i >= MAX_STRUCTURED_OUTPUT_ATTEMPTS - 1:
                raise_openai_validation_exhausted(last_exc)
            sleep_between_output_validation_attempts(val_i)

        raise_openai_validation_exhausted(last_exc)

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

        def _fetch_stream_bytes() -> list[bytes]:
            chunks: list[bytes] = []
            with self._client.audio.speech.with_streaming_response.create(
                model=speech_model,
                voice=speech_voice,
                input=text,
                instructions=speech_instructions,
            ) as response:
                for chunk in response.iter_bytes():
                    chunks.append(chunk)
            return chunks

        chunk_list = run_with_transport_retries(_fetch_stream_bytes)
        for chunk in chunk_list:
            yield chunk
