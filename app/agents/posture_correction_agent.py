"""
Posture correction agent: combines landmark checks into one personalized instruction.

Loads session, user profile, optional theme and posture catalogue, then calls the LLM.
The prompt is fully inlined—no tool calls from inside the model.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.prompts.v4.developer.posture_correction import get_posture_correction_developer_prompt
from app.prompts.v4.developer.profile_context import extract_profile_context
from app.prompts.v4.pose_landmarks_user import get_posture_correction_user_prompt
from app.schemas.pose_landmarks import PoseLandmarksRequest, PostureCorrectionInstructionOutput


class PostureCorrectionAgent:
    """Fetches session and profile context, builds prompts, returns structured instruction."""

    def __init__(self, llm_client, auth_service, db: AsyncIOMotorDatabase):
        self.llm_client = llm_client
        self.auth_service = auth_service
        self.db = db
        self.model = "gpt-5.4-mini"

    async def _get_developer_prompt(self, user_id: Optional[str]) -> str:
        """Fetch profile, extract context, build developer prompt."""
        user = None
        if user_id:
            try:
                user = await self.auth_service.get_profile(str(user_id))
            except RuntimeError:
                pass
        ctx = extract_profile_context(user)
        return get_posture_correction_developer_prompt(ctx)

    async def _fetch_theme_summary(self, practice_theme_id: Any) -> str | None:
        """Return a short human-readable theme line for the prompt, or None."""
        if practice_theme_id is None:
            return None
        try:
            oid = practice_theme_id if isinstance(practice_theme_id, ObjectId) else ObjectId(str(practice_theme_id))
        except Exception:
            return None
        theme = await self.db["themes"].find_one({"_id": oid})
        if not theme:
            return None
        name = theme.get("name") or ""
        desc = theme.get("description") or theme.get("summary") or ""
        parts = [p for p in (name, desc) if p]
        return "\n".join(parts) if parts else None

    async def _fetch_posture_doc(self, client_id: str) -> dict[str, Any] | None:
        """Load catalogue fields for the posture_client_id."""
        doc = await self.db["postures"].find_one({"client_id": client_id})
        if not doc:
            return None
        out: dict[str, Any] = {
            "client_id": doc.get("client_id"),
            "name": doc.get("name"),
            "sanskrit_name": doc.get("sanskrit_name"),
        }
        for key in ("intensity_profile", "sensory_cues", "typical_cues", "contraindications", "chronic_pain"):
            if doc.get(key) is not None:
                out[key] = doc.get(key)
        return out

    def _review_qa_from_sequence(self, sequence: dict) -> str | None:
        """Use persisted review context if the sequence document ever stores it."""
        direct = sequence.get("review_qa_context")
        if isinstance(direct, str) and direct.strip():
            return direct
        raw = sequence.get("review_answers") or sequence.get("answered_questions")
        if isinstance(raw, list) and raw:
            try:
                return json.dumps(raw, indent=2)
            except TypeError:
                return str(raw)
        return None

    async def generate_combined_instruction(
        self,
        *,
        session_id: str,
        payload: PoseLandmarksRequest,
    ) -> dict[str, Any]:
        """
        Build the user prompt from fetched data and return structured instruction plus message_id.

        Raises RuntimeError if the session is missing or invalid.
        """
        session = await self.db["session"].find_one({"_id": ObjectId(session_id)})
        if not session:
            raise RuntimeError("The given session was not found")

        user_id = session.get("user_id")
        user_id_str = str(user_id) if user_id is not None else None

        sequence = session.get("sequence") or {}
        sequence_name = sequence.get("name")
        user_notes = sequence.get("user_notes")
        practice_theme_id = sequence.get("practice_theme_id")
        review_qa_context = self._review_qa_from_sequence(sequence)

        theme_summary = await self._fetch_theme_summary(practice_theme_id)
        posture_doc = await self._fetch_posture_doc(payload.posture_client_id)

        landmarks = [lm.model_dump() for lm in payload.world_landmarks]
        checks = [c.model_dump(by_alias=True) for c in payload.checks]

        user_prompt = get_posture_correction_user_prompt(
            sequence_name=sequence_name,
            session_theme_summary=theme_summary,
            user_notes=user_notes,
            review_qa_context=review_qa_context,
            posture_catalogue_json=posture_doc,
            posture_client_id=payload.posture_client_id,
            orientation=payload.orientation,
            world_landmarks=landmarks,
            checks=checks,
        )

        developer_prompt = await self._get_developer_prompt(user_id_str)

        parsed, message_id = await asyncio.to_thread(
            self.llm_client.generate_with_schema_meta,
            prompt=user_prompt,
            developer_prompt=developer_prompt,
            response_format=PostureCorrectionInstructionOutput,
            model=self.model,
            temperature=0.5,
        )
        if parsed is None:
            raise RuntimeError("LLM returned no posture correction output")

        return {
            "instruction": parsed.instruction,
            "message_id": message_id,
        }
