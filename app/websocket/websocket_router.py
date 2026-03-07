from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.query.query_service import QueryService
from app.websocket.websocket_service import ConnectionManager
from app.session.session_service import SessionService
from app.dependency_injector import DependencyInjector
from app.globals.errors import SessionException
from app.globals.errors import QueryException
import asyncio
import json

router = APIRouter()


@router.websocket("/ws/yoga-session")
async def websocket_endpoint(websocket: WebSocket, user_id: str = "67d5632a3a9bdddef290e127", service=Depends(DependencyInjector.get_websocket_service)):
  return await service.handle_connection(websocket, user_id)
