from fastapi import APIRouter, Depends

from app.auth.auth_service import get_current_user_id
from app.auth.settings import get_auth_settings
from app.dependency_injector import DependencyInjector
from app.usage.constants import config_usd_to_micro_usd
from app.usage.helpers import UserBudgetAccess, get_user_budget_access, raise_if_llm_daily_cap_exceeded
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
    return await service.get_sequences(user_id=user_id)


@router.get("/sequence/get_postures")
async def get_postures(
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Get all postures from the postures collection."""
    return await service.get_postures()


@router.get("/sequence/get_themes")
async def get_themes(
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Get all themes from the themes collection."""
    return await service.get_themes()


@router.post("/sequence/get_sequence")
async def get_sequence(
    sequence_data: SequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    return await service.get_sequence(sequence_data.sequence_id, user_id)


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
    return await service.generate_sequence(
        user_id=access.user_id,
        practice_theme_id=data.practice_theme_id,
        duration_minutes=data.duration_minutes,
        user_notes=data.user_notes,
        questions=data.questions,
    )


@router.post("/sequence/create_manual_sequence")
async def create_manual_sequence(
    data: CreateManualSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Create a manual sequence from user-selected posture client_ids."""
    return await service.create_manual_sequence(
        name=data.name,
        posture_client_ids=data.posture_client_ids,
        user_id=user_id,
    )


@router.post("/sequence/update")
async def update_sequence(
    data: UpdateSequenceData,
    service: SequenceService = Depends(DependencyInjector.get_sequence_service),
    user_id: str = Depends(get_current_user_id),
):
    """Update a sequence's name and ordered postures (same shape as stored in DB)."""
    return await service.update_sequence(
        sequence_id=data.sequence_id,
        name=data.name,
        postures=data.postures,
        user_id=user_id,
    )
