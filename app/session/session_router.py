from fastapi import APIRouter, Depends, Request
from app.session.session_service import SessionService
from app.session.session_interfaces import SeriesData
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from bson import ObjectId

router = APIRouter()


@router.post("/session/start")
async def start_user_session(
    series_data: SeriesData, service: SessionService = Depends(DependencyInjector.get_session_service)
):
    """
    Start a new yoga session.
    Pre-generates all guidance texts (intro, transitions, ending) and stores them in the session document.
    """
    try:
        sequence_id = series_data.sequence_id
        user_id = ObjectId("67d5632a3a9bdddef290e127")  # TODO: Get from authentication
        response = await service.start_user_session(user_id=user_id, sequence_id=sequence_id)
        return response

    except ValueError as e:
        raise CustomException(str(e))

    except RuntimeError as e:
        raise CustomException(str(e))

    except Exception as e:
        raise CustomException(str(e))
