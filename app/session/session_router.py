from fastapi import APIRouter, Depends, Request
from app.session.session_service import SessionService
from app.session.session_interfaces import SeriesData
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from bson import ObjectId

router = APIRouter()


@router.post("/query/start_user_session")
async def start_user_session(series_data: SeriesData, service: SessionService = Depends(DependencyInjector.get_session_service)):
  try:
    sequence_id = series_data.sequence_id
    user_id = ObjectId("67d5632a3a9bdddef290e127")
    response = await service.start_user_session(user_id=user_id, sequence_id=sequence_id)
    return response

  except ValueError as e:
    raise CustomException(e)

  except RuntimeError as e:
    raise CustomException(e)

  except Exception as e:
    raise CustomException(e)
