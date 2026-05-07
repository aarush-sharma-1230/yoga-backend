from fastapi import APIRouter, Depends

from app.auth.settings import get_auth_settings
from app.middlewares.auth import get_current_user
from app.query.query_service import QueryService
from app.dependency_injector import DependencyInjector
from app.usage.constants import config_usd_to_micro_usd
from app.usage.helpers import enforce_user_llm_budget

router = APIRouter()


@router.post("/query/get_user_query_response")
async def get_user_query_response(
    user_query: str,
    service: QueryService = Depends(DependencyInjector.get_query_service),
    user: dict = Depends(get_current_user),
):
    settings = get_auth_settings()
    cap_micro = config_usd_to_micro_usd(settings.user_daily_llm_usd_cap)
    enforce_user_llm_budget(
        llm_cost=user.get("llm_cost"),
        cap_micro_usd=cap_micro,
        limit_usd=settings.user_daily_llm_usd_cap,
    )
    return await service.get_user_query_response(user_query, str(user["_id"]))
