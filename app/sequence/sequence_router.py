from fastapi import APIRouter, Depends, Request

from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from app.sequence.sequence_interface import CreateCustomSequenceData, SequenceData
from app.sequence.sequence_service import SequenceService

router = APIRouter()


@router.post("/sequence/get_sequences")
async def get_sequences(service: SequenceService = Depends(DependencyInjector.get_sequence_service)):
    try:
        response = await service.get_sequences()
        return response

    except Exception as e:
        raise CustomException(e)


@router.post("/sequence/get_sequence")
async def get_sequence(sequence_data: SequenceData, service: SequenceService = Depends(DependencyInjector.get_sequence_service)):
    try:
        sequence_id = sequence_data.sequence_id
        response = await service.get_sequence(sequence_id)
        return response

    except Exception as e:
        raise CustomException(e)


@router.post("/sequence/create_custom")
async def create_custom_sequence(
    data: CreateCustomSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
):
    """
    Create a custom yoga sequence for the user.
    Uses the user profile (medical conditions, goals) and posture catalogue
    to generate a personalized sequence via LLM.
    """
    try:
        response = await service.create_custom_sequence(
            user_id=data.user_id,
            duration_minutes=data.duration_minutes,
            focus=data.focus,
        )
        return response
    except RuntimeError as e:
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(e)
