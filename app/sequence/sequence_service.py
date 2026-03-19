from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.agents.sequence_composer import SequenceComposer
from app.posture_docs.all_postures import ALL_POSTURES
from app.prompts.user import get_custom_sequence_prompt
from app.schemas.custom_sequence import CustomSequenceOutput

POSTURE_BY_ID = {p["client_id"]: p for p in ALL_POSTURES}


class SequenceService:
    def __init__(self, db: AsyncIOMotorDatabase, sequence_composer: SequenceComposer | None = None):
        self.db = db
        self.sequence_composer = sequence_composer

    async def get_sequences(self):
        pipeline = [{"$project": {"_id": 1, "name": 1, "postures": 1, "type": 1, "user_id": 1}}]
        sequences = await self.db["sequences"].aggregate(pipeline).to_list(length=None)
        return {"status": True, "result": sequences}

    async def get_postures(self):
        """Fetch all postures from the postures collection."""
        postures = await self.db["postures"].find().to_list(length=None)
        return {"status": True, "result": postures}

    async def get_sequence(self, sequence_id: str):
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        return {"status": True, "result": sequence}

    def _posture_for_sequence(self, posture: dict) -> dict:
        """Build sequence posture format: name as string for display, full object for transitions."""
        name = posture.get("name") or {}
        english = name.get("english", "Unknown")
        return {**posture, "name": english}

    async def generate_sequence(
        self,
        user_id: str,
        duration_minutes: int | None = None,
        focus: str | None = None,
        intensity_level: str | None = None,
        user_notes: str | None = None,
    ) -> dict:
        """
        Generate a sequence using the LLM, user profile, and posture catalogue.
        Saves to DB and returns the new sequence.
        """
        if not self.sequence_composer:
            raise RuntimeError("SequenceComposer is required for sequence generation")

        prompt = get_custom_sequence_prompt(
            postures=ALL_POSTURES,
            duration_minutes=duration_minutes,
            focus=focus,
            intensity_level=intensity_level,
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
            "type": "generated",
            "user_id": user_id,
            "created_at": datetime.utcnow(),
        }
        result = await self.db["sequences"].insert_one(sequence_doc)
        sequence_doc["_id"] = result.inserted_id

        return {
            "status": True,
            "result": {
                **sequence_doc,
                "reasoning": output.reasoning,
            },
        }

    async def create_manual_sequence(
        self, name: str, posture_client_ids: list[str], user_id: str
    ) -> dict:
        """
        Create a manual sequence from user-provided posture client_ids.
        Resolves postures from DB, preserving order.
        """
        if not posture_client_ids:
            raise ValueError("posture_client_ids cannot be empty")

        id_to_posture = {}
        async for doc in self.db["postures"].find({"client_id": {"$in": posture_client_ids}}):
            id_to_posture[doc["client_id"]] = doc

        missing_ids = [pid for pid in posture_client_ids if pid not in id_to_posture]
        if missing_ids:
            raise ValueError(f"Posture IDs not found in database: {missing_ids}")

        postures = []
        for pid in posture_client_ids:
            postures.append(self._posture_for_sequence(id_to_posture[pid]))

        sequence_doc = {
            "name": name,
            "postures": postures,
            "type": "manual",
            "user_id": user_id,
            "created_at": datetime.utcnow(),
        }
        result = await self.db["sequences"].insert_one(sequence_doc)
        sequence_doc["_id"] = result.inserted_id

        return {"status": True, "result": sequence_doc}
