import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.prompts.prompts import (
    _get_start_user_session_prompt,
    _get_transition_query_prompt,
    _get_end_user_session_prompt,
)


class SessionService:
    def __init__(self, db: AsyncIOMotorDatabase, yoga_agent):
        self.db = db
        self.yoga_agent = yoga_agent

    async def get_session_by_id(self, session_id: str):
        session = await self.db["session"].find_one({"_id": ObjectId(session_id)})

        if not session:
            raise RuntimeError("The given session was not found")

        return session

    def _find_instruction(self, session: dict, message_id: str) -> dict:
        """Return the instruction matching message_id, or raise if not found."""
        instructions = session.get("instructions") or []
        instruction = next((i for i in instructions if i.get("message_id") == message_id), None)
        if not instruction:
            raise RuntimeError("The given instruction was not found")
        return instruction

    def _build_audio_path(self, session_id: str, message_id: str) -> Path:
        """Build the canonical file path for an instruction's audio."""
        return Path("audio_files") / session_id / f"{message_id}.mp3"

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

    async def get_sequence_by_id(self, sequence_id: str):
        sequence = await self.db["sequences"].find_one({"_id": ObjectId(sequence_id)})

        if not sequence:
            raise RuntimeError("The given sequence was not found")

        return sequence

    async def create_new_session(self, user_id: str, sequence, chat_history):
        current_timestamp = datetime.utcnow()
        current_posture = None  # {**sequence["postures"][0], "idx": 0, "started_on": current_timestamp}

        session = {
            "user_id": user_id,
            "sequence": sequence,
            "created_on": current_timestamp,
            "chat_history": chat_history,
            "current_posture": current_posture,
            "total_number_of_postures": len(sequence["postures"]),
        }

        session_created = await self.db["session"].insert_one(session)

        if not session_created:
            raise RuntimeError("Failed to create session")

        return session_created.inserted_id

    async def update_session(self, session_id: str, update_argument):
        await self.db["session"].update_one({"_id": ObjectId(session_id)}, update_argument)

    async def end_session(self, session_id: str):
        update_argument = {
            "ended_on": datetime.utcnow(),
            "status": "completed",
            "current_posture": None,
        }

        await self.update_session(session_id=session_id, update_argument=update_argument)

    def _generate_intro_text(self, sequence_name: str) -> dict:
        """Generate introduction text for the session."""
        prompt = _get_start_user_session_prompt(sequence_name=sequence_name)
        response = self.yoga_agent.generate_text(prompt=prompt)
        return {"type": "intro", "text": response["text"], "message_id": response["message_id"]}

    def _generate_transition_texts(self, postures: list) -> list:
        """Generate all transition texts for the sequence."""
        transitions = []

        for from_idx in range(-1, len(postures) - 1):
            to_idx = from_idx + 1
            transition_prompt = _get_transition_query_prompt(transition_from_idx=from_idx, postures=postures)
            transition_response = self.yoga_agent.generate_text(prompt=transition_prompt)
            transitions.append(
                {
                    "type": "transition",
                    "from_idx": from_idx,
                    "to_idx": to_idx,
                    "text": transition_response["text"],
                    "message_id": transition_response["message_id"],
                }
            )

        return transitions

    def _generate_ending_text(self, sequence_name: str) -> dict:
        """Generate ending text for the session."""
        prompt = _get_end_user_session_prompt(sequence_name=sequence_name)
        response = self.yoga_agent.generate_text(prompt=prompt)
        return {"type": "ending", "text": response["text"], "message_id": response["message_id"]}

    def _save_audio_to_file(self, session_id: str, message_id: str, audio_chunks) -> str:
        """Save audio chunks to file and return the file path."""
        audio_dir = Path("audio_files") / session_id
        audio_dir.mkdir(parents=True, exist_ok=True)

        audio_path = audio_dir / f"{message_id}.mp3"

        with open(audio_path, "wb") as audio_file:
            for chunk in audio_chunks:
                audio_file.write(chunk)

        return str(audio_path)

    def _generate_and_save_audio(self, session_id: str, text: str, message_id: str) -> str:
        """Generate audio from text and save to file."""
        audio_chunks = self.yoga_agent.generate_audio_from_text(text)
        return self._save_audio_to_file(session_id, message_id, audio_chunks)

    async def _generate_and_save_intro_audio(self, session_id: str, intro: dict) -> dict:
        """Generate intro audio, save to file, and update database."""
        intro_audio_path = self._generate_and_save_audio(
            session_id, intro["text"], intro["message_id"]
        )
        intro["audio_path"] = intro_audio_path

        await self.db["session"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"instructions.0.audio_path": intro_audio_path}},
        )

        return intro

    def _create_session_document(self, user_id: str, sequence: dict, intro: dict) -> dict:
        """Create session document with intro only"""
        current_timestamp = datetime.utcnow()
        postures = sequence["postures"]

        return {
            "user_id": user_id,
            "sequence": sequence,
            "created_on": current_timestamp,
            "current_posture": None,
            "total_number_of_postures": len(postures),
            "instructions": [intro],
        }

    async def _generate_remaining_guidance_background(self, session_id: str, postures: list, sequence_name: str):
        """Generate transitions and ending text, then generate audio in background."""
        try:
            transitions = self._generate_transition_texts(postures)
            ending = self._generate_ending_text(sequence_name)

            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {
                    "$push": {"instructions": {"$each": transitions + [ending]}},
                    "$set": {"generation_status": "text_completed"},
                },
            )

            asyncio.create_task(self._generate_audio_background(session_id, transitions + [ending]))
        except Exception as e:
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)}, {"$set": {"generation_status": "failed", "generation_error": str(e)}}
            )

    async def _generate_audio_background(self, session_id: str, instructions: list):
        """Generate and save audio for instructions in background."""
        try:
            for instruction in instructions:
                audio_path = self._generate_and_save_audio(session_id, instruction["text"], instruction["message_id"])

                await self.db["session"].update_one(
                    {
                        "_id": ObjectId(session_id),
                        "instructions.message_id": instruction["message_id"],
                    },
                    {"$set": {"instructions.$.audio_path": audio_path}},
                )

            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)}, {"$set": {"generation_status": "completed"}}
            )
        except Exception as e:
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"generation_status": "audio_failed", "audio_error": str(e)}},
            )

    async def start_user_session(self, user_id: str, sequence_id: str):
        """
        Start a new yoga session by pre-generating intro text and audio,
        then scheduling background generation for transitions and ending.
        """
        sequence = await self.get_sequence_by_id(sequence_id)
        postures = sequence["postures"]

        intro = self._generate_intro_text(sequence["name"])
        session_doc = self._create_session_document(user_id, sequence, intro)
        session_created = await self.db["session"].insert_one(session_doc)

        if not session_created:
            raise RuntimeError("Failed to create session")

        session_id_str = str(session_created.inserted_id)

        try:
            intro = await self._generate_and_save_intro_audio(session_id_str, intro)

            asyncio.create_task(self._generate_remaining_guidance_background(session_id_str, postures, sequence["name"]))

            return {
                "status": True,
                "type": "session_started",
                "session_id": session_id_str,
                "instructions": [intro],
                "sequence": sequence,
                "generation_status": "in_progress",
            }
        except Exception as e:
            await self.db["session"].update_one(
                {"_id": ObjectId(session_id_str)},
                {"$set": {"generation_status": "failed", "generation_error": str(e)}},
            )
            raise
