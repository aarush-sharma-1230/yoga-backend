from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.auth.auth_service import AuthService
from app.auth.auth_service import get_current_user_id
from app.auth.settings import get_auth_settings
from app.session.session_service import SessionService
from app.schemas.pose_landmarks import PoseLandmarksRequest
from app.schemas.session_state import CurrentSessionStateRequest
from app.schemas.session_requests import SeriesData
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from app.usage.auth_budget_deps import UserBudgetAccess, get_user_budget_access
from app.usage.budget_http import raise_if_llm_daily_cap_exceeded
from app.usage.llm_pricing import config_usd_to_micro_usd
from bson import ObjectId

router = APIRouter()


def _map_session_dependency_error(exc: Exception) -> None:
    """Translate service errors into HTTP status codes or CustomException."""
    if isinstance(exc, HTTPException):
        raise exc
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if isinstance(exc, RuntimeError) and "not found" in str(exc).lower():
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise CustomException(str(exc)) from exc


@router.post("/session/start")
async def start_user_session(
    series_data: SeriesData,
    access: UserBudgetAccess = Depends(get_user_budget_access),
    service: SessionService = Depends(DependencyInjector.get_session_service),
    auth_service: AuthService = Depends(DependencyInjector.get_auth_service),
):
    """
    Start a new yoga session.
    Pre-generates guidance: `intro` and `ending` as top-level fields; per-posture transition audio under `sequence.postures`.
    """
    try:
        user_id_str = access.user_id
        remaining_sec = access.seconds_until_exp
        settings = get_auth_settings()
        min_sec = settings.min_remaining_to_start_minutes * 60
        if remaining_sec < min_sec:
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "access_token_expiring",
                    "message": "Access token does not have enough lifetime left; refresh before starting a session.",
                },
            )
        cap_micro = config_usd_to_micro_usd(settings.user_daily_llm_usd_cap)
        raise_if_llm_daily_cap_exceeded(
            llm_cost=access.llm_cost,
            cap_micro_usd=cap_micro,
            limit_usd=settings.user_daily_llm_usd_cap,
        )
        sequence_id = series_data.sequence_id
        user = await auth_service.get_profile(user_id_str)
        user_name = user.get("full_name") or "Friend"
        return await service.start_user_session(user_id=user_id_str, sequence_id=sequence_id, user_name=user_name)
    except HTTPException:
        raise
    except Exception as e:
        raise CustomException(str(e))


@router.post("/session/{session_id}/pose_landmarks")
async def submit_pose_landmarks(
    session_id: str,
    body: PoseLandmarksRequest,
    user_id: str = Depends(get_current_user_id),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Submit world landmarks and geometric checks; returns a single combined alignment instruction
    tailored to the session and user profile.
    """
    try:
        await service.require_session_owned_by_user(session_id, user_id)
        return await service.submit_pose_landmarks(session_id, body)
    except Exception as e:
        _map_session_dependency_error(e)


@router.post("/session/{session_id}/current_session_state")
async def update_current_session_state(
    session_id: str,
    body: CurrentSessionStateRequest,
    user_id: str = Depends(get_current_user_id),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Update `session_status` (`session_play_status` and `current_position`) on the session document.

    Use `session_play_status` `"abandoned"` when the user leaves the session without completing it.
    """
    try:
        await service.require_session_owned_by_user(session_id, user_id)
        return await service.update_current_session_state(session_id, body)
    except Exception as e:
        _map_session_dependency_error(e)


@router.post("/session/{session_id}/start_over")
async def start_over_session(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Reset `session_status` to not started (no current segment) and clear `posture_correction` on each
    sequence posture so the user can restart from the chart.
    """
    try:
        await service.require_session_owned_by_user(session_id, user_id)
        return await service.start_over_session(session_id)
    except Exception as e:
        _map_session_dependency_error(e)


@router.get("/session/latest_incomplete")
async def get_latest_incomplete_session(
    user_id: str = Depends(get_current_user_id),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Return the latest session for the user when it is ``not_started`` or ``in_progress``; if the latest
    session is ``completed``, ``abandoned``, or the user has no sessions, ``session`` is null.
    """
    session = await service.get_latest_incomplete_session_for_user(ObjectId(user_id))
    return {"session": session}


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """Return session info by session_id. Omits legacy `instructions` if present; intro/ending are top-level on the document."""
    try:
        await service.require_session_owned_by_user(session_id, user_id)
        return await service.get_session_info(session_id)
    except Exception as e:
        _map_session_dependency_error(e)


@router.get("/session/{session_id}/audio/{message_id}")
async def get_audio(
    session_id: str,
    message_id: str,
    user_id: str = Depends(get_current_user_id),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Stream one audio clip. `message_id` is `intro`/`ending` message_id or a guidance step's
    `instruction_message_id` / `sensory_message_id` from the session document.
    """
    try:
        await service.require_session_owned_by_user(session_id, user_id)
        chunk_stream = service.get_audio_chunks(session_id=session_id, message_id=message_id)
        return StreamingResponse(chunk_stream, media_type="audio/mpeg")
    except Exception as e:
        _map_session_dependency_error(e)
