from fastapi import APIRouter, Depends, Request
from app.auth.auth_service import AuthService
from app.dependency_injector import DependencyInjector
from app.auth.auth_interfaces import CreateUser, GetUserData, UserProfilePayload
from app.globals.errors import CustomException

router = APIRouter()


@router.post("/user/user_registration")
async def user_registration(user: CreateUser, service: AuthService = Depends(DependencyInjector.get_auth_service)):
    try:
        return await service.create_user(user)

    except Exception:
        raise CustomException()


@router.post("/user/get_user_data")
async def get_user_data(user_data: GetUserData, service: AuthService = Depends(DependencyInjector.get_auth_service)):
    try:
        response = await service.get_user_data(user_data)
        return response

    except Exception:
        raise CustomException()


@router.post("/user/profile")
async def save_profile(
    profile: UserProfilePayload, service: AuthService = Depends(DependencyInjector.get_auth_service)
):
    """Save user profile for personalized yoga sessions."""
    try:
        user_id = "67d5632a3a9bdddef290e127"
        return await service.save_profile(user_id=user_id, profile=profile)
    except Exception as e:
        raise CustomException(str(e))
