from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime


class SessionService:
  def __init__(self, db: AsyncIOMotorDatabase, yoga_agent):
    self.db = db
    self.yoga_agent = yoga_agent

  async def get_session_by_id(self, session_id: str):
    session = await self.db["session"].find_one({"_id": ObjectId(session_id)})

    if not session:
      raise RuntimeError("The given session was not found")

    return session

  async def get_sequence_by_id(self, sequence_id: str):
    sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})

    if not sequence:
      raise RuntimeError("The given sequence was not found")

    return sequence

  async def create_new_session(self, user_id: str, sequence, chat_history):
    current_timestamp = datetime.utcnow()
    current_posture = None  # {**sequence["postures"][0], "idx": 0, "started_on": current_timestamp}

    session = {
        "user_id": user_id,
        "sequence": sequence,
        "created_on": current_timestamp,
        "chat_history": chat_history,
        "current_posture": current_posture,
        "total_number_of_postures": len(sequence["postures"]),
    }

    session_created = await self.db["session"].insert_one(session)

    if not session_created:
      raise RuntimeError("Failed to create session")

    return session_created.inserted_id

  async def update_session(self, session_id: str, update_argument):
    await self.db["session"].update_one({"_id": ObjectId(session_id)}, update_argument)

  async def end_session(self, session_id: str):
    update_argument = {
        "ended_on": datetime.utcnow(),
        "status": "completed",
        "current_posture": None,
    }

    await self.update_session(session_id=session_id, update_argument=update_argument)
