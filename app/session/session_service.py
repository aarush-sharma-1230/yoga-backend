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
        Return the session document. Transition guidance uses `sequence.postures[i].guidance_steps` (arrays).
        Intro and ending are top-level single objects `{text, message_id, audio_path}` each—no `steps`.
        Legacy `instructions` is omitted if present.
        """
        session = await self.get_session_by_id(session_id)
       
        return {"status": True, "result": session}

    @staticmethod
    def _bookend_spoken_document(text: str, message_id: str, audio_path: str) -> dict:
        """
        Persisted shape for intro and ending: one clip each, not a `steps` array.
        Keys match for both: spoken `text`, API `message_id`, on-disk `audio_path`.
        """
        return {"text": text, "message_id": message_id, "audio_path": str(audio_path)}

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
        intro = session.get("intro")
        if isinstance(intro, dict) and intro.get("message_id") == message_id:
            return {"kind": "intro", **intro}
        ending = session.get("ending")
        if isinstance(ending, dict) and ending.get("message_id") == message_id:
            return {"kind": "ending", **ending}

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
        """Persist audio_path for `intro`, `ending`, or a `guidance_steps` item after on-demand TTS."""
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
        """Generate intro copy and TTS; store a single flat `intro` object (same shape as `ending`, not `steps`)."""
        prompt = get_introduction_prompt(sequence_name=sequence_name, user_name=user_name)
        response = await self.yoga_coordinator.generate_intro_or_ending(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_coordinator.generate_audio_from_text(text)
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

    async def _generate_remaining_guidance_background(self, session_id: str, postures: list, sequence_name: str, user_name: str, user_id: str | None = None) -> None:
        """Generate transitions and ending text, then generate audio in background."""
        await self._generate_intro(sequence_name, session_id, user_name, user_id)
        await self._generate_transitions(postures, session_id, user_id)
        await self._generate_ending_note(sequence_name, session_id, user_id)

    def _create_session_document(self, user_id: str, sequence: dict) -> dict:
        """Create session document; `intro` and `ending` are set when background generation completes."""
        current_timestamp = datetime.utcnow()
        postures = sequence["postures"]

        return {
            "user_id": user_id,
            "sequence": sequence,
            "created_on": current_timestamp,
            "current_posture": None,
            "total_number_of_postures": len(postures),
            "generation_status": "in_progress",
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
