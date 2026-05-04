import asyncio
import logging
import os
import uuid
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from fastapi import HTTPException, status

from app.llms.openai_client import (
    DEFAULT_YOGA_TTS_INSTRUCTIONS,
    ENERGETIC_YOGA_TTS_INSTRUCTIONS,
)
from app.prompts.active import (
    get_ending_prompt,
    get_introduction_prompt,
)
from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_VINYASA_LOOP,
)
from app.session.session_trace_logger import trace
from app.schemas.pose_landmarks import PoseLandmarksRequest
from app.schemas.session_state import CurrentSessionStateRequest
from app.session.transition_request import build_transition_request
from app.usage.request_llm_cost_context import (
    get_request_llm_cost_micro_total,
    start_request_llm_cost_tracking,
    stop_request_llm_cost_tracking,
)


class SessionService:
    def __init__(self, db: AsyncIOMotorDatabase, yoga_coordinator, posture_correction_agent, llm_cost_service=None):
        self.db = db
        self.yoga_coordinator = yoga_coordinator
        self.posture_correction_agent = posture_correction_agent
        self.llm_cost_service = llm_cost_service

    async def get_sequence_by_id(self, sequence_id: str):
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})

        if not sequence:
            raise RuntimeError("The given sequence was not found")

        return sequence

    async def get_session_by_id(self, session_id: str):
        session = await self.db["session"].find_one({"_id": ObjectId(session_id)})

        if not session:
            raise RuntimeError("The given session was not found")

        return session

    async def require_session_owned_by_user(self, session_id: str, user_id: str) -> dict:
        """Return the session document or raise 403 if it does not belong to ``user_id``."""

        session = await self.get_session_by_id(session_id)
        stored = session.get("user_id")
        if stored is None or str(stored) != str(user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return session

    async def _set_sequence_posture_correction(
        self, session_id: str, posture_index: int, text: str, audio_path: str
    ) -> None:
        """Persist pose correction under sequence.postures[i].posture_correction for GET .../audio/{message_id}."""
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    f"sequence.postures.{posture_index}.posture_correction": {
                        "text": text,
                        "audio_path": audio_path,
                    }
                }
            },
        )

    async def submit_pose_landmarks(self, session_id: str, body: PoseLandmarksRequest) -> dict:
        """
        LLM returns optional instruction (null/empty when posture is acceptable). When non-empty, TTS is saved
        under audio_files/{session_id}/{message_id}.mp3 and stored on sequence.postures[i].posture_correction
        for the row whose client_id(s) include body.posture_client_id.
        """
        session = await self.get_session_by_id(session_id)
        postures = (session.get("sequence") or {}).get("postures") or []
        user_id_str = str(session["user_id"]) if session.get("user_id") is not None else None
        posture_index = SessionService._posture_index_for_client_id(postures, body.posture_client_id)
        if posture_index is None:
            raise ValueError(
                f"No posture in this session's sequence matches posture_client_id={body.posture_client_id!r}."
            )

        start_request_llm_cost_tracking()
        try:
            result = await self.posture_correction_agent.generate_combined_instruction(
                session_id=session_id,
                payload=body,
            )
        finally:
            total_micro = get_request_llm_cost_micro_total()
            stop_request_llm_cost_tracking()
        if self.llm_cost_service and user_id_str and total_micro > 0:
            try:
                await self.llm_cost_service.commit_delta_micro_usd(user_id_str, total_micro)
            except Exception:
                logging.exception("llm_cost commit after pose correction failed")

        instruction = result.get("instruction")
        if not instruction:
            return {"status": True, "result": {"instruction": None, "message_id": None, "audio_path": None}}

        message_id = result.get("message_id") or f"pose_corr_{uuid.uuid4().hex}"
        audio_chunks = self.yoga_coordinator.generate_audio_from_text(
            instruction,
            instructions=DEFAULT_YOGA_TTS_INSTRUCTIONS,
        )
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)
        await self._set_sequence_posture_correction(session_id, posture_index, instruction, audio_path)

        return {
            "status": True,
            "result": {**result, "message_id": message_id, "audio_path": audio_path},
        }

    def _build_audio_path(self, session_id: str, message_id: str) -> Path:
        """Build the canonical file path for an instruction's audio."""
        return Path("audio_files") / session_id / f"{message_id}.mp3"

    async def update_current_session_state(self, session_id: str, body: CurrentSessionStateRequest) -> dict:
        """
        Update `session_status` on the session document: overall play state and optional segment position
        (intro vs posture with sequence_posture_id).
        """
        await self.get_session_by_id(session_id)
        current_position = None
        if body.current_position is not None:
            current_position = body.current_position.model_dump()
        session_status = {
            "session_play_status": body.session_play_status,
            "current_position": current_position,
        }
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"session_status": session_status}},
        )
        return {"status": True, "result": {"session_status": session_status}}

    async def start_over_session(self, session_id: str) -> dict:
        """
        Reset playback to the initial state (same as a newly scripted session) and strip
        `posture_correction` from each row in `sequence.postures` so restarted practice does not reuse old clips.
        """
        session = await self.get_session_by_id(session_id)
        postures = (session.get("sequence") or {}).get("postures") or []
        postures_cleaned = [
            {k: v for k, v in p.items() if k != "posture_correction"} if isinstance(p, dict) else p
            for p in postures
        ]
        session_status = {
            "session_play_status": "not_started",
            "current_position": None,
        }
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "session_status": session_status,
                    "sequence.postures": postures_cleaned,
                }
            },
        )
        return {"status": True, "result": {"session_status": session_status}}

    async def get_session_info(self, session_id: str) -> dict:
        """
        Return the session document. `sequence.postures[i].guidance_steps` entries hold `instruction` /
        `sensory_cue` plus optional `instruction_message_id` / `instruction_audio_path` and
        `sensory_message_id` / `sensory_audio_path` when each clip exists.
        Optional `sequence.postures[i].posture_correction` holds `text` and `audio_path` for live pose feedback.
        Intro and ending are top-level `{text, message_id, audio_path}` each.
        Legacy `instructions` is omitted if present.
        """
        session = await self.get_session_by_id(session_id)
       
        return {"status": True, "result": session}

    async def get_latest_incomplete_session_for_user(self, user_id: ObjectId | str) -> dict | None:
        """
        Return ``{_id, name}`` for the user's most recently created session when its play status is
        ``not_started`` or ``in_progress``; return ``None`` when there is no session or the latest one is
        ``completed`` or ``abandoned``.
        """
        uid = user_id if isinstance(user_id, ObjectId) else ObjectId(user_id)
        doc = await self.db["session"].find_one({"user_id": uid}, sort=[("created_on", -1)])
        if doc is None:
            return None
        play_status = (doc.get("session_status") or {}).get("session_play_status")
        if play_status in ("completed", "abandoned"):
            return None
        sequence = doc.get("sequence") or {}
        sequence_name = sequence.get("name") or ""
        session_status = doc.get("session_status") or {}
        
        return {"_id": str(doc["_id"]), "name": sequence_name, "sequence": sequence, "session_status": session_status}

    @staticmethod
    def _bookend_spoken_document(text: str, message_id: str, audio_path: str) -> dict:
        """
        Persisted shape for intro and ending: one clip each, not a `steps` array.
        Keys match for both: spoken `text`, API `message_id`, on-disk `audio_path`.
        """
        return {"text": text, "message_id": message_id, "audio_path": str(audio_path)}

    @staticmethod
    def _client_ids_from_posture_row(row: dict) -> list[str]:
        """Collect client_ids from a single stored posture row."""
        ids: set[str] = set()
        intent = row.get("posture_intent")
        if intent == POSTURE_INTENT_INTERVAL_SET:
            wp = row.get("work_posture") or {}
            rp = row.get("recovery_posture") or {}
            if wp.get("client_id"):
                ids.add(wp["client_id"])
            if rp.get("client_id"):
                ids.add(rp["client_id"])
        elif intent == POSTURE_INTENT_VINYASA_LOOP:
            for slot in row.get("cycle_postures") or []:
                cid = slot.get("client_id")
                if cid:
                    ids.add(cid)
        elif row.get("client_id"):
            ids.add(row["client_id"])
        return list(ids)

    @staticmethod
    def _client_ids_from_stored_postures(postures: list) -> list[str]:
        """Collect client_ids from sequence postures (static, interval_set, vinyasa_loop)."""
        ids: set[str] = set()
        for p in postures:
            ids.update(SessionService._client_ids_from_posture_row(p))
        return list(ids)

    @staticmethod
    def _posture_index_for_client_id(postures: list, client_id: str) -> int | None:
        """Index of the first sequence posture row that includes this catalogue client_id."""
        cid = (client_id or "").strip()
        if not cid:
            return None
        for i, row in enumerate(postures or []):
            if cid in SessionService._client_ids_from_posture_row(row):
                return i
        return None

    @staticmethod
    def _transition_tts_instructions_for_target(target_row: dict, posture_docs: dict[str, dict]) -> str:
        """
        Choose energetic vs calm TTS steering for a transition into `target_row`, using posture intensity docs.
        """
        max_exertion = 0
        max_balance = 0
        for cid in SessionService._client_ids_from_posture_row(target_row):
            doc = posture_docs.get(cid) or {}
            profile = doc.get("intensity_profile") or {}
            ex = profile.get("overall_exertion")
            bal = profile.get("balance_requirement")
            if isinstance(ex, (int, float)):
                max_exertion = max(max_exertion, int(ex))
            if isinstance(bal, (int, float)):
                max_balance = max(max_balance, int(bal))
        if max_exertion >= 4 or max_balance >= 4:
            return ENERGETIC_YOGA_TTS_INSTRUCTIONS
        return DEFAULT_YOGA_TTS_INSTRUCTIONS

    def _find_instruction(self, session: dict, message_id: str) -> dict:
        """
        Return payload for TTS or streaming: `text` plus persistence keys for intro/ending/guidance clips.
        Guidance steps expose separate instruction and sensory message ids.
        """
        intro = session.get("intro")
        if isinstance(intro, dict) and intro.get("message_id") == message_id:
            return {"kind": "intro", **intro}
        ending = session.get("ending")
        if isinstance(ending, dict) and ending.get("message_id") == message_id:
            return {"kind": "ending", **ending}

        for pi, p in enumerate((session.get("sequence") or {}).get("postures") or []):
            pc = p.get("posture_correction")
            if isinstance(pc, dict):
                ap = (pc.get("audio_path") or "").strip()
                if ap and Path(ap).stem == message_id:
                    text = (pc.get("text") or "").strip()
                    return {
                        "kind": "pose_correction",
                        "text": text,
                        "message_id": message_id,
                        "posture_index": pi,
                    }
            for si, step in enumerate(p.get("guidance_steps") or []):
                if step.get("instruction_message_id") == message_id:
                    text = (step.get("instruction") or "").strip()
                    return {
                        "kind": "guidance_step",
                        "guidance_clip": "instruction",
                        "text": text,
                        "posture_index": pi,
                        "step_index": si,
                        "message_id": message_id,
                    }
                if step.get("sensory_message_id") == message_id:
                    sc = step.get("sensory_cue")
                    text = (sc or "").strip() if sc is not None else ""
                    return {
                        "kind": "guidance_step",
                        "guidance_clip": "sensory",
                        "text": text,
                        "posture_index": pi,
                        "step_index": si,
                        "message_id": message_id,
                    }

        raise RuntimeError("The given instruction was not found")

    async def _stream_chunks_from_file(self, file_path: Path, chunk_size: int = 8192):
        """Async generator that reads a file and yields raw bytes in fixed-size chunks."""
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    def _generate_audio_and_enqueue(
        self,
        text: str,
        file_path: Path,
        queue: asyncio.Queue,
        sentinel: object,
        instructions: str | None = None,
    ) -> None:
        """
        Sync worker or Producer: generate audio from text, write to file, enqueue each chunk.
        Runs in a thread to avoid blocking the event loop.
        """
        with open(file_path, "wb") as audio_file:
            for chunk in self.yoga_coordinator.generate_audio_from_text(text, instructions=instructions):
                audio_file.write(chunk)
                queue.put_nowait(chunk)

        queue.put_nowait(sentinel)

    async def _stream_generated_audio(
        self,
        session_id: str,
        message_id: str,
        text: str,
        file_path: Path,
        instructions: str | None = None,
    ):
        """
        Async generator or Consumer: run TTS in a thread, yield chunks as they are produced,
        then update the session document with the saved path.
        """
        queue = asyncio.Queue()
        sentinel = object()
        task = asyncio.create_task(
            asyncio.to_thread(self._generate_audio_and_enqueue, text, file_path, queue, sentinel, instructions)
        )

        while True:
            chunk = await queue.get()
            if chunk is sentinel:
                break
            yield chunk

        await task
        await self._persist_instruction_audio_path(session_id, message_id, file_path)

    async def _on_demand_tts_instructions(
        self, session_id: str, target: dict, session: dict | None = None
    ) -> str | None:
        """Resolve OpenAI Speech steering when regenerating a missing clip (intro energetic; instruction from row)."""
        kind = target.get("kind")
        if kind == "intro":
            return ENERGETIC_YOGA_TTS_INSTRUCTIONS
        if kind == "ending":
            return None
        if kind == "pose_correction":
            return DEFAULT_YOGA_TTS_INSTRUCTIONS
        if kind != "guidance_step":
            return None
        if target.get("guidance_clip") != "instruction":
            return None
        sess = session if session is not None else await self.get_session_by_id(session_id)
        pi = target["posture_index"]
        rows = (sess.get("sequence") or {}).get("postures") or []
        if pi < 0 or pi >= len(rows):
            return None
        row = rows[pi]
        client_ids = self._client_ids_from_posture_row(row)
        posture_docs = {}
        if client_ids:
            async for doc in self.db["postures"].find({"client_id": {"$in": client_ids}}):
                posture_docs[doc["client_id"]] = doc
        return self._transition_tts_instructions_for_target(row, posture_docs)

    async def _stream_audio_when_missing(
        self, session_id: str, message_id: str, target: dict, audio_path: Path, session: dict | None = None
    ):
        """
        Async generator for the case when the audio file does not exist yet.
        Validates target has text, creates directory, generates and streams audio.
        """
        text = target.get("text")

        if not text:
            raise RuntimeError("Instruction has no text to generate audio from")

        audio_path.parent.mkdir(parents=True, exist_ok=True)
        tts_instructions = await self._on_demand_tts_instructions(session_id, target, session)
        async for chunk in self._stream_generated_audio(
            session_id, message_id, text, audio_path, instructions=tts_instructions
        ):
            yield chunk

    async def _persist_instruction_audio_path(self, session_id: str, message_id: str, file_path: Path) -> None:
        """Persist audio_path for `intro`, `ending`, or a `guidance_steps` item after on-demand TTS."""
        session = await self.get_session_by_id(session_id)
        payload = self._find_instruction(session, message_id)
        if payload.get("kind") == "guidance_step":
            pi = payload["posture_index"]
            si = payload["step_index"]
            clip = payload.get("guidance_clip")
            if clip == "instruction":
                path_key = "instruction_audio_path"
            elif clip == "sensory":
                path_key = "sensory_audio_path"
            else:
                raise RuntimeError("guidance_step missing guidance_clip for audio path update")
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {f"sequence.postures.{pi}.guidance_steps.{si}.{path_key}": str(file_path)}},
            )
            return
        if payload.get("kind") == "intro":
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"intro.audio_path": str(file_path)}},
            )
            return
        if payload.get("kind") == "ending":
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"ending.audio_path": str(file_path)}},
            )
            return
        if payload.get("kind") == "pose_correction":
            pi = payload.get("posture_index")
            if pi is None:
                raise RuntimeError("pose_correction payload missing posture_index for audio path update")
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {f"sequence.postures.{pi}.posture_correction.audio_path": str(file_path)}},
            )
            return
        raise RuntimeError("Unknown instruction payload kind for audio path update")

    async def get_audio_chunks(self, session_id: str, message_id: str):
        """
        Async generator yielding audio chunks. Serves from disk if present,
        otherwise generates on-demand, saves, and streams chunks in real time.
        """
        audio_path = self._build_audio_path(session_id, message_id)

        if audio_path.exists():
            async for chunk in self._stream_chunks_from_file(audio_path):
                yield chunk

            return

        session = await self.get_session_by_id(session_id)
        target = self._find_instruction(session, message_id)

        async for chunk in self._stream_audio_when_missing(
            session_id, message_id, target, audio_path, session
        ):
            yield chunk

    def _save_audio_to_file(self, session_id: str, message_id: str, audio_chunks) -> str:
        """Save audio chunks to file and return the file path."""
        audio_dir = Path("audio_files") / session_id
        audio_dir.mkdir(parents=True, exist_ok=True)
        audio_path = audio_dir / f"{message_id}.mp3"

        with open(audio_path, "wb") as audio_file:
            for chunk in audio_chunks:
                audio_file.write(chunk)

        return str(audio_path)

    async def _generate_intro(
        self, sequence_name: str, session_id: str, user_name: str, user_id: str | None = None
    ) -> None:
        """Generate intro copy and TTS; store a single flat `intro` object (same shape as `ending`, not `steps`)."""
        prompt = get_introduction_prompt(sequence_name=sequence_name, user_name=user_name)
        response = await self.yoga_coordinator.generate_intro_or_ending(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_coordinator.generate_audio_from_text(
            text, instructions=ENERGETIC_YOGA_TTS_INSTRUCTIONS
        )
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)
        doc = self._bookend_spoken_document(text, message_id, audio_path)

        trace("Saving intro", session_id=session_id)
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"intro": doc}},
        )

    async def _generate_transitions(self, postures: list, session_id: str, user_id: str | None = None) -> None:
        """Generate transition guidance steps and audio; persist on embedded sequence.postures[idx].guidance_steps."""
        client_ids = self._client_ids_from_stored_postures(postures)
        posture_docs = {}
        if client_ids:
            async for doc in self.db["postures"].find({"client_id": {"$in": client_ids}}):
                posture_docs[doc["client_id"]] = doc
        sensory_cues_map = {cid: (doc.get("sensory_cues") or []) for cid, doc in posture_docs.items()}

        for idx in range(len(postures)):
            req = build_transition_request(idx, postures, sensory_cues_map)
            if req is None:
                continue
            if req.expected_step_count <= 0:
                continue

            response = await self.yoga_coordinator.generate_transition_guidance(req, user_id=user_id)
            base_message_id = response["message_id"]
            raw_steps = response["steps"]
            target_row = postures[idx]
            transition_instructions = self._transition_tts_instructions_for_target(target_row, posture_docs)

            guidance_steps = []
            for i, step in enumerate(raw_steps):
                row: dict = {
                    "instruction": step.get("instruction"),
                    "sensory_cue": step.get("sensory_cue"),
                }
                inst_text = (step.get("instruction") or "").strip()
                sensory_raw = step.get("sensory_cue")
                sensory_text = (sensory_raw or "").strip() if sensory_raw is not None else ""

                if inst_text:
                    iid = f"{base_message_id}_step{i}_instruction"
                    ichunks = self.yoga_coordinator.generate_audio_from_text(
                        inst_text, instructions=transition_instructions
                    )
                    row["instruction_message_id"] = iid
                    row["instruction_audio_path"] = self._save_audio_to_file(session_id, iid, ichunks)
                else:
                    row["instruction_message_id"] = None
                    row["instruction_audio_path"] = None

                if sensory_text:
                    sid = f"{base_message_id}_step{i}_sensory"
                    schunks = self.yoga_coordinator.generate_audio_from_text(sensory_text)
                    row["sensory_message_id"] = sid
                    row["sensory_audio_path"] = self._save_audio_to_file(session_id, sid, schunks)
                else:
                    row["sensory_message_id"] = None
                    row["sensory_audio_path"] = None

                guidance_steps.append(row)

            trace(f"Saving transition guidance: idx={idx}", session_id=session_id)
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {f"sequence.postures.{idx}.guidance_steps": guidance_steps}},
            )

    async def _generate_ending_note(self, sequence_name: str, session_id: str, user_id: str | None = None) -> None:
        """Generate ending copy and TTS; store a single flat `ending` object (identical keys to `intro`, not `steps`)."""
        prompt = get_ending_prompt(sequence_name=sequence_name)
        response = await self.yoga_coordinator.generate_intro_or_ending(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_coordinator.generate_audio_from_text(text)
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)
        doc = self._bookend_spoken_document(text, message_id, audio_path)

        trace("Saving ending note", session_id=session_id)
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"ending": doc, "generation_status": "completed"}},
        )

    async def _generate_remaining_guidance_background(
        self, session_id: str, postures: list, sequence_name: str, user_name: str, user_id: str | None = None
    ) -> None:
        """Generate intro, transitions, and ending; accumulate LLM cost via ContextVar; commit on full success."""
        start_request_llm_cost_tracking()
        try:
            await self._generate_intro(sequence_name, session_id, user_name, user_id)
            await self._generate_transitions(postures, session_id, user_id)
            await self._generate_ending_note(sequence_name, session_id, user_id)
        except Exception:
            logging.exception("session guidance background task failed")
        else:
            total = get_request_llm_cost_micro_total()
            if self.llm_cost_service and user_id and total > 0:
                try:
                    await self.llm_cost_service.commit_delta_micro_usd(str(user_id), total)
                except Exception:
                    logging.exception("llm_cost commit after session guidance failed")
        finally:
            stop_request_llm_cost_tracking()

    def _create_session_document(self, user_id: str, sequence: dict) -> dict:
        """Create session document; `intro` and `ending` are set when background generation completes."""
        current_timestamp = datetime.utcnow()
        postures = sequence["postures"]

        return {
            "user_id": ObjectId(user_id),
            "sequence": sequence,
            "created_on": current_timestamp,
            "total_number_of_postures": len(postures),
            "generation_status": "in_progress",
            "session_status": {
                "session_play_status": "not_started",
                "current_position": None,
            },
        }

    async def start_user_session(self, user_id: str, sequence_id: str, user_name: str):
        """
        Start a new yoga session by pre-generating intro text and audio,
        then scheduling background generation for transitions and ending.
        """
        trace("Session starting now", session_id=None)
        sequence = await self.get_sequence_by_id(sequence_id)
        seq_uid = sequence.get("user_id")
        if seq_uid is None or str(seq_uid) != str(user_id):
            raise ValueError("Sequence not found or access denied")
        postures = sequence["postures"]

        session_doc = self._create_session_document(user_id, sequence)
        session_created = await self.db["session"].insert_one(session_doc)

        if not session_created:
            raise RuntimeError("Failed to create session")

        session_id_str = str(session_created.inserted_id)

        user_id_str = str(user_id)
        asyncio.create_task(self._generate_remaining_guidance_background(session_id_str, postures, sequence["name"], user_name, user_id_str))

        trace("Session started", session_id=session_id_str)
        return {
            "status": True,
            "session_id": session_id_str,
            "sequence": sequence,
            "generation_status": "in_progress",
        }
