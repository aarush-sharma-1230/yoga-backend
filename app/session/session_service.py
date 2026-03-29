import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.prompts.active import (
    get_ending_prompt,
    get_introduction_prompt,
)
from app.schemas.custom_sequence import (
    POSTURE_INTENT_INTERVAL_SET,
    POSTURE_INTENT_STATIC_HOLD,
    POSTURE_INTENT_VINYASA_LOOP,
)
from app.session.session_trace_logger import trace
from app.session.transition_request import build_transition_request


class SessionService:
    def __init__(self, db: AsyncIOMotorDatabase, yoga_coordinator):
        self.db = db
        self.yoga_coordinator = yoga_coordinator

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

    def _build_audio_path(self, session_id: str, message_id: str) -> Path:
        """Build the canonical file path for an instruction's audio."""
        return Path("audio_files") / session_id / f"{message_id}.mp3"

    async def get_session_info(self, session_id: str) -> dict:
        """
        Return session document excluding the flat `instructions` array.
        Spoken transition guidance is stored per posture on `sequence.postures[i].guidance_steps`;
        intro and ending remain in `instructions` on the document (omitted here).
        """
        session = await self.get_session_by_id(session_id)
        session = {k: v for k, v in session.items() if k != "instructions"}
        return {"status": True, "result": session}

    async def get_instructions(self, session_id: str) -> dict:
        """
        Return intro/ending rows from `instructions` plus per-posture `guidance_steps` (without audio_path).

        Transitions are no longer flattened into `instructions`; clients should read `posture_guidance`.
        """
        session = await self.get_session_by_id(session_id)
        flat = session.get("instructions") or []
        intro_ending = [
            {k: v for k, v in i.items() if k != "audio_path"}
            for i in flat
            if i.get("category") in ("intro", "ending")
        ]
        postures = (session.get("sequence") or {}).get("postures") or []
        posture_guidance = []
        for i, p in enumerate(postures):
            steps = p.get("guidance_steps") or []
            posture_guidance.append(
                {
                    "posture_index": i,
                    **SessionService._posture_identity_for_client(p),
                    "guidance_steps": [{k: v for k, v in s.items() if k != "audio_path"} for s in steps],
                }
            )
        return {"instructions": intro_ending, "posture_guidance": posture_guidance}

    @staticmethod
    def _posture_identity_for_client(p: dict) -> dict:
        """Fields the client can use to match a guidance block to a sequence row (client_id varies by intent)."""
        intent = p.get("posture_intent") or POSTURE_INTENT_STATIC_HOLD
        if intent == POSTURE_INTENT_INTERVAL_SET:
            wp = p.get("work_posture") or {}
            rp = p.get("recovery_posture") or {}
            return {
                "posture_intent": intent,
                "client_id": wp.get("client_id"),
                "work_client_id": wp.get("client_id"),
                "recovery_client_id": rp.get("client_id"),
            }
        if intent == POSTURE_INTENT_VINYASA_LOOP:
            cycle_ids = [x.get("client_id") for x in (p.get("cycle_postures") or []) if x.get("client_id")]
            return {
                "posture_intent": intent,
                "client_id": cycle_ids[0] if cycle_ids else None,
                "cycle_client_ids": cycle_ids,
            }
        return {"posture_intent": intent, "client_id": p.get("client_id")}

    @staticmethod
    def _client_ids_from_stored_postures(postures: list) -> list[str]:
        """Collect client_ids from sequence postures (static, interval_set, vinyasa_loop)."""
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

    @staticmethod
    def _spoken_text_from_guidance_step(step: dict) -> str:
        """Compose TTS text from a transition guidance step."""
        inst = (step.get("instruction") or "").strip()
        sensory = (step.get("sensory_cue") or "").strip()
        if sensory:
            return f"{inst} {sensory}".strip()
        return inst

    def _find_instruction(self, session: dict, message_id: str) -> dict:
        """Return a dict with `text` for TTS and enough context to persist audio_path after generation."""
        instructions = session.get("instructions") or []
        for i in instructions:
            if i.get("message_id") == message_id:
                return {"kind": "flat", **i}

        for pi, p in enumerate((session.get("sequence") or {}).get("postures") or []):
            for si, step in enumerate(p.get("guidance_steps") or []):
                if step.get("message_id") == message_id:
                    text = self._spoken_text_from_guidance_step(step)
                    return {
                        "kind": "guidance_step",
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

    def _generate_audio_and_enqueue(self, text: str, file_path: Path, queue: asyncio.Queue, sentinel: object) -> None:
        """
        Sync worker or Producer: generate audio from text, write to file, enqueue each chunk.
        Runs in a thread to avoid blocking the event loop.
        """
        with open(file_path, "wb") as audio_file:
            for chunk in self.yoga_coordinator.generate_audio_from_text(text):
                audio_file.write(chunk)
                queue.put_nowait(chunk)

        queue.put_nowait(sentinel)

    async def _stream_generated_audio(self, session_id: str, message_id: str, text: str, file_path: Path):
        """
        Async generator or Consumer: run TTS in a thread, yield chunks as they are produced,
        then update the session document with the saved path.
        """
        queue = asyncio.Queue()
        sentinel = object()
        task = asyncio.create_task(asyncio.to_thread(self._generate_audio_and_enqueue, text, file_path, queue, sentinel))

        while True:
            chunk = await queue.get()
            if chunk is sentinel:
                break
            yield chunk

        await task
        await self._persist_instruction_audio_path(session_id, message_id, file_path)

    async def _stream_audio_when_missing(self, session_id: str, message_id: str, target: dict, audio_path: Path):
        """
        Async generator for the case when the audio file does not exist yet.
        Validates target has text, creates directory, generates and streams audio.
        """
        text = target.get("text")

        if not text:
            raise RuntimeError("Instruction has no text to generate audio from")

        audio_path.parent.mkdir(parents=True, exist_ok=True)
        async for chunk in self._stream_generated_audio(session_id, message_id, text, audio_path):
            yield chunk

    async def _persist_instruction_audio_path(self, session_id: str, message_id: str, file_path: Path) -> None:
        """Write audio_path onto the flat instruction row or nested guidance_step."""
        session = await self.get_session_by_id(session_id)
        payload = self._find_instruction(session, message_id)
        if payload.get("kind") == "guidance_step":
            pi = payload["posture_index"]
            si = payload["step_index"]
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {f"sequence.postures.{pi}.guidance_steps.{si}.audio_path": str(file_path)}},
            )
            return
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id), "instructions.message_id": message_id},
            {"$set": {"instructions.$.audio_path": str(file_path)}},
        )

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

        async for chunk in self._stream_audio_when_missing(session_id, message_id, target, audio_path):
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

    async def _generate_intro(self, sequence_name: str, session_id: str, user_name: str, user_id: str | None = None) -> None:
        """Generate introduction micro-instructions and audio, store as flat array with category=introduction."""
        prompt = get_introduction_prompt(sequence_name=sequence_name, user_name=user_name)
        response = await self.yoga_coordinator.generate_text(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_coordinator.generate_audio_from_text(text)
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)

        trace("Saving intro", session_id=session_id)
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$push": {"instructions": {"category": "intro", "text": text, "message_id": message_id, "audio_path": audio_path}}},
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

            guidance_steps = []
            for i, step in enumerate(raw_steps):
                message_id = f"{base_message_id}_step{i}"
                text = self._spoken_text_from_guidance_step(step)
                audio_chunks = self.yoga_coordinator.generate_audio_from_text(text)
                audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)
                guidance_steps.append(
                    {
                        "instruction": step.get("instruction"),
                        "sensory_cue": step.get("sensory_cue"),
                        "message_id": message_id,
                        "audio_path": audio_path,
                    }
                )

            trace(f"Saving transition guidance: idx={idx}", session_id=session_id)
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {f"sequence.postures.{idx}.guidance_steps": guidance_steps}},
            )

    async def _generate_ending_note(self, sequence_name: str, session_id: str, user_id: str | None = None) -> None:
        """Generate ending micro-instructions and audio, store as flat array with category=ending."""
        prompt = get_ending_prompt(sequence_name=sequence_name)
        response = await self.yoga_coordinator.generate_text(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_coordinator.generate_audio_from_text(text)
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)

        trace("Saving ending note", session_id=session_id)
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$push": {"instructions": {"category": "ending", "text": text, "message_id": message_id, "audio_path": audio_path}}, "$set": {"generation_status": "completed"}},
        )

    async def _generate_remaining_guidance_background(self, session_id: str, postures: list, sequence_name: str, user_name: str, user_id: str | None = None) -> None:
        """Generate transitions and ending text, then generate audio in background."""
        await self._generate_intro(sequence_name, session_id, user_name, user_id)
        await self._generate_transitions(postures, session_id, user_id)
        await self._generate_ending_note(sequence_name, session_id, user_id)

    def _create_session_document(self, user_id: str, sequence: dict) -> dict:
        """Create session document with intro only."""
        current_timestamp = datetime.utcnow()
        postures = sequence["postures"]

        return {
            "user_id": user_id,
            "sequence": sequence,
            "created_on": current_timestamp,
            "current_posture": None,
            "total_number_of_postures": len(postures),
            "generation_status": "in_progress",
            "instructions": [],
        }

    async def start_user_session(self, user_id: str, sequence_id: str, user_name: str):
        """
        Start a new yoga session by pre-generating intro text and audio,
        then scheduling background generation for transitions and ending.
        """
        trace("Session starting now", session_id=None)
        sequence = await self.get_sequence_by_id(sequence_id)
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
