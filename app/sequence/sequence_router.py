from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth_service import get_current_user_id
from app.auth.settings import get_auth_settings
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from app.usage.auth_budget_deps import UserBudgetAccess, get_user_budget_access
from app.usage.budget_http import raise_if_llm_daily_cap_exceeded
from app.usage.llm_pricing import config_usd_to_micro_usd
from app.schemas.sequence_requests import (
    CreateManualSequenceData,
    GenerateSequenceData,
    SequenceData,
    UpdateSequenceData,
)
from app.sequence.sequence_service import SequenceService

router = APIRouter()


@router.post("/sequence/get_sequences")
async def get_sequences(
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    try:
        return await service.get_sequences(user_id=user_id)
    except Exception as e:
        raise CustomException(str(e))


@router.get("/sequence/get_postures")
async def get_postures(
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Get all postures from the postures collection."""
    try:
        return await service.get_postures()
    except Exception as e:
        raise CustomException(str(e))


@router.get("/sequence/get_themes")
async def get_themes(
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Get all themes from the themes collection."""
    try:
        return await service.get_themes()
    except Exception as e:
        raise CustomException(str(e))


@router.post("/sequence/get_sequence")
async def get_sequence(
    sequence_data: SequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    try:
        return await service.get_sequence(sequence_data.sequence_id, user_id)
    except ValueError as e:
        msg = str(e).lower()
        if "access denied" in msg:
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise CustomException(str(e))


@router.post("/sequence/generate")
async def generate_sequence(
    data: GenerateSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    access: UserBudgetAccess = Depends(get_user_budget_access),
):
    """
    Generate a personalized yoga sequence for the user.

    On the first call (no review_answers), the requirement reviewer checks
    for conflicts. If questions are returned, the response has status=false
    with questions and a summary.     On the second call (with review_answers), the requirement reviewer is skipped
    and answers are threaded into the composer; automated sequence review still runs.
    """
    settings = get_auth_settings()
    cap_micro = config_usd_to_micro_usd(settings.user_daily_llm_usd_cap)
    raise_if_llm_daily_cap_exceeded(
        llm_cost=access.llm_cost,
        cap_micro_usd=cap_micro,
        limit_usd=settings.user_daily_llm_usd_cap,
    )
    try:
        return await service.generate_sequence(
            user_id=access.user_id,
            practice_theme_id=data.practice_theme_id,
            duration_minutes=data.duration_minutes,
            user_notes=data.user_notes,
            questions=data.questions,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise CustomException(str(e))


@router.post("/sequence/create_manual_sequence")
async def create_manual_sequence(
    data: CreateManualSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Create a manual sequence from user-selected posture client_ids."""
    try:
        return await service.create_manual_sequence(
            name=data.name,
            posture_client_ids=data.posture_client_ids,
            user_id=user_id,
        )
    except Exception as e:
        raise CustomException(str(e))


@router.post("/sequence/update")
async def update_sequence(
    data: UpdateSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Update a sequence's name and ordered postures (same shape as stored in DB)."""
    try:
        return await service.update_sequence(
            sequence_id=data.sequence_id,
            name=data.name,
            postures=data.postures,
            user_id=user_id,
        )
    except Exception as e:
        raise CustomException(str(e))
