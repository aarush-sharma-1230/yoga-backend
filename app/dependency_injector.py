from fastapi import Depends

from app.agents.reviewer_agent import ReviewerAgent
from app.agents.sequence_composer import SequenceComposer
from app.agents.summary_agent import SummaryAgent
from app.agents.posture_correction_agent import PostureCorrectionAgent
from app.agents.yoga_coordinator import YogaCoordinator
from app.auth.auth_service import AuthService
from app.database.mongo import MongoDB
from app.llms.openai_client import OpenAIClient
from app.orchestration.graph import build_sequence_graph
from app.orchestration.nodes import build_node_functions
from app.session.session_service import SessionService
from app.sequence.sequence_service import SequenceService
from app.usage.llm_cost_service import LlmCostService
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

    def get_posture_correction_agent(
        openai_client=Depends(get_openai_client),
        auth_service=Depends(get_auth_service),
        db=Depends(get_database),
    ):
        return PostureCorrectionAgent(llm_client=openai_client, auth_service=auth_service, db=db)

    def get_sequence_composer(openai_client=Depends(get_openai_client)):
        return SequenceComposer(llm_client=openai_client)

    def get_reviewer_agent(openai_client=Depends(get_openai_client)):
        return ReviewerAgent(llm_client=openai_client)

    def get_llm_cost_service(db=Depends(get_database)):
        return LlmCostService(db)

    def get_session_service(
        db=Depends(get_database),
        yoga_coordinator=Depends(get_yoga_coordinator),
        posture_correction_agent=Depends(get_posture_correction_agent),
        llm_cost_service=Depends(get_llm_cost_service),
    ):
        return SessionService(
            db,
            yoga_coordinator=yoga_coordinator,
            posture_correction_agent=posture_correction_agent,
            llm_cost_service=llm_cost_service,
        )

    def get_sequence_service(
        db=Depends(get_database),
        auth_service=Depends(get_auth_service),
        summary_agent=Depends(get_summary_agent),
        sequence_composer=Depends(get_sequence_composer),
        reviewer_agent=Depends(get_reviewer_agent),
        llm_cost_service=Depends(get_llm_cost_service),
    ):
        """Build the orchestration graph and inject it into SequenceService."""
        sequence_service = SequenceService(db, llm_cost_service=llm_cost_service)

        node_fns = build_node_functions(
            db=db,
            auth_service=auth_service,
            summary_agent=summary_agent,
            reviewer_agent=reviewer_agent,
            sequence_composer=sequence_composer,
            sequence_service=sequence_service,
        )
        compiled_graph = build_sequence_graph(node_fns)
        sequence_service.compiled_graph = compiled_graph

        return sequence_service