"""Authentication routes: Google OIDC, refresh cookie rotation, and user profile APIs."""

from fastapi import APIRouter, Depends, Request, Response

from app.auth.auth_service import AuthService
from app.auth.helpers import set_refresh_cookie
from app.auth.settings import get_auth_settings
from app.middlewares.auth import get_current_user
from app.schemas.auth import GoogleLoginRequest, UserGoals, UserMedicalProfile
from app.dependency_injector import DependencyInjector

router = APIRouter()


def _public_user_subset(user: dict) -> dict:
    """Shape returned by legacy ``get_user_data`` / ``get_profile`` endpoints (projection-aligned)."""

    return {
        "_id": str(user["_id"]),
        "full_name": user.get("full_name"),
        "email": user.get("email"),
        "profile": user.get("profile"),
    }


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
async def get_user_data(user: dict = Depends(get_current_user)):
    """Return profile subset for the authenticated user (single DB load via ``get_current_user``)."""

    return {"status": True, "user": _public_user_subset(user)}


@router.post("/user/profile/medical_profile")
async def save_user_medical_profile(
    profile: UserMedicalProfile,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user: dict = Depends(get_current_user),
):
    """Persist user medical profile and regenerate its LLM summary in one request."""

    return await service.save_user_medical_profile(user_id=str(user["_id"]), profile=profile)


@router.post("/user/profile/goals")
async def save_user_goals(
    goals: UserGoals,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
    user: dict = Depends(get_current_user),
):
    """Persist user goals (experience, activity, primary goals) and regenerate their LLM summary."""

    return await service.save_user_goals(user_id=str(user["_id"]), goals=goals)


@router.get("/user/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    """Same payload as ``POST /user/get_user_data`` without a second database round-trip."""

    return {"status": True, "user": _public_user_subset(user)}
