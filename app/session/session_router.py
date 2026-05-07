from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.auth.settings import get_auth_settings
from app.middlewares.auth import get_current_user
from app.session.session_service import SessionService
from app.schemas.pose_landmarks import PoseLandmarksRequest
from app.schemas.session_state import CurrentSessionStateRequest
from app.schemas.session_requests import SeriesData
from app.dependency_injector import DependencyInjector
from app.usage.constants import config_usd_to_micro_usd
from app.usage.helpers import enforce_user_llm_budget
from bson import ObjectId

router = APIRouter()


@router.post("/session/start")
async def start_user_session(
    series_data: SeriesData,
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Start a new yoga session.
    Pre-generates guidance: `intro` and `ending` as top-level fields; per-posture transition audio under `sequence.postures`.
    """
    user_id_str = str(user["_id"])
    settings = get_auth_settings()
    cap_micro = config_usd_to_micro_usd(settings.user_daily_llm_usd_cap)
    enforce_user_llm_budget(
        llm_cost=user.get("llm_cost"),
        cap_micro_usd=cap_micro,
        limit_usd=settings.user_daily_llm_usd_cap,
    )
    sequence_id = series_data.sequence_id
    user_name = user.get("full_name") or ""
    return await service.start_user_session(user_id=user_id_str, sequence_id=sequence_id, user_name=user_name)


@router.post("/session/{session_id}/pose_landmarks")
async def submit_pose_landmarks(
    session_id: str,
    body: PoseLandmarksRequest,
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Submit world landmarks and geometric checks; returns a single combined alignment instruction
    tailored to the session and user profile.
    """
    user_id = str(user["_id"])
    await service.require_session_owned_by_user(session_id, user_id)
    return await service.submit_pose_landmarks(session_id, body)


@router.post("/session/{session_id}/current_session_state")
async def update_current_session_state(
    session_id: str,
    body: CurrentSessionStateRequest,
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Update `session_status` (`session_play_status` and `current_position`) on the session document.

    Use `session_play_status` `"abandoned"` when the user leaves the session without completing it.
    """
    user_id = str(user["_id"])
    await service.require_session_owned_by_user(session_id, user_id)
    return await service.update_current_session_state(session_id, body)


@router.post("/session/{session_id}/start_over")
async def start_over_session(
    session_id: str,
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Reset `session_status` to not started (no current segment) and clear `posture_correction` on each
    sequence posture so the user can restart from the chart.
    """
    user_id = str(user["_id"])
    await service.require_session_owned_by_user(session_id, user_id)
    return await service.start_over_session(session_id)


@router.get("/session/latest_incomplete")
async def get_latest_incomplete_session(
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Return the latest session for the user when it is ``not_started`` or ``in_progress``; if the latest
    session is ``completed``, ``abandoned``, or the user has no sessions, ``session`` is null.
    """
    user_id = str(user["_id"])
    session = await service.get_latest_incomplete_session_for_user(ObjectId(user_id))
    return {"session": session}


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """Return session info by session_id. Omits legacy `instructions` if present; intro/ending are top-level on the document."""
    user_id = str(user["_id"])
    await service.require_session_owned_by_user(session_id, user_id)
    return await service.get_session_info(session_id)


@router.get("/session/{session_id}/audio/{message_id}")
async def get_audio(
    session_id: str,
    message_id: str,
    user: dict = Depends(get_current_user),
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """
    Stream one audio clip. `message_id` is `intro`/`ending` message_id or a guidance step's
    `instruction_message_id` / `sensory_message_id` from the session document.
    """
    user_id = str(user["_id"])
    await service.require_session_owned_by_user(session_id, user_id)
    chunk_stream = service.get_audio_chunks(session_id=session_id, message_id=message_id)
    return StreamingResponse(chunk_stream, media_type="audio/mpeg")
