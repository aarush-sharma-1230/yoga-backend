from fastapi import APIRouter, BackgroundTasks, Depends
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


USER_ID_TEMP = "67d5632a3a9bdddef290e127"


@router.post("/user/profile")
async def save_profile(
    profile: UserProfilePayload,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Save user profile for personalized yoga sessions. Summaries are generated in background."""
    try:
        result = await service.save_profile(user_id=USER_ID_TEMP, profile=profile)
        background_tasks.add_task(
            service.generate_summaries_and_update_profile,
            USER_ID_TEMP,
            profile.hard_priority_strategy.model_dump(),
            profile.medium_priority_strategy.model_dump(),
        )
        return result
    except Exception as e:
        raise CustomException(str(e))


@router.get("/user/profile")
async def get_profile(service: AuthService = Depends(DependencyInjector.get_auth_service)):
    """Fetch user profile. Returns MongoDB document structure."""
    try:
        return await service.get_profile(user_id=USER_ID_TEMP)
    except RuntimeError as e:
        if "not found" in str(e).lower():
            raise CustomException(str(e))
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(str(e))
