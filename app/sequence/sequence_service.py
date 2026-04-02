from datetime import datetime

from bson import ObjectId
from openai import RateLimitError
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.agents.request_reviewer import RequestReviewer
from app.agents.sequence_composer import SequenceComposer
from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_VINYASA_LOOP,
    CustomSequenceOutput,
    SequencePostureItem,
)
from app.schemas.request_review import ReviewQuestionAnswered

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
        sequence_composer: SequenceComposer | None = None,
        request_reviewer: RequestReviewer | None = None,
    ):
        self.db = db
        self.sequence_composer = sequence_composer
        self.request_reviewer = request_reviewer

    async def get_sequences(self, user_id: str):
        pipeline = [{"$match": {"user_id": ObjectId(user_id)}}, {"$sort": {"created_at": -1}}, {"$project": {"_id": 1, "name": 1, "postures": 1, "type": 1, "user_id": 1, "duration_minutes": 1, "practice_theme_id": 1, "user_notes": 1, "created_at": 1}}]
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

    @staticmethod
    def _format_review_qa_context(questions: list[ReviewQuestionAnswered]) -> str:
        """Render answered review questions into plain text for the composer prompt."""
        lines: list[str] = []
        for ra in questions:
            lines.append(f"Q: {ra.question}")
            lines.append(f"A: {', '.join(ra.answer)}")
            lines.append("")
        return "\n".join(lines).strip()

    async def _fetch_theme(self, practice_theme_id: str) -> dict:
        """Load a theme document by ObjectId string, raising on invalid/missing."""
        try:
            theme = await self.db["themes"].find_one({"_id": ObjectId(practice_theme_id)})
        except Exception:
            raise ValueError(f"Invalid theme ID: {practice_theme_id}")
        if not theme:
            raise ValueError(f"Theme not found: {practice_theme_id}")
        return theme

    async def _compose_and_persist_sequence(
        self,
        user_id: str,
        practice_theme_id: str,
        duration_minutes: int,
        theme: dict,
        user_notes: str | None,
        review_qa_context: str | None = None,
    ) -> dict:
        """Run SequenceComposer, resolve postures from DB, persist, and return the result."""
        try:
            output: CustomSequenceOutput = await self.sequence_composer.compose_sequence(
                response_format=CustomSequenceOutput,
                user_id=user_id,
                duration_minutes=duration_minutes,
                theme=theme,
                user_notes=user_notes,
                review_qa_context=review_qa_context,
            )
        except RateLimitError as e:
            raise RuntimeError(
                "OpenAI rate limit or quota exceeded (check billing and plan at "
                "https://platform.openai.com/account/billing). Sequence generation was not completed."
            ) from e

        all_posture_ids = list(self._client_ids_from_llm_output(output))

        db_postures = {}
        async for doc in self.db["postures"].find({"client_id": {"$in": all_posture_ids}}):
            cid = doc.get("client_id")
            if cid is None:
                continue
            db_postures[_norm_cid(str(cid))] = doc

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
            "duration_minutes": duration_minutes,
            "user_id": ObjectId(user_id),
            "practice_theme_id": ObjectId(practice_theme_id),
            "user_notes": user_notes,
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

    async def generate_sequence(
        self,
        user_id: str,
        practice_theme_id: str,
        duration_minutes: int,
        user_notes: str | None = None,
        questions: list[ReviewQuestionAnswered] | None = None,
    ) -> dict:
        """
        Generate a sequence with an optional review gate.

        Pass 1 (questions is None): run RequestReviewer first. If it returns
        questions, return them immediately without composing a sequence.
        Pass 2 (questions provided): skip the reviewer, format Q&A as context
        for the SequenceComposer.
        """
        if not self.sequence_composer:
            raise RuntimeError("SequenceComposer is required for sequence generation")

        theme = await self._fetch_theme(practice_theme_id)

        if questions is not None:
            review_qa_context = self._format_review_qa_context(questions)
            return await self._compose_and_persist_sequence(
                user_id=user_id,
                practice_theme_id=practice_theme_id,
                duration_minutes=duration_minutes,
                theme=theme,
                user_notes=user_notes,
                review_qa_context=review_qa_context,
            )

        if self.request_reviewer:
            review_output = await self.request_reviewer.review_request(
                user_id=user_id,
                duration_minutes=duration_minutes,
                theme=theme,
                user_notes=user_notes,
            )
            if not review_output.status:
                return {
                    "status": False,
                    "questions": [q.model_dump() for q in review_output.questions],
                }

        return await self._compose_and_persist_sequence(
            user_id=user_id,
            practice_theme_id=practice_theme_id,
            duration_minutes=duration_minutes,
            theme=theme,
            user_notes=user_notes,
        )

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
            row = self.canonical_posture_row(
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
