from fastapi import APIRouter, BackgroundTasks, Depends

from app.auth.auth_service import AuthService
from app.schemas.auth import CreateUser, GetUserData, HardPriorityStrategy, MediumPriorityStrategy
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException

router = APIRouter()

USER_ID_TEMP = "67d5632a3a9bdddef290e127"


@router.post("/user/user_registration")
async def user_registration(user: CreateUser, service: AuthService = Depends(DependencyInjector.get_auth_service)):
    try:
        return await service.create_user(user)

    except Exception:
        raise CustomException()


@router.post("/user/get_user_data")
async def get_user_data(
    user_data: GetUserData,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Request body is validated; response uses the configured temp user id until auth is wired."""
    _ = user_data
    try:
        lookup = GetUserData(user_id=USER_ID_TEMP)
        return await service.get_user_data(lookup)

    except Exception:
        raise CustomException()


@router.post("/user/profile/hard_priority")
async def save_hard_priority_strategy(
    strategy: HardPriorityStrategy,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Save medical / safety (hard priority) strategy; LLM hard summary is generated in the background."""
    try:
        result = await service.save_hard_priority_strategy(user_id=USER_ID_TEMP, strategy=strategy)
        background_tasks.add_task(
            service.generate_hard_summary_and_update_profile,
            USER_ID_TEMP,
            strategy.model_dump(),
        )
        return result
    except Exception as e:
        raise CustomException(str(e))


@router.post("/user/profile/medium_priority")
async def save_medium_priority_strategy(
    strategy: MediumPriorityStrategy,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """Save goals / experience (medium priority) strategy; LLM medium summary is generated in the background."""
    try:
        result = await service.save_medium_priority_strategy(user_id=USER_ID_TEMP, strategy=strategy)
        background_tasks.add_task(
            service.generate_medium_summary_and_update_profile,
            USER_ID_TEMP,
            strategy.model_dump(),
        )
        return result
    except Exception as e:
        raise CustomException(str(e))


@router.get("/user/profile")
async def get_profile(service: AuthService = Depends(DependencyInjector.get_auth_service)):
    """Fetch user profile. Returns MongoDB document structure."""
    try:
        return await service.get_profile(user_id=USER_ID_TEMP)
    except Exception as e:
        raise CustomException(str(e))
