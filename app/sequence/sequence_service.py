from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.agents.sequence_composer import SequenceComposer
from app.globals.functions import serialize_mongo_output
from app.posture_docs.inversion_postures import INVERSION_POSTURES
from app.posture_docs.prone_postures import PRONE_POSTURES
from app.posture_docs.seated_postures import SEATED_POSTURES
from app.posture_docs.standing_postures import STANDING_POSTURES
from app.posture_docs.supine_postures import SUPINE_POSTURES
from app.prompts.user import get_custom_sequence_prompt
from app.schemas.custom_sequence import CustomSequenceOutput

ALL_POSTURES = STANDING_POSTURES + SEATED_POSTURES + SUPINE_POSTURES + PRONE_POSTURES + INVERSION_POSTURES
POSTURE_BY_ID = {p["client_id"]: p for p in ALL_POSTURES}


class SequenceService:
    def __init__(self, db: AsyncIOMotorDatabase, sequence_composer: SequenceComposer | None = None):
        self.db = db
        self.sequence_composer = sequence_composer

    async def get_sequences(self):
        pipeline = [{"$project": {"_id": 1, "name": 1, "postures": 1}}]
        sequences = await self.db["sequences"].aggregate(pipeline).to_list(length=None)
        sequences = serialize_mongo_output(sequences)
        return {"status": True, "result": sequences}

    async def get_sequence(self, sequence_id: str):
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        sequence = serialize_mongo_output(sequence)
        return {"status": True, "result": sequence}

    def _posture_for_sequence(self, posture: dict) -> dict:
        """Build sequence posture format: name as string for display, full object for transitions."""
        name = posture.get("name") or {}
        english = name.get("english", "Unknown")
        return {**posture, "name": english}

    async def create_custom_sequence(
        self,
        user_id: str,
        duration_minutes: int | None = None,
        focus: str | None = None,
    ) -> dict:
        """
        Create a custom sequence using the LLM, user profile, and posture catalogue.
        Saves to DB and returns the new sequence.
        """
        if not self.sequence_composer:
            raise RuntimeError("SequenceComposer is required for custom sequence creation")

        prompt = get_custom_sequence_prompt(
            postures=ALL_POSTURES,
            duration_minutes=duration_minutes,
            focus=focus,
        )
        output: CustomSequenceOutput = await self.sequence_composer.compose_sequence(
            prompt=prompt,
            response_format=CustomSequenceOutput,
            user_id=user_id,
        )

        postures = []
        for pid in output.posture_ids:
            if pid in POSTURE_BY_ID:
                postures.append(self._posture_for_sequence(POSTURE_BY_ID[pid]))
            # Skip invalid IDs; LLM may occasionally hallucinate

        if not postures:
            raise RuntimeError("No valid postures selected; sequence generation failed")

        sequence_doc = {
            "name": output.name,
            "postures": postures,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
        }
        result = await self.db["sequences"].insert_one(sequence_doc)
        sequence_doc["_id"] = result.inserted_id
        serialized = serialize_mongo_output(sequence_doc)
        return {"status": True, "result": serialized}
