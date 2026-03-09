from motor.motor_asyncio import AsyncIOMotorDatabase
from app.globals.functions import serialize_mongo_output
from bson import ObjectId
from app.globals.constants import pydantic_mongo_helper_projection


class SequenceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_sequences(self):
        pipeline = [{"$project": {"_id": 1, "name": 1, "postures": 1}}]
        sequences = await self.db["sequences"].aggregate(pipeline).to_list(length=None)
        sequences = serialize_mongo_output(sequences)
        return {"status": True, "result": sequences}

    async def get_sequence(self, sequence_id: str):
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        sequence = serialize_mongo_output(sequence)
        return {"status": True, "result": sequence}
