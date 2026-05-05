from fastapi import APIRouter, WebSocket, Depends

from app.dependency_injector import DependencyInjector

router = APIRouter()


@router.websocket("/ws/yoga-session")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str = "67d5632a3a9bdddef290e127",
    service=Depends(DependencyInjector.get_websocket_service),
):
    return await service.handle_connection(websocket, user_id)
