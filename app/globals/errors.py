"""Central application exceptions; HTTP status and client-safe payloads are resolved in global handlers."""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Canonical error codes and copy (single source of truth for clients)
# ---------------------------------------------------------------------------

OPENAI_ACCOUNT_QUOTA_ERROR_CODE = "openai_account_quota"
OPENAI_ACCOUNT_QUOTA_MESSAGE = (
    "The AI provider account has insufficient quota or billing. "
    "The service cannot complete AI requests until provider billing is fixed."
)

USER_USAGE_LIMIT_ERROR_CODE = "user_usage_limit_exceeded"
USER_USAGE_LIMIT_MESSAGE = (
    "Your AI usage limit for this period has been reached. Try again after the reset time."
)


class AppError(Exception):
    """
    Base class for API errors.

    ``detail`` is returned inside the standard JSON envelope under ``error`` (string becomes
    ``message``, or dict merges with ``code`` / ``message`` / optional fields).
    """

    status_code: int = 500
    error_code: str = "internal_error"
    default_detail: str | dict[str, Any] = "An unexpected error occurred. Please try again later."

    def __init__(self, detail: str | dict[str, Any] | None = None) -> None:
        self.detail: str | dict[str, Any] = detail if detail is not None else self.default_detail
        super().__init__(self.detail if isinstance(self.detail, str) else "AppError")


class BadRequestError(AppError):
    """Malformed input, invalid ids, or failed request validation."""

    status_code = 400
    error_code = "bad_request"
    default_detail = "The request could not be completed."


class AuthenticationError(AppError):
    """Missing or invalid credentials (JWT, refresh token, or upstream identity)."""

    status_code = 401
    error_code = "authentication_failed"
    default_detail = "Authentication failed."


class ForbiddenError(AppError):
    """Authenticated caller is not allowed to access the resource."""

    status_code = 403
    error_code = "forbidden"
    default_detail = "Access denied."


class NotFoundError(AppError):
    """Resource does not exist or is not visible to the caller."""

    status_code = 404
    error_code = "not_found"
    default_detail = "The requested resource was not found."


class ConflictError(AppError):
    """State conflict such as a duplicate unique key."""

    status_code = 409
    error_code = "conflict"
    default_detail = "This resource already exists."


class LlmBudgetExceededError(AppError):
    """
    User's configured LLM spend / usage cap for the window has been reached.

    Same semantics everywhere: use ``enforce_user_llm_budget`` (``usage/helpers``).
    """

    status_code = 429
    error_code = USER_USAGE_LIMIT_ERROR_CODE

    def __init__(self, *, renews_on: str | None, limit_usd: float) -> None:
        super().__init__(
            {
                "code": USER_USAGE_LIMIT_ERROR_CODE,
                "message": USER_USAGE_LIMIT_MESSAGE,
                "renews_on": renews_on,
                "limit_usd": limit_usd,
            }
        )


class AIDependencyError(AppError):
    """Upstream AI provider (e.g. OpenAI) failed or is unreachable."""

    status_code = 503
    error_code = "ai_dependency_unavailable"
    default_detail = "The AI assistant is temporarily unavailable. Please try again later."


class OpenAIAccountQuotaError(AppError):
    """
    OpenAI rejected the call for billing, quota, or insufficient provider credits.

    Raised only via ``OpenAIClient`` / ``openai_policy`` so all LLM paths share this behavior.
    """

    status_code = 503
    error_code = OPENAI_ACCOUNT_QUOTA_ERROR_CODE

    def __init__(self) -> None:
        super().__init__(
            {
                "code": OPENAI_ACCOUNT_QUOTA_ERROR_CODE,
                "message": OPENAI_ACCOUNT_QUOTA_MESSAGE,
            }
        )


class DatabaseOperationError(AppError):
    """Unexpected persistence failure after validation."""

    status_code = 500
    error_code = "database_error"
    default_detail = "A data error occurred. Please try again later."


class InternalAppError(AppError):
    """Unexpected server-side failure not attributed to a specific subsystem."""

    status_code = 500
    error_code = "internal_error"
    default_detail = "An unexpected error occurred. Please try again later."
