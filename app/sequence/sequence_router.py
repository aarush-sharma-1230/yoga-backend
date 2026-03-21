from fastapi import APIRouter, Depends

from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from app.sequence.sequence_interface import CreateManualSequenceData, GenerateSequenceData, SequenceData
from app.sequence.sequence_service import SequenceService

router = APIRouter()

USER_ID_TEMP = "67d5632a3a9bdddef290e127"

@router.post("/sequence/get_sequences")
async def get_sequences(service: SequenceService = Depends(DependencyInjector.get_sequence_service)):
    try:
        response = await service.get_sequences()
        return response

    except Exception as e:
        raise CustomException(e)


@router.get("/sequence/get_postures")
async def get_postures(service: SequenceService = Depends(DependencyInjector.get_sequence_service)):
    """Get all postures from the postures collection."""
    try:
        response = await service.get_postures()
        return response
    except Exception as e:
        raise CustomException(e)


@router.get("/sequence/get_themes")
async def get_themes(service: SequenceService = Depends(DependencyInjector.get_sequence_service)):
    """Get all themes from the themes collection."""
    try:
        response = await service.get_themes()
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


@router.post("/sequence/generate")
async def generate_sequence(
    data: GenerateSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
):
    """
    Generate a personalized yoga sequence for the user.
    Uses the user profile (medical conditions, goals) and posture catalogue
    via LLM to create a custom sequence.
    """
    try:
        response = await service.generate_sequence(
            user_id=USER_ID_TEMP,
            practice_theme_id=data.practice_theme_id,
            duration_minutes=data.duration_minutes,
            user_notes=data.user_notes,
        )
        return response
    except ValueError as e:
        raise CustomException(str(e))
    except RuntimeError as e:
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(e)


@router.post("/sequence/create_manual_sequence")
async def create_manual_sequence(
    data: CreateManualSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
):
    """Create a manual sequence from user-selected posture client_ids."""
    try:
        response = await service.create_manual_sequence(
            name=data.name,
            posture_client_ids=data.posture_client_ids,
            user_id=USER_ID_TEMP,
        )
        return response
    except ValueError as e:
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(e)
