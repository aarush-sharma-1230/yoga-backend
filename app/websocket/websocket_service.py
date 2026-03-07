import traceback
from fastapi import WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import json
import asyncio


class ConnectionManager:
  def __init__(self):
    self.active_connections = {}

  async def connect(self, websocket: WebSocket, user_id: str):
    try:
      existing_connection = self.active_connections.get(user_id)

      if existing_connection:
        raise Exception("User session is already running")

      await websocket.accept()
      self.active_connections[user_id] = websocket

    except Exception as e:
      print(f"Error during connection: {e}")

  async def disconnect(self, websocket: WebSocket, user_id: str):
    if self.active_connections[user_id]:
      self.active_connections.pop(user_id, None)

    if websocket:
      await websocket.close()

  async def send_message(self, message: dict, websocket: WebSocket):
    await websocket.send_json(message)

  async def send_audio_bytes(self, chunk, websocket: WebSocket):
    await websocket.send_bytes(chunk)


class WebSocketService:
  def __init__(self, db: AsyncIOMotorDatabase, query_service, connection_manager, session_service, yoga_agent):
    self.db = db
    self.query_service = query_service
    self.session_service = session_service
    self.connection_manager = connection_manager
    self.yoga_agent = yoga_agent

  def calculate_wait_time(self, current_posture):
    current_timestamp = datetime.utcnow()
    time_taken = (current_timestamp - current_posture["started_on"]).total_seconds() if current_posture else 0
    waiting_time = 60 - time_taken
    return waiting_time

  async def _stream_audio(self, websocket: WebSocket, text: str):
    for chunk in self.yoga_agent.generate_audio(text):
      await self.connection_manager.send_audio_bytes(chunk, websocket)

  async def _send_response(self, websocket: WebSocket, response: dict, stream: bool = True):
    if not response:
      raise Exception("Failed to generate response")

    await self.connection_manager.send_message(response, websocket)

    if stream:
      await self._stream_audio(websocket, response["result"]["text"])

  async def run_session(self, websocket: WebSocket, user_id: str, session_id: str, resume_session: asyncio.Event):
    last_response_sent_at = datetime.utcnow()
    session = await self.session_service.get_session_by_id(session_id)
    postures = session["sequence"]["postures"]

    for posture in postures:
      await resume_session.wait()

      session = await self.session_service.get_session_by_id(session_id)
      current_posture = session["current_posture"]
      chat_history = session["chat_history"]["messages"]
      current_posture_idx = current_posture["idx"] if current_posture else -1

      upcoming_response = await self.query_service.process_transition_query(current_posture_idx, session_id, postures, chat_history)

      time_taken_to_generate_response = (datetime.utcnow() - last_response_sent_at).total_seconds()
      await asyncio.sleep(60 - time_taken_to_generate_response)
      last_response_sent_at = datetime.utcnow()

      await self._send_response(websocket, upcoming_response)

  async def close_connection(self, websocket: WebSocket, session_id, user_id, session_task):
    end_session_response = {"status": True, "type": "session_ended", "result": {
        "text": "This is session ending. Namaste", "msg_id": "12312321"}}  # await self.query_service.end_user_session(session_id)
    await self._send_response(websocket, end_session_response)

    if session_task:
      session_task.cancel()

    await self.connection_manager.disconnect(websocket, user_id)

  async def handle_connection(self, websocket: WebSocket, user_id: str):
    await self.connection_manager.connect(websocket, user_id)
    resume_session = asyncio.Event()
    resume_session.set()

    session_task = None
    session_id = None

    try:
      while True:
        data = await websocket.receive_text()
        message = json.loads(data)

        if message["type"] == "start_session":
          try:
            response = await self.query_service.start_user_session(user_id=user_id, sequence_id=message["sequence_id"])

            session_id = response["session_id"]
            await self._send_response(websocket, response)

            session_task = asyncio.create_task(self.run_session(websocket, user_id, session_id, resume_session))
            await session_task

            await self.close_connection(websocket, session_id, user_id, session_task)
            break

          except Exception as e:
            traceback.print_exc()
            await self.connection_manager.send_message({"type": "session_error", "text": str(e)}, websocket)

            if session_task:
              session_task.cancel()

            await self.connection_manager.disconnect(websocket, user_id)

        elif message["type"] == "user_query":
          try:
            session = await self.db["session"].find_one({"_id": session_id})

            # user_query: str, session_id: str, postures: list, current_posture_name, chat_history: list
            current_posture_name = session["current_posture"]['name']
            chat_history = session["chat_history"].messages
            postures = session["sequence"].postures

            resume_session.clear()

            user_query = message["text"]
            response = await self.query_service.process_user_query(user_query=user_query, session_id=session_id, postures=postures, current_posture_name=current_posture_name, chat_history=chat_history)

            if not response:
              raise Exception("Failed to answer user query")

            await self.connection_manager.send_message(response, websocket)
            resume_session.set()

          except Exception as e:
            await self.connection_manager.send_message({"type": "query_error", "text": str(e)}, websocket)
            resume_session.set()

        elif message["type"] == "end_session":
          try:
            await self.close_connection(websocket, session_id, user_id, session_task)
            break

          except Exception as e:
            await self.connection_manager.send_message({"type": "session_error", "text": str(e)}, websocket)

            if session_task:
              session_task.cancel()

            await self.connection_manager.disconnect(websocket, user_id)
            break

    except WebSocketDisconnect:
      if session_task:
        session_task.cancel()

      await self.connection_manager.disconnect(websocket, user_id)
