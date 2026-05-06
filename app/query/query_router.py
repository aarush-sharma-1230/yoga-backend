from fastapi import APIRouter, Depends

from app.auth.auth_service import get_current_user_id
from app.auth.settings import get_auth_settings
from app.query.query_service import QueryService
from app.dependency_injector import DependencyInjector
from app.usage.constants import config_usd_to_micro_usd
from app.usage.helpers import UserBudgetAccess, enforce_user_llm_budget, get_user_budget_access

router = APIRouter()


@router.post("/query/get_user_query_response")
async def get_user_query_response(
    user_query: str,
    service: QueryService = Depends(DependencyInjector.get_query_service),
    access: UserBudgetAccess = Depends(get_user_budget_access),
):
    settings = get_auth_settings()
    cap_micro = config_usd_to_micro_usd(settings.user_daily_llm_usd_cap)
    enforce_user_llm_budget(
        llm_cost=access.llm_cost,
        cap_micro_usd=cap_micro,
        limit_usd=settings.user_daily_llm_usd_cap,
    )
    return await service.get_user_query_response(user_query, access.user_id)
