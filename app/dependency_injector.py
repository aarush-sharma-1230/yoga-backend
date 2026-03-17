from fastapi import Depends

from app.agents.sequence_composer import SequenceComposer
from app.agents.summary_agent import SummaryAgent
from app.agents.yoga_coordinator import YogaCoordinator
from app.auth.auth_service import AuthService
from app.database.mongo import MongoDB
from app.llms.openai_client import OpenAIClient
from app.query.query_service import QueryService
from app.session.session_service import SessionService
from app.sequence.sequence_service import SequenceService
from app.websocket.websocket_service import ConnectionManager, WebSocketService
import os
from dotenv import load_dotenv

load_dotenv()


class DependencyInjector:
    def get_database():
        return MongoDB().get_database()

    def get_openai_client():
        openai_api_key = os.getenv("OPENAI_API_KEY")
        return OpenAIClient(openai_api_key=openai_api_key)

    def get_summary_agent(openai_client=Depends(get_openai_client)):
        return SummaryAgent(llm_client=openai_client)

    def get_auth_service(db=Depends(get_database), summary_agent=Depends(get_summary_agent)):
        return AuthService(db, summary_agent=summary_agent)

    def get_yoga_coordinator(openai_client=Depends(get_openai_client), auth_service=Depends(get_auth_service)):
        return YogaCoordinator(llm_client=openai_client, auth_service=auth_service)

    def get_sequence_composer(openai_client=Depends(get_openai_client), auth_service=Depends(get_auth_service)):
        return SequenceComposer(llm_client=openai_client, auth_service=auth_service)

    def get_session_service(db=Depends(get_database), yoga_coordinator=Depends(get_yoga_coordinator)):
        return SessionService(db, yoga_coordinator=yoga_coordinator)

    def get_query_service(
        db=Depends(get_database),
        session_service=Depends(get_session_service),
        yoga_coordinator=Depends(get_yoga_coordinator),
    ):
        return QueryService(db, session_service, yoga_coordinator)

    def get_sequence_service(
        db=Depends(get_database),
        sequence_composer=Depends(get_sequence_composer),
    ):
        return SequenceService(db, sequence_composer=sequence_composer)

    def get_websocket_connection_manager():
        return ConnectionManager()

    def get_websocket_service(
        db=Depends(get_database),
        query_service=Depends(get_query_service),
        connection_manager=Depends(get_websocket_connection_manager),
        session_service=Depends(get_session_service),
        yoga_coordinator=Depends(get_yoga_coordinator),
    ):
        return WebSocketService(
            db,
            query_service=query_service,
            connection_manager=connection_manager,
            session_service=session_service,
            yoga_coordinator=yoga_coordinator,
        )
