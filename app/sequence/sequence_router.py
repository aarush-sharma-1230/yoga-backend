from fastapi import APIRouter, Depends, Request
from app.dependency_injector import DependencyInjector
from app.sequence.sequence_service import SequenceService
from app.sequence.sequence_interface import SequenceData
from app.globals.errors import CustomException

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
