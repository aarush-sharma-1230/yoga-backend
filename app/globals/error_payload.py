"""
Standard JSON error bodies for API responses.

Shape follows common production conventions (similar to Stripe/GitHub): a single top-level
``error`` object with machine-readable ``code``, human ``message``, and optional extra fields.
HTTP status is carried by the response status line; the body does not duplicate it.
"""

from __future__ import annotations

from typing import Any

from fastapi.responses import JSONResponse

from app.globals.errors import AppError


def error_envelope(*, code: str, message: str, **extra: Any) -> dict[str, Any]:
    """
    Build the canonical ``{"error": {...}}`` payload.

    Extra keyword arguments are merged into the inner object when values are not ``None``.
    """
    inner: dict[str, Any] = {"code": code, "message": message}
    for key, value in extra.items():
        if value is not None:
            inner[key] = value
    return {"error": inner}


def _fallback_message(exc: AppError) -> str:
    raw = getattr(exc, "default_detail", "An error occurred.")
    if isinstance(raw, dict):
        return str(raw.get("message", "An error occurred."))
    return str(raw)


def app_error_to_body(exc: AppError) -> dict[str, Any]:
    """
    Serialize an ``AppError`` into the standard envelope.

    If ``detail`` is already a dict (typically ``code``, ``message``, plus optional fields),
    those keys populate the inner ``error`` object, with class ``error_code`` as fallback
    for missing ``code``.
    """
    fallback_code = getattr(exc, "error_code", "internal_error")

    detail = exc.detail
    if isinstance(detail, dict):
        inner: dict[str, Any] = dict(detail)
        inner.setdefault("code", fallback_code)
        inner.setdefault("message", _fallback_message(exc))
        return {"error": inner}
    return error_envelope(code=fallback_code, message=str(detail))


def json_response_for_app_error(exc: AppError) -> JSONResponse:
    """Return a ``JSONResponse`` with status from the exception and the standard body."""
    return JSONResponse(status_code=exc.status_code, content=app_error_to_body(exc))
