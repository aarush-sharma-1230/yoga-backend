"""Central application exceptions; HTTP status and client-safe payloads are resolved in global handlers."""

from __future__ import annotations

from typing import Any


class AppError(Exception):
    """
    Base class for API errors.

    ``detail`` is returned as the JSON ``detail`` field (string or structured dict).
    """

    status_code: int = 500
    default_detail: str | dict[str, Any] = "An unexpected error occurred. Please try again later."

    def __init__(self, detail: str | dict[str, Any] | None = None) -> None:
        self.detail: str | dict[str, Any] = detail if detail is not None else self.default_detail
        super().__init__(self.detail if isinstance(self.detail, str) else "AppError")


class BadRequestError(AppError):
    """Malformed input, invalid ids, or failed request validation."""

    status_code = 400
    default_detail = "The request could not be completed."


class AuthenticationError(AppError):
    """Missing or invalid credentials (JWT, refresh token, or upstream identity)."""

    status_code = 401
    default_detail = "Authentication failed."


class ForbiddenError(AppError):
    """Authenticated caller is not allowed to access the resource."""

    status_code = 403
    default_detail = "Access denied."


class NotFoundError(AppError):
    """Resource does not exist or is not visible to the caller."""

    status_code = 404
    default_detail = "The requested resource was not found."


class ConflictError(AppError):
    """State conflict such as a duplicate unique key."""

    status_code = 409
    default_detail = "This resource already exists."


class AccessTokenTooShortLifetimeError(AppError):
    """Bearer token expires before the minimum required for the operation."""

    status_code = 409

    def __init__(self) -> None:
        super().__init__(
            {
                "code": "access_token_expiring",
                "message": "Access token does not have enough lifetime left; refresh before starting a session.",
            }
        )


class LlmBudgetExceededError(AppError):
    """Rolling-window LLM spend cap reached for the user."""

    status_code = 429

    def __init__(self, *, renews_on: str | None, limit_usd: float) -> None:
        super().__init__(
            {
                "code": "llm_daily_cap",
                "message": "Daily LLM usage limit reached. Try again after the reset time.",
                "renews_on": renews_on,
                "limit_usd": limit_usd,
            }
        )


class AIDependencyError(AppError):
    """Upstream AI provider (e.g. OpenAI) failed or is unreachable."""

    status_code = 503
    default_detail = "The AI assistant is temporarily unavailable. Please try again later."


class DatabaseOperationError(AppError):
    """Unexpected persistence failure after validation."""

    status_code = 500
    default_detail = "A data error occurred. Please try again later."


class InternalAppError(AppError):
    """Unexpected server-side failure not attributed to a specific subsystem."""

    status_code = 500
    default_detail = "An unexpected error occurred. Please try again later."
