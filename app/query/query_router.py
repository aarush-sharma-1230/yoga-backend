from fastapi import APIRouter, Depends, Request
from app.query.query_service import QueryService
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException

router = APIRouter()


@router.post("/query/get_user_query_response")
async def get_user_query_response(user_query, service: QueryService = Depends(DependencyInjector.get_query_service)):
  try:
    response = await service.get_user_query_response(user_query)
    return response

  except Exception:
    raise CustomException()
