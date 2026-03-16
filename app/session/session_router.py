from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.session.session_service import SessionService
from app.session.session_interfaces import SeriesData, GetInstructionsData
from app.dependency_injector import DependencyInjector
from app.globals.errors import CustomException
from bson import ObjectId

router = APIRouter()


@router.post("/session/start")
async def start_user_session(series_data: SeriesData, service: SessionService = Depends(DependencyInjector.get_session_service)):
    """
    Start a new yoga session.
    Pre-generates all guidance texts (intro, transitions, ending) and stores them in the session document.
    """
    try:
        sequence_id = series_data.sequence_id
        user_name = "Aarush"
        user_id = ObjectId("67d5632a3a9bdddef290e127")  # TODO: Get from authentication
        response = await service.start_user_session(user_id=user_id, sequence_id=sequence_id, user_name=user_name)
        return response

    except ValueError as e:
        raise CustomException(str(e))

    except RuntimeError as e:
        raise CustomException(str(e))

    except Exception as e:
        raise CustomException(str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str, service: SessionService = Depends(DependencyInjector.get_session_service)):
    """Return session info by session_id. Excludes instructions."""
    try:
        response = await service.get_session_info(session_id)
        return response
    except RuntimeError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(str(e))


@router.post("/session/get_instructions")
async def get_instructions(data: GetInstructionsData, service: SessionService = Depends(DependencyInjector.get_session_service)):
    """Return instructions for a session. Excludes audio_path from each instruction."""
    try:
        instructions = await service.get_instructions(data.session_id)
        return {"status": True, "instructions": instructions}
    except RuntimeError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(str(e))


@router.get("/session/{session_id}/audio/{message_id}")
async def get_audio(
    session_id: str,
    message_id: str,
    service: SessionService = Depends(DependencyInjector.get_session_service),
):
    """Stream audio chunks for a session instruction. Generates on-demand if file is missing."""
    try:
        chunk_stream = service.get_audio_chunks(session_id=session_id, message_id=message_id)
        return StreamingResponse(chunk_stream, media_type="audio/mpeg")
    except RuntimeError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise CustomException(str(e))
    except Exception as e:
        raise CustomException(str(e))
