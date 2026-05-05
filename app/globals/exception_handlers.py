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

from app.globals.errors import AppError

logger = logging.getLogger(__name__)


def _init_sentry() -> None:
    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        return
    traces = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0") or "0")
    sentry_sdk.init(dsn=dsn, traces_sample_rate=traces, send_default_pii=False)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach global handlers for AppError, common infrastructure errors, and a final catch-all."""

    _init_sentry()

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        if exc.status_code == 401:
            public = "Authentication failed."
        elif exc.status_code == 403:
            public = "Access denied."
        elif exc.status_code == 404:
            public = "The requested resource was not found."
        elif exc.status_code == 409:
            public = "This resource already exists."
        elif 400 <= exc.status_code < 500:
            public = "The request could not be completed."
        else:
            public = "An unexpected error occurred. Please try again later."
        return JSONResponse(status_code=exc.status_code, content={"detail": public})

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        return JSONResponse(
            status_code=422,
            content={"detail": "The request data is invalid."},
        )

    @app.exception_handler(jwt.PyJWTError)
    async def jwt_handler(request: Request, exc: jwt.PyJWTError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication failed."},
        )

    @app.exception_handler(InvalidId)
    async def invalid_object_id_handler(request: Request, exc: InvalidId) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        return JSONResponse(
            status_code=400,
            content={"detail": "The request could not be completed."},
        )

    @app.exception_handler(DuplicateKeyError)
    async def duplicate_key_handler(request: Request, exc: DuplicateKeyError) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        return JSONResponse(
            status_code=409,
            content={"detail": "This resource already exists."},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        sentry_sdk.capture_exception(exc)
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please try again later."},
        )
