from fastapi import APIRouter, Depends

from app.auth.auth_service import get_current_user_id
from app.query.query_service import QueryService
from app.dependency_injector import DependencyInjector

router = APIRouter()


@router.post("/query/get_user_query_response")
async def get_user_query_response(
    user_query: str,
    service: QueryService = Depends(DependencyInjector.get_query_service),
    user_id: str = Depends(get_current_user_id),
):
    return await service.get_user_query_response(user_query, user_id)
