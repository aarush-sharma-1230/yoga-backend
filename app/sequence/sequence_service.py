from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.agents.sequence_composer import SequenceComposer
from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_VINYASA_LOOP,
    CustomSequenceOutput,
    SequencePostureItem,
)
from app.sequence.posture_row import canonical_posture_row

DEFAULT_MANUAL_HOLD_SECONDS = 60


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

    async def get_themes(self):
        """Fetch all themes from the themes collection."""
        themes = await self.db["themes"].find().to_list(length=None)
        return {"status": True, "result": themes}

    async def get_sequence(self, sequence_id: str):
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})
        if not sequence:
            raise ValueError(f"Sequence not found: {sequence_id}")
        client_ids = self._client_ids_from_stored_postures(sequence.get("postures", []))
        db_by_client = {}
        if client_ids:
            async for doc in self.db["postures"].find({"client_id": {"$in": client_ids}}):
                db_by_client[doc["client_id"]] = doc
        postures = [self._normalize_stored_posture(p, db_by_client) for p in sequence.get("postures", [])]
        return {"status": True, "result": {**sequence, "postures": postures}}

    def _client_ids_from_stored_postures(self, postures: list) -> list[str]:
        """Collect client_ids from stored sequence postures (flat, interval_set, or vinyasa_loop)."""
        ids: set[str] = set()
        for p in postures:
            intent = p.get("posture_intent")
            if intent == POSTURE_INTENT_INTERVAL_SET:
                wp = p.get("work_posture") or {}
                rp = p.get("recovery_posture") or {}
                if wp.get("client_id"):
                    ids.add(wp["client_id"])
                if rp.get("client_id"):
                    ids.add(rp["client_id"])
            elif intent == POSTURE_INTENT_VINYASA_LOOP:
                for slot in p.get("cycle_postures") or []:
                    cid = slot.get("client_id")
                    if cid:
                        ids.add(cid)
            elif p.get("client_id"):
                ids.add(p["client_id"])
        return list(ids)

    def _normalize_stored_posture(self, p: dict, db_by_client: dict[str, dict]) -> dict:
        """Refresh names from DB while keeping stored intent, modifications, and timing fields."""
        intent = p.get("posture_intent")
        if intent == POSTURE_INTENT_INTERVAL_SET:
            wp, rp = p.get("work_posture") or {}, p.get("recovery_posture") or {}
            wdoc, rdoc = db_by_client.get(wp.get("client_id")), db_by_client.get(rp.get("client_id"))
            if not wdoc or not rdoc:
                return p
            return {
                "posture_intent": POSTURE_INTENT_INTERVAL_SET,
                "rounds": p["rounds"],
                "hold_time_seconds": p["hold_time_seconds"],
                "rest_time_seconds": p["rest_time_seconds"],
                "work_posture": canonical_posture_row(
                    wdoc,
                    posture_intent=POSTURE_INTENT_STATIC_HOLD,
                    recommended_modification=wp.get("recommended_modification", ""),
                ),
                "recovery_posture": canonical_posture_row(
                    rdoc,
                    posture_intent=POSTURE_INTENT_STATIC_HOLD,
                    recommended_modification=rp.get("recommended_modification", ""),
                ),
            }

        if intent == POSTURE_INTENT_VINYASA_LOOP:
            slots = p.get("cycle_postures") or []
            rebuilt = []
            for slot in slots:
                doc = db_by_client.get(slot.get("client_id"))
                if not doc:
                    return p
                rebuilt.append(
                    canonical_posture_row(
                        doc,
                        posture_intent=POSTURE_INTENT_STATIC_HOLD,
                        recommended_modification=slot.get("recommended_modification", ""),
                    )
                )
            return {
                "posture_intent": POSTURE_INTENT_VINYASA_LOOP,
                "rounds": p["rounds"],
                "cycle_postures": rebuilt,
            }

        doc = db_by_client.get(p.get("client_id"))
        if not doc:
            return p
        row = canonical_posture_row(
            doc,
            posture_intent=p.get("posture_intent", POSTURE_INTENT_STATIC_HOLD),
            recommended_modification=p.get("recommended_modification", ""),
        )
        if intent == POSTURE_INTENT_STATIC_HOLD and "hold_time_seconds" in p:
            row["hold_time_seconds"] = p["hold_time_seconds"]
        return row

    def _client_ids_from_llm_output(self, output: CustomSequenceOutput) -> set[str]:
        ids: set[str] = set()
        for item in output.postures:
            if item.posture_intent == POSTURE_INTENT_INTERVAL_SET:
                assert item.work_posture is not None and item.recovery_posture is not None
                ids.add(item.work_posture.posture_id)
                ids.add(item.recovery_posture.posture_id)
            elif item.posture_intent == POSTURE_INTENT_VINYASA_LOOP:
                assert item.cycle_postures is not None
                for slot in item.cycle_postures:
                    ids.add(slot.posture_id)
            else:
                assert item.posture_id is not None
                ids.add(item.posture_id)
        return ids

    def _stored_posture_from_llm_item(
        self, item: SequencePostureItem, db_postures: dict[str, dict]
    ) -> dict | None:
        """Build one stored sequence row from a validated LLM posture item."""
        if item.posture_intent == POSTURE_INTENT_INTERVAL_SET:
            assert item.work_posture is not None and item.recovery_posture is not None
            wdoc = db_postures.get(item.work_posture.posture_id)
            rdoc = db_postures.get(item.recovery_posture.posture_id)
            if not wdoc or not rdoc:
                return None
            return {
                "posture_intent": POSTURE_INTENT_INTERVAL_SET,
                "rounds": item.rounds,
                "hold_time_seconds": item.hold_time_seconds,
                "rest_time_seconds": item.rest_time_seconds,
                "work_posture": canonical_posture_row(
                    wdoc,
                    posture_intent=POSTURE_INTENT_STATIC_HOLD,
                    recommended_modification=item.work_posture.recommended_modification,
                ),
                "recovery_posture": canonical_posture_row(
                    rdoc,
                    posture_intent=POSTURE_INTENT_STATIC_HOLD,
                    recommended_modification=item.recovery_posture.recommended_modification,
                ),
            }

        if item.posture_intent == POSTURE_INTENT_VINYASA_LOOP:
            assert item.cycle_postures is not None and item.rounds is not None
            rows = []
            for slot in item.cycle_postures:
                doc = db_postures.get(slot.posture_id)
                if not doc:
                    return None
                rows.append(
                    canonical_posture_row(
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
        doc = db_postures.get(item.posture_id)
        if not doc:
            return None
        row = canonical_posture_row(
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
    ) -> dict:
        """
        Generate a sequence using the LLM, user profile, theme, and posture catalogue.
        """
        if not self.sequence_composer:
            raise RuntimeError("SequenceComposer is required for sequence generation")

        try:
            theme = await self.db["themes"].find_one({"_id": ObjectId(practice_theme_id)})
        except Exception:
            raise ValueError(f"Invalid theme ID: {practice_theme_id}")
        if not theme:
            raise ValueError(f"Theme not found: {practice_theme_id}")

        output: CustomSequenceOutput = await self.sequence_composer.compose_sequence(
            response_format=CustomSequenceOutput,
            user_id=user_id,
            duration_minutes=duration_minutes,
            theme=theme,
            user_notes=user_notes,
        )

        all_posture_ids = list(self._client_ids_from_llm_output(output))

        db_postures = {}
        async for doc in self.db["postures"].find({"client_id": {"$in": all_posture_ids}}):
            db_postures[doc["client_id"]] = doc

        postures = []
        for item in output.postures:
            row = self._stored_posture_from_llm_item(item, db_postures)
            if row:
                postures.append(row)

        if not postures:
            raise RuntimeError("No valid postures selected; sequence generation failed")

        sequence_doc = {
            "name": output.name,
            "postures": postures,
            "type": "generated",
            "user_id": user_id,
            "practice_theme_id": practice_theme_id,
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
        Resolves postures from DB, preserving order. Each row is a static_hold with default hold time.
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
            row = canonical_posture_row(
                id_to_posture[pid],
                posture_intent=POSTURE_INTENT_STATIC_HOLD,
                recommended_modification="",
            )
            row["hold_time_seconds"] = DEFAULT_MANUAL_HOLD_SECONDS
            postures.append(row)

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
