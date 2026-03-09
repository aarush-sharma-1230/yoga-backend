from fastapi import APIRouter, Depends, Request
from app.auth.auth_service import AuthService
from app.dependency_injector import DependencyInjector
from app.auth.auth_interfaces import CreateUser, GetUserData
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
