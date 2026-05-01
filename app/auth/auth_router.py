"""Authentication routes: Google OIDC, refresh cookie rotation, and user profile APIs."""

import jwt
from bson.errors import InvalidId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response, status
from pymongo.errors import DuplicateKeyError

from app.auth.auth_service import AuthService, get_current_user_id
from app.auth.jwt_middleware import jwt_access_payload
from app.auth.helpers import set_refresh_cookie
from app.auth.settings import get_auth_settings
from app.schemas.auth import (CreateUser, GoogleLoginRequest, HardPriorityStrategy, MediumPriorityStrategy)
from app.dependency_injector import DependencyInjector

router = APIRouter()


def _http_detail_for_status(status_code: int) -> str:
    """Generic client-facing message for an HTTP status code."""

    if status_code == 401:
        return "Authentication failed."
    if status_code == 403:
        return "Access denied."
    if status_code == 404:
        return "The requested resource was not found."
    if status_code == 409:
        return "This resource already exists."
    if 400 <= status_code < 500:
        return "The request could not be completed."
    return "An unexpected error occurred. Please try again later."


def _map_auth_route_exception(
    exc: Exception,
    *,
    value_error_as_unauthorized: bool = False,
) -> HTTPException:
    """Map raised exceptions to HTTP responses with generic messages."""

    if isinstance(exc, HTTPException):
        return HTTPException(
            status_code=exc.status_code,
            detail=_http_detail_for_status(exc.status_code),
        )
    if isinstance(exc, jwt.PyJWTError):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_http_detail_for_status(401),
        )
    if isinstance(exc, ValueError):
        code = (
            status.HTTP_401_UNAUTHORIZED
            if value_error_as_unauthorized
            else status.HTTP_400_BAD_REQUEST
        )
        return HTTPException(status_code=code, detail=_http_detail_for_status(code))
    if isinstance(exc, InvalidId):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_http_detail_for_status(400),
        )
    if isinstance(exc, DuplicateKeyError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=_http_detail_for_status(409),
        )
    if isinstance(exc, RuntimeError):
        if "not found" in str(exc).lower():
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=_http_detail_for_status(404),
            )
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_http_detail_for_status(500),
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=_http_detail_for_status(500),
    )


@router.post("/auth/google")
async def login_with_google(
    body: GoogleLoginRequest,
    response: Response,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Verify Google ID token, set refresh cookie, return access JWT JSON."""

    try:
        out = await service.sign_in_with_google(body.id_token)
        set_refresh_cookie(response, out["refresh_token_raw"], get_auth_settings())
        return {"access_token": out["access_token"]}
    except Exception as exc:
        raise _map_auth_route_exception(exc, value_error_as_unauthorized=True) from exc


@router.post("/auth/refresh")
async def refresh_session(
    request: Request,
    response: Response,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Rotate refresh cookie and return new access JWT JSON."""

    try:
        settings = get_auth_settings()
        raw = request.cookies.get(settings.refresh_cookie_name)
        out = await service.refresh_session(raw)
        if not out:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="placeholder",
            )
        set_refresh_cookie(response, out["refresh_token_raw"], settings)
        return {"access_token": out["access_token"], "token_type": "bearer"}
    except Exception as exc:
        raise _map_auth_route_exception(exc) from exc


@router.post("/user/user_registration")
async def user_registration(
    user: CreateUser,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    try:
        return await service.create_user(user)
    except Exception as exc:
        raise _map_auth_route_exception(exc) from exc


@router.post("/user/get_user_data")
async def get_user_data(
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    jwt_payload: dict = Depends(jwt_access_payload),
):
    """Return profile subset for the authenticated user (user id from access JWT only)."""

    try:
        user_id = str(jwt_payload["_id"])
        return await service.get_user_data(user_id)
    except Exception as exc:
        raise _map_auth_route_exception(exc) from exc


@router.post("/user/profile/hard_priority")
async def save_hard_priority_strategy(
    strategy: HardPriorityStrategy,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user_id: str = Depends(get_current_user_id),
):
    """Save medical / safety (hard priority) strategy; LLM hard summary is generated in the background."""

    try:
        result = await service.save_hard_priority_strategy(user_id=user_id, strategy=strategy)
        background_tasks.add_task(
            service.generate_hard_summary_and_update_profile,
            user_id,
            strategy.model_dump(),
        )
        return result
    except Exception as exc:
        raise _map_auth_route_exception(exc) from exc


@router.post("/user/profile/medium_priority")
async def save_medium_priority_strategy(
    strategy: MediumPriorityStrategy,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user_id: str = Depends(get_current_user_id),
):
    """Save goals / experience (medium priority) strategy; LLM medium summary is generated in the background."""

    try:
        result = await service.save_medium_priority_strategy(user_id=user_id, strategy=strategy)
        background_tasks.add_task(
            service.generate_medium_summary_and_update_profile,
            user_id,
            strategy.model_dump(),
        )
        return result
    except Exception as exc:
        raise _map_auth_route_exception(exc) from exc


@router.get("/user/profile")
async def get_profile(
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user_id: str = Depends(get_current_user_id),
):
    """Fetch user profile. Returns MongoDB document structure."""

    try:
        return await service.get_profile(user_id=user_id)
    except Exception as exc:
        raise _map_auth_route_exception(exc) from exc
