"""
OpenAI error classification, retries, usage/cost helpers, and TTS defaults used by ``OpenAIClient``.

Call sites run in worker threads (``asyncio.to_thread``), so retries use ``time.sleep``.
"""

from __future__ import annotations

import random
import time
from typing import Any, Callable, TypeVar

from openai import (
    APIConnectionError,
    APIError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    LengthFinishReasonError,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
)

from app.globals.errors import AIDependencyError, OpenAIAccountQuotaError
from app.usage import constants

T = TypeVar("T")

MAX_TRANSPORT_ATTEMPTS = 5
MAX_STRUCTURED_OUTPUT_ATTEMPTS = 3
BASE_DELAY_SEC = 0.5
MAX_SINGLE_SLEEP_SEC = 15.0

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
    r_reas = (
        reasoning_usd_per_million
        if reasoning_usd_per_million is not None
        else constants.REASONING_USD_PER_MILLION_TOKENS
    )
    inp = int(input_tokens or 0)
    out = int(output_tokens or 0)
    reas = int(reasoning_tokens or 0)
    total_micro = inp * r_in + out * r_out + reas * r_reas
    return int(round(total_micro))


def extract_usage_from_chat_completion(completion: Any) -> tuple[int | None, int | None, int | None]:
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


def extract_usage_from_response_dict(resp_dict: dict) -> tuple[int | None, int | None, int | None]:
    """Extract input, output, and optional reasoning token counts from a Responses API response dict."""
    usage = resp_dict.get("usage") or (resp_dict.get("output") or [{}])[0].get("usage")
    if not isinstance(usage, dict):
        return (None, None, None)
    input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens")
    output_tokens = usage.get("output_tokens") or usage.get("completion_tokens")
    reasoning = usage.get("reasoning_tokens")
    return (input_tokens, output_tokens, reasoning)


def raise_openai_validation_exhausted(cause: BaseException | None = None) -> None:
    """Raise the standard error when structured or text output retries are exhausted."""
    err = AIDependencyError(
        detail={
            "code": "openai_validation_exhausted",
            "message": "The AI assistant returned an unexpected response. Please try again later.",
        }
    )
    if cause is not None:
        raise err from cause
    raise err


def is_openai_account_quota_failure(exc: BaseException) -> bool:
    """Return True when OpenAI rejects the call for billing, quota, or insufficient credits."""
    if isinstance(exc, APIStatusError) and getattr(exc, "status_code", None) == 402:
        return True
    if isinstance(exc, RateLimitError):
        code = getattr(exc, "code", None)
        if code == "insufficient_quota":
            return True
        body = getattr(exc, "body", None)
        if isinstance(body, dict):
            nested = body.get("error")
            if isinstance(nested, dict) and nested.get("code") == "insufficient_quota":
                return True
    return False


def _retry_after_seconds(exc: BaseException) -> float | None:
    if not isinstance(exc, APIStatusError):
        return None
    raw = exc.response.headers.get("retry-after")
    if not raw:
        return None
    try:
        return min(float(raw), 120.0)
    except ValueError:
        return None


def is_transport_retryable(exc: BaseException) -> bool:
    """Connection, timeout, upstream 5xx, or non-quota 429."""
    if isinstance(exc, (APIConnectionError, APITimeoutError)):
        return True
    if isinstance(exc, InternalServerError):
        return True
    if isinstance(exc, RateLimitError):
        return not is_openai_account_quota_failure(exc)
    return False


def _backoff_sleep(attempt_index: int, *, retry_after: float | None) -> None:
    if retry_after is not None:
        time.sleep(min(retry_after, MAX_SINGLE_SLEEP_SEC))
        return
    base = BASE_DELAY_SEC * (2**attempt_index)
    jitter = random.random() * 0.25 * base
    time.sleep(min(base + jitter, MAX_SINGLE_SLEEP_SEC))


def run_with_transport_retries(fn: Callable[[], T]) -> T:
    """
    Run a synchronous OpenAI call with retries for transient transport and rate issues.

    Fails fast with ``OpenAIAccountQuotaError`` when the provider rejects the call for
    quota or billing. Exhaustion raises ``AIDependencyError`` with code ``openai_retries_exhausted``.
    """
    last_exc: BaseException | None = None
    for attempt in range(MAX_TRANSPORT_ATTEMPTS):
        try:
            return fn()
        except OpenAIAccountQuotaError:
            raise
        except Exception as exc:
            last_exc = exc
            if is_openai_account_quota_failure(exc):
                raise OpenAIAccountQuotaError() from exc
            if isinstance(exc, AuthenticationError):
                raise AIDependencyError(
                    detail={
                        "code": "openai_auth",
                        "message": "The AI assistant is temporarily unavailable. Please try again later.",
                    }
                ) from exc
            if isinstance(exc, PermissionDeniedError):
                raise AIDependencyError(
                    detail={
                        "code": "openai_permission_denied",
                        "message": "The AI assistant is temporarily unavailable. Please try again later.",
                    }
                ) from exc
            if isinstance(exc, BadRequestError):
                raise AIDependencyError(
                    detail={
                        "code": "openai_bad_request",
                        "message": "The AI assistant could not process this request.",
                    }
                ) from exc
            if isinstance(exc, APIResponseValidationError):
                raise
            if isinstance(exc, LengthFinishReasonError):
                raise
            if is_transport_retryable(exc):
                if attempt >= MAX_TRANSPORT_ATTEMPTS - 1:
                    break
                ra = _retry_after_seconds(exc)
                _backoff_sleep(attempt, retry_after=ra)
                continue
            if isinstance(exc, APIError):
                raise AIDependencyError() from exc
            if isinstance(exc, OpenAIError):
                raise AIDependencyError() from exc
            raise

    raise AIDependencyError(
        detail={
            "code": "openai_retries_exhausted",
            "message": "The AI assistant is temporarily unavailable. Please try again later.",
        }
    ) from last_exc


def responses_dict_has_usable_text(resp_dict: dict) -> bool:
    """Return False when the Responses API payload has no non-empty assistant text."""
    output = resp_dict.get("output") or []
    if not output:
        return False
    first = output[0]
    content = first.get("content") if isinstance(first, dict) else None
    if not content:
        return False
    block = content[0] if isinstance(content, list) else None
    if not isinstance(block, dict):
        return False
    text = block.get("text")
    return isinstance(text, str) and bool(text.strip())


def sleep_between_output_validation_attempts(attempt_index: int) -> None:
    """Backoff between full LLM retries when structured or text output is invalid."""
    base = BASE_DELAY_SEC * (2**attempt_index)
    jitter = random.random() * 0.25 * base
    time.sleep(min(base + jitter, MAX_SINGLE_SLEEP_SEC))
