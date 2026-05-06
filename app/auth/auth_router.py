"""Authentication routes: Google OIDC, refresh cookie rotation, and user profile APIs."""

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response

from app.auth.auth_service import AuthService, get_current_user_id
from app.auth.jwt_middleware import jwt_access_payload
from app.auth.helpers import set_refresh_cookie
from app.auth.settings import get_auth_settings
from app.schemas.auth import GoogleLoginRequest, HardPriorityStrategy, MediumPriorityStrategy
from app.dependency_injector import DependencyInjector

router = APIRouter()


@router.post("/auth/google")
async def login_with_google(
    body: GoogleLoginRequest,
    response: Response,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Verify Google ID token, set refresh cookie, return access JWT JSON."""

    out = await service.sign_in_with_google(body.id_token)
    set_refresh_cookie(response, out["refresh_token_raw"], get_auth_settings())
    return {"access_token": out["access_token"]}


@router.post("/auth/refresh")
async def refresh_session(
    request: Request,
    response: Response,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Rotate refresh cookie and return new access JWT JSON."""

    settings = get_auth_settings()
    raw = request.cookies.get(settings.refresh_cookie_name)
    out = await service.refresh_session(raw)
    set_refresh_cookie(response, out["refresh_token_raw"], settings)
    return {"access_token": out["access_token"]}


@router.post("/user/get_user_data")
async def get_user_data(
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    jwt_payload: dict = Depends(jwt_access_payload),
):
    """Return profile subset for the authenticated user (user id from access JWT only)."""

    user_id = str(jwt_payload["_id"])
    return await service.get_user_data(user_id)


@router.post("/user/profile/hard_priority")
async def save_hard_priority_strategy(
    strategy: HardPriorityStrategy,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user_id: str = Depends(get_current_user_id),
):
    """Save medical / safety (hard priority) strategy; LLM hard summary is generated in the background."""

    result = await service.save_hard_priority_strategy(user_id=user_id, strategy=strategy)
    background_tasks.add_task(
        service.generate_hard_summary_and_update_profile,
        user_id,
        strategy.model_dump(),
    )
    return result


@router.post("/user/profile/medium_priority")
async def save_medium_priority_strategy(
    strategy: MediumPriorityStrategy,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user_id: str = Depends(get_current_user_id),
):
    """Save goals / experience (medium priority) strategy; LLM medium summary is generated in the background."""

    result = await service.save_medium_priority_strategy(user_id=user_id, strategy=strategy)
    background_tasks.add_task(
        service.generate_medium_summary_and_update_profile,
        user_id,
        strategy.model_dump(),
    )
    return result


@router.get("/user/profile")
async def get_profile(
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user_id: str = Depends(get_current_user_id),
):
    """Fetch user profile. Returns MongoDB document structure."""

    return await service.get_profile(user_id=user_id)
