from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_VINYASA_LOOP,
    CustomSequenceOutput,
    SequencePostureItem,
)
from app.schemas.stored_sequence_posture import StoredSequencePostureItem
from app.schemas.request_review import ReviewQuestionAnswered
from app.orchestration.runner import run_sequence_generation

DEFAULT_MANUAL_HOLD_SECONDS = 60


def _norm_cid(raw: str | None) -> str:
    """Normalize catalogue / DB client_id for consistent dict lookups."""
    if raw is None:
        return ""
    return str(raw).strip()


class SequenceService:
    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        compiled_graph=None,
    ):
        self.db = db
        self.compiled_graph = compiled_graph

    async def get_sequences(self, user_id: str):
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$sort": {"created_at": -1}},
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "postures": 1,
                    "type": 1,
                    "user_id": 1,
                    "duration_minutes": 1,
                    "theme": 1,
                    "practice_theme_id": 1,
                    "user_notes": 1,
                    "created_at": 1,
                }
            },
        ]
        sequences = await self.db["sequences"].aggregate(pipeline).to_list(length=None)
        return {"status": True, "result": sequences}

    async def get_postures(self):
        """Fetch all postures from the postures collection."""
        postures = await self.db["postures"].find().to_list(length=None)
        return {"status": True, "result": postures}

    async def get_themes(self):
        """Fetch all themes from the themes collection."""
        themes = await self.db["themes"].find().to_list(length=None)
        return {"status": True, "result": themes}

    async def get_sequence(self, sequence_id: str):
        """Return the sequence document as stored; postures are not re-fetched from the catalogue."""
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        if not sequence:
            raise ValueError(f"Sequence not found: {sequence_id}")
        return {"status": True, "result": sequence}

    def canonical_posture_row(self, posture_doc: dict, *, posture_intent: str, recommended_modification: str) -> dict:
        """
        Map a posture document from the database to the uniform six-field shape.

        Expects flat `name` (English string) and `sanskrit_name` on the posture doc.
        Returns _id, name, sanskrit_name, client_id, posture_intent, recommended_modification.
        Does not include aliases on this row.
        """
        english = posture_doc.get("name") or "Unknown"
        sanskrit = posture_doc.get("sanskrit_name") or ""

        oid = posture_doc.get("_id") or posture_doc.get("id") or posture_doc.get("client_id")

        return {
            "_id": str(oid),
            "name": english,
            "sanskrit_name": sanskrit,
            "client_id": posture_doc.get("client_id", ""),
            "posture_intent": posture_intent,
            "recommended_modification": recommended_modification,
        }

    def _client_ids_from_llm_output(self, output: CustomSequenceOutput) -> set[str]:
        ids: set[str] = set()
        for item in output.postures:
            if item.posture_intent == POSTURE_INTENT_INTERVAL_SET:
                assert item.work_posture is not None and item.recovery_posture is not None
                ids.add(_norm_cid(item.work_posture.posture_id))
                ids.add(_norm_cid(item.recovery_posture.posture_id))
            elif item.posture_intent == POSTURE_INTENT_VINYASA_LOOP:
                assert item.cycle_postures is not None
                for slot in item.cycle_postures:
                    ids.add(_norm_cid(slot.posture_id))
            else:
                assert item.posture_id is not None
                ids.add(_norm_cid(item.posture_id))
        return {i for i in ids if i}

    def _stored_posture_from_llm_item(
        self, item: SequencePostureItem, db_postures: dict[str, dict]
    ) -> dict | None:
        """Build one stored sequence row from a validated LLM posture item."""
        if item.posture_intent == POSTURE_INTENT_INTERVAL_SET:
            assert item.work_posture is not None and item.recovery_posture is not None
            wdoc = db_postures.get(_norm_cid(item.work_posture.posture_id))
            rdoc = db_postures.get(_norm_cid(item.recovery_posture.posture_id))
            if not wdoc or not rdoc:
                return None
            return {
                "posture_intent": POSTURE_INTENT_INTERVAL_SET,
                "rounds": item.rounds,
                "hold_time_seconds": item.hold_time_seconds,
                "rest_time_seconds": item.rest_time_seconds,
                "work_posture": self.canonical_posture_row(
                    wdoc,
                    posture_intent=POSTURE_INTENT_STATIC_HOLD,
                    recommended_modification=item.work_posture.recommended_modification,
                ),
                "recovery_posture": self.canonical_posture_row(
                    rdoc,
                    posture_intent=POSTURE_INTENT_STATIC_HOLD,
                    recommended_modification=item.recovery_posture.recommended_modification,
                ),
            }

        if item.posture_intent == POSTURE_INTENT_VINYASA_LOOP:
            assert item.cycle_postures is not None and item.rounds is not None
            rows = []
            for slot in item.cycle_postures:
                doc = db_postures.get(_norm_cid(slot.posture_id))
                if not doc:
                    return None
                rows.append(
                    self.canonical_posture_row(
                        doc,
                        posture_intent=POSTURE_INTENT_STATIC_HOLD,
                        recommended_modification=slot.recommended_modification,
                    )
                )
            return {
                "posture_intent": POSTURE_INTENT_VINYASA_LOOP,
                "rounds": item.rounds,
                "cycle_postures": rows,
            }

        assert item.posture_id is not None
        doc = db_postures.get(_norm_cid(item.posture_id))
        if not doc:
            return None
        row = self.canonical_posture_row(
            doc,
            posture_intent=item.posture_intent,
            recommended_modification=item.recommended_modification,
        )
        if item.posture_intent == POSTURE_INTENT_STATIC_HOLD:
            row["hold_time_seconds"] = item.hold_time_seconds
        return row

    async def generate_sequence(
        self,
        user_id: str,
        practice_theme_id: str,
        duration_minutes: int,
        user_notes: str | None = None,
        questions: list[ReviewQuestionAnswered] | None = None,
    ) -> dict:
        """
        Generate a sequence via the LangGraph orchestration graph.

        Pass 1 (questions is None): requirement reviewer, then composer and
        sequence review (with retries), then hydration.
        Pass 2 (questions provided): requirement reviewer is skipped; answers
        are injected for the composer; sequence review still runs.
        """
        if not self.compiled_graph:
            raise RuntimeError("Sequence generation graph is not configured")

        return await run_sequence_generation(
            compiled_graph=self.compiled_graph,
            user_id=user_id,
            practice_theme_id=practice_theme_id,
            duration_minutes=duration_minutes,
            user_notes=user_notes,
            questions=questions,
        )

    def _sequence_owned_by_user(self, sequence_doc: dict, user_id: str) -> bool:
        """Return True if the sequence document belongs to the given user id string."""
        stored = sequence_doc.get("user_id")
        if stored is None:
            return False
        return str(stored) == user_id

    async def _build_manual_posture_rows(self, posture_client_ids: list[str]) -> list:
        """
        Resolve catalogue postures by client_id in order; each row is static_hold with default hold time.
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
            row = self.canonical_posture_row(
                id_to_posture[pid],
                posture_intent=POSTURE_INTENT_STATIC_HOLD,
                recommended_modification="",
            )
            row["hold_time_seconds"] = DEFAULT_MANUAL_HOLD_SECONDS
            postures.append(row)
        return postures

    async def create_manual_sequence(
        self, name: str, posture_client_ids: list[str], user_id: str
    ) -> dict:
        """
        Create a manual sequence from user-provided posture client_ids.
        Resolves postures from DB, preserving order. Each row is a static_hold with default hold time.
        """
        postures = await self._build_manual_posture_rows(posture_client_ids)

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

    async def update_sequence(
        self,
        sequence_id: str,
        name: str,
        postures: list[StoredSequencePostureItem],
        user_id: str,
    ) -> dict:
        """
        Update a sequence's display name and ordered postures.

        Each posture entry matches the document shape stored on the sequence
        (static_hold, transitional_hub, interval_set, or vinyasa_loop).
        """
        if not postures:
            raise ValueError("postures cannot be empty")

        existing = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        if not existing:
            raise ValueError(f"Sequence not found: {sequence_id}")
        if not self._sequence_owned_by_user(existing, user_id):
            raise ValueError("Sequence not found or access denied")

        stored = [row.model_dump(by_alias=True, exclude_none=True) for row in postures]
        await self.db["sequences"].update_one(
            {"_id": ObjectId(sequence_id)},
            {"$set": {"name": name, "postures": stored}},
        )
        updated = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        return {"status": True, "result": updated}
