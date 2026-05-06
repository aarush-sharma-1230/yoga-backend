"""Register FastAPI exception handlers: Sentry reporting and consistent JSON error bodies."""

from __future__ import annotations

import logging
import os

import jwt
import sentry_sdk
from bson.errors import InvalidId
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.globals.error_payload import error_envelope, json_response_for_app_error
from app.globals.errors import AppError, OpenAIAccountQuotaError

logger = logging.getLogger(__name__)


def _init_sentry() -> None:
    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        return
    traces = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0") or "0")
    sentry_sdk.init(dsn=dsn, traces_sample_rate=traces, send_default_pii=False)


def _http_exception_code(status_code: int) -> str:
    """Map HTTP status to a stable machine-readable error code."""
    return {
        400: "bad_request",
        401: "authentication_failed",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
        429: "too_many_requests",
        503: "service_unavailable",
    }.get(status_code, f"http_{status_code}")


def register_exception_handlers(app: FastAPI) -> None:
    """Attach global handlers for AppError, common infrastructure errors, and a final catch-all."""

    _init_sentry()

    @app.exception_handler(OpenAIAccountQuotaError)
    async def openai_account_quota_handler(request: Request, exc: OpenAIAccountQuotaError) -> JSONResponse:
        """Provider billing/quota: same JSON shape as other errors; omit Sentry (operator-side)."""
        return json_response_for_app_error(exc)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        return json_response_for_app_error(exc)

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        code = _http_exception_code(exc.status_code)
        if isinstance(exc.detail, dict):
            inner = dict(exc.detail)
            inner.setdefault("code", code)
            inner.setdefault("message", str(inner.get("message", "Request failed.")))
            body = {"error": inner}
        elif isinstance(exc.detail, str):
            body = error_envelope(code=code, message=exc.detail)
        else:
            body = error_envelope(code=code, message="Request failed.")
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        issues = [{"loc": list(err.get("loc", ())), "msg": err.get("msg", "")} for err in exc.errors()]
        body = error_envelope(
            code="validation_error",
            message="The request data is invalid.",
            validation_issues=issues,
        )
        return JSONResponse(status_code=422, content=body)

    @app.exception_handler(jwt.PyJWTError)
    async def jwt_handler(request: Request, exc: jwt.PyJWTError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        body = error_envelope(code="authentication_failed", message="Authentication failed.")
        return JSONResponse(status_code=401, content=body)

    @app.exception_handler(InvalidId)
    async def invalid_object_id_handler(request: Request, exc: InvalidId) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        body = error_envelope(code="bad_request", message="The request could not be completed.")
        return JSONResponse(status_code=400, content=body)

    @app.exception_handler(DuplicateKeyError)
    async def duplicate_key_handler(request: Request, exc: DuplicateKeyError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        body = error_envelope(code="conflict", message="This resource already exists.")
        return JSONResponse(status_code=409, content=body)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        logger.exception("Unhandled exception", exc_info=exc)
        body = error_envelope(code="internal_error", message="An unexpected error occurred. Please try again later.")
        return JSONResponse(status_code=500, content=body)
