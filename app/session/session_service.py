import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.prompts.ending import get_ending_prompt
from app.prompts.introduction import get_introduction_prompt
from app.prompts.transition import get_transition_prompt
from app.session.session_trace_logger import trace


class SessionService:
    def __init__(self, db: AsyncIOMotorDatabase, yoga_agent):
        self.db = db
        self.yoga_agent = yoga_agent

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
        """Return session document excluding the instructions field."""
        session = await self.get_session_by_id(session_id)
        session = {k: v for k, v in session.items() if k != "instructions"}
        return {"status": True, "result": session}

    async def get_instructions(self, session_id: str) -> list:
        """Return instructions for a session, excluding audio_path from each instruction."""
        session = await self.get_session_by_id(session_id)
        instructions = session.get("instructions") or []
        return [{k: v for k, v in i.items() if k != "audio_path"} for i in instructions]

    def _find_instruction(self, session: dict, message_id: str) -> dict:
        """Return the instruction matching message_id, or raise if not found."""
        instructions = session.get("instructions") or []
        instruction = next((i for i in instructions if i.get("message_id") == message_id), None)

        if not instruction:
            raise RuntimeError("The given instruction was not found")

        return instruction

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
            for chunk in self.yoga_agent.generate_audio_from_text(text):
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
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id), "instructions.message_id": message_id},
            {"$set": {"instructions.$.audio_path": str(file_path)}},
        )

    async def _stream_audio_when_missing(self, session_id: str, message_id: str, instruction: dict, audio_path: Path):
        """
        Async generator for the case when the audio file does not exist yet.
        Validates instruction has text, creates directory, generates and streams audio.
        """
        text = instruction.get("text")

        if not text:
            raise RuntimeError("Instruction has no text to generate audio from")

        audio_path.parent.mkdir(parents=True, exist_ok=True)
        async for chunk in self._stream_generated_audio(session_id, message_id, text, audio_path):
            yield chunk

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
        instruction = self._find_instruction(session, message_id)

        async for chunk in self._stream_audio_when_missing(session_id, message_id, instruction, audio_path):
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
        """Generate introduction micro-instructions and audio, store as flat array with category=introduction."""
        prompt = get_introduction_prompt(sequence_name=sequence_name, user_name=user_name)
        response = await self.yoga_agent.generate_text(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_agent.generate_audio_from_text(text)
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)

        trace("Saving intro", session_id=session_id)
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$push": {"instructions": {"category": "intro", "text": text, "message_id": message_id, "audio_path": audio_path}}},
        )

    async def _generate_transitions(
        self, postures: list, session_id: str, user_id: str | None = None
    ) -> None:
        """Generate transition micro-instructions and audio, store as flat array with category=transition."""
        for from_idx in range(-1, len(postures) - 1):
            transition_prompt = get_transition_prompt(transition_from_idx=from_idx, postures=postures)
            response = await self.yoga_agent.generate_structured_text(prompt=transition_prompt, user_id=user_id)
            instructions = response["instructions"]
            base_message_id = response["message_id"]

            flat_items = []
            for i, micro in enumerate(instructions):
                message_id = f"{base_message_id}_{i}"
                audio_chunks = self.yoga_agent.generate_audio_from_text(micro["text"])
                audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)
                flat_items.append({
                    "category": "transition",
                    "type": micro["type"],
                    "text": micro["text"],
                    "message_id": message_id,
                    "audio_path": audio_path,
                })

            trace(f"Saving transition: from_idx={from_idx}", session_id=session_id)
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$push": {"instructions": {"$each": flat_items}}},
            )

    async def _generate_ending_note(
        self, sequence_name: str, session_id: str, user_id: str | None = None
    ) -> None:
        """Generate ending micro-instructions and audio, store as flat array with category=ending."""
        prompt = get_ending_prompt(sequence_name=sequence_name)
        response = await self.yoga_agent.generate_text(prompt=prompt, user_id=user_id)
        text = response["text"]
        message_id = response["message_id"]
        audio_chunks = self.yoga_agent.generate_audio_from_text(text)
        audio_path = self._save_audio_to_file(session_id, message_id, audio_chunks)

        trace("Saving ending note", session_id=session_id)
        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {
                "$push": {"instructions": {"category": "ending", "text": text, "message_id": message_id, "audio_path": audio_path}}, 
                "$set": {"generation_status": "completed"}
            }
        )

    async def _generate_remaining_guidance_background(
        self, session_id: str, postures: list, sequence_name: str, user_name: str, user_id: str | None = None
    ):
        """Generate transitions and ending text, then generate audio in background."""
        await self._generate_intro(sequence_name, session_id, user_name, user_id)
        await self._generate_transitions(postures, session_id, user_id)
        await self._generate_ending_note(sequence_name, session_id, user_id)

    def _create_session_document(self, user_id: str, sequence: dict) -> dict:
        """Create session document with intro only"""
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
        asyncio.create_task(
            self._generate_remaining_guidance_background(session_id_str, postures, sequence["name"], user_name, user_id_str)
        )

        trace("Session started", session_id=session_id_str)
        return {
                "status": True,
                "session_id": session_id_str,
                "sequence": sequence,
                "generation_status": "in_progress",
        }
