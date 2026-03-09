from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from pathlib import Path
from datetime import datetime

from app.prompts.prompts import _get_transition_query_prompt, _get_start_user_session_prompt, _get_user_query_prompt

from app.globals.functions import serialize_mongo_output


class QueryService:
    def __init__(self, db: AsyncIOMotorDatabase, session_service, yoga_agent):
        self.db = db
        self.session_service = session_service
        self.yoga_agent = yoga_agent

    async def process_user_query(
        self, user_query: str, session_id: str, postures: list, current_posture_name, chat_history: list
    ):
        prompt = _get_user_query_prompt(
            postures=postures, current_posture=current_posture_name, chat_history=chat_history, user_query=user_query
        )
        llm_response = self.yoga_agent.generate_text(prompt=prompt)
        llm_response_message_id = llm_response["message_id"]
        llm_response_text = llm_response["text"]

        # self._save_audio_response(llm_response_text, llm_response_message_id)
        # return StreamingResponse(self._save_audio_response(llm_response_text), media_type="audio/mpeg") // For streaming audio directly

        update_argument = {
            "$push": {
                "chat_history.messages": {
                    "human": user_query,
                    "ai": llm_response_text,
                    "message_id": llm_response_message_id,
                }
            }
        }
        await self.session_service.update_session(session_id=session_id, update_argument=update_argument)

        return {
            "status": True,
            "type": "query_response",
            "result": {"text": llm_response_text, "msgId": llm_response_message_id},
        }

    def _validate_transition_query(self, transition_from_idx: int, postures: list):
        if transition_from_idx < -1 or transition_from_idx >= len(postures) - 1:
            raise ValueError("Invalid transition index")

        return True

    async def process_transition_query(
        self, transition_from_idx: int, session_id: str, postures: list, chat_history: list
    ):
        self._validate_transition_query(transition_from_idx=transition_from_idx, postures=postures)

        prompt = _get_transition_query_prompt(
            transition_from_idx=transition_from_idx, postures=postures, chat_history=chat_history
        )
        llm_response = self.yoga_agent.generate_text(prompt=prompt)
        llm_response_message_id = llm_response["message_id"]
        llm_response_text = llm_response["text"]

        # self._save_audio_response(llm_response_text, llm_response_message_id)
        # return StreamingResponse(self._save_audio_response(llm_response_text), media_type="audio/mpeg") // For streaming audio directly

        current_timestamp = datetime.utcnow()
        current_posture = {**postures[transition_from_idx + 1], "idx": transition_from_idx + 1}
        update_argument = {
            "$push": {
                "chat_history.messages": {
                    "human": "Please narrate the transition from current posture to the next one",
                    "ai": llm_response_text,
                    "message_id": llm_response_message_id,
                }
            },
            "$set": {"current_posture": current_posture},
        }
        await self.session_service.update_session(session_id=session_id, update_argument=update_argument)

        return {
            "status": True,
            "session_id": session_id,
            "posture": serialize_mongo_output(current_posture),
            "type": "transition_response",
            "result": {"text": llm_response_text, "msgId": llm_response_message_id},
        }

    async def start_user_session(self, user_id: str, sequence_id):
        sequence = await self.session_service.get_sequence_by_id(sequence_id=sequence_id)

        prompt = _get_start_user_session_prompt(sequence_name=sequence["name"])
        llm_response = self.yoga_agent.generate_text(prompt=prompt)
        llm_response_message_id = llm_response["message_id"]
        llm_response_text = llm_response["text"]

        chat_history = {
            "messages": [
                {
                    "human": "Please start the yoga session",
                    "ai": llm_response_text,
                    "message_id": llm_response_message_id,
                }
            ]
        }
        session_id = await self.session_service.create_new_session(
            user_id=user_id, sequence=sequence, chat_history=chat_history
        )

        return {
            "status": True,
            "type": "session_started",
            "session_id": str(session_id),
            "result": {"text": llm_response_text, "msgId": llm_response_message_id},
        }

    async def end_user_session(self, session_id: str):
        session = await self.session_service.get_session_by_id(session_id=session_id)

        prompt = self._get_end_user_session_prompt(session_name=session["sequence"]["name"])
        llm_response = self.yoga_agent.generate_text(prompt=prompt)
        llm_response_message_id = llm_response["message_id"]
        llm_response_text = llm_response["text"]

        await self.session_service.end_session(session_id)

        return {
            "status": True,
            "type": "session_ended",
            "session_id": str(session_id),
            "result": {"text": llm_response_text, "msgId": llm_response_message_id},
        }
