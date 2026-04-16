"""
Node functions for the sequence-generation LangGraph.

Each function receives the full ``SequenceGraphState`` but reads only the keys
it needs and returns a dict of keys it writes.  The graph merges the returned
dict back into state automatically.

All heavy logic (LLM calls, DB queries) is delegated to existing agent and
service classes injected via ``build_node_functions``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from bson import ObjectId
from openai import RateLimitError

from app.orchestration.profile_helpers import build_profiler_profile_bundle
from app.orchestration.state import SequenceGraphState
from app.profile_extraction import ProfileContext
from app.schemas.custom_sequence import CustomSequenceOutput


def build_node_functions(
    *,
    db,
    auth_service,
    summary_agent,
    request_reviewer,
    sequence_composer,
    sequence_service,
) -> dict[str, Any]:
    """
    Close over shared dependencies and return a dict of node callables keyed by
    node name.  The graph builder uses these to register nodes.
    """

    async def profiler_node(state: SequenceGraphState) -> dict:
        """Load user profile and theme from DB; extract profile bundle in one pass."""
        user = await auth_service.get_profile(str(state["user_id"]))
        bundle = build_profiler_profile_bundle(user)

        theme_id = state["practice_theme_id"]
        try:
            theme = await db["themes"].find_one({"_id": ObjectId(theme_id)})
        except Exception:
            raise ValueError(f"Invalid theme ID: {theme_id}")
        if not theme:
            raise ValueError(f"Theme not found: {theme_id}")

        return {**bundle, "theme": theme}

    async def briefing_node(state: SequenceGraphState) -> dict:
        """Distil profile + theme + user notes into a single session briefing."""
        ctx = ProfileContext(**state["profile_context"])

        briefing = await summary_agent.generate_session_briefing(
            ctx=ctx,
            hard_strategy=state["hard_strategy"],
            medium_strategy=state["medium_strategy"],
            theme=state["theme"],
            user_notes=state.get("user_notes"),
        )
        return {"session_briefing": briefing}

    async def reviewer_node(state: SequenceGraphState) -> dict:
        """Run the RequestReviewer; may surface clarification questions."""
        output = await request_reviewer.review_request(
            session_briefing=state["session_briefing"],
            duration_minutes=state["duration_minutes"],
            theme=state["theme"],
        )
        return {
            "review_passed": output.status,
            "review_questions": [q.model_dump() for q in output.questions],
        }

    async def composer_node(state: SequenceGraphState) -> dict:
        """Run the SequenceComposer to generate a structured sequence."""
        try:
            output: CustomSequenceOutput = await sequence_composer.compose_sequence(
                response_format=CustomSequenceOutput,
                session_briefing=state["session_briefing"],
                duration_minutes=state["duration_minutes"],
                theme=state["theme"],
                review_qa_context=state.get("review_qa_context"),
            )
        except RateLimitError as exc:
            return {
                "composer_output": None,
                "error": (
                    "OpenAI rate limit or quota exceeded (check billing and plan at "
                    "https://platform.openai.com/account/billing). "
                    "Sequence generation was not completed."
                ),
            }

        return {
            "composer_output": output.model_dump(),
            "error": None,
        }

    async def hydrate_node(state: SequenceGraphState) -> dict:
        """Resolve LLM posture IDs against the DB catalogue."""
        raw = state.get("composer_output")
        if not raw:
            return {"hydrated_postures": None}

        output = CustomSequenceOutput(**raw)
        all_ids = list(sequence_service._client_ids_from_llm_output(output))

        db_postures: dict[str, dict] = {}
        async for doc in db["postures"].find({"client_id": {"$in": all_ids}}):
            cid = doc.get("client_id")
            if cid is not None:
                db_postures[str(cid).strip()] = doc

        postures = []
        for item in output.postures:
            row = sequence_service._stored_posture_from_llm_item(item, db_postures)
            if row:
                postures.append(row)

        if not postures:
            retries = state.get("composer_retries") or 0
            return {
                "hydrated_postures": None,
                "composer_retries": retries + 1,
                "error": "No valid postures could be resolved from the catalogue",
            }

        return {
            "hydrated_postures": postures,
            "error": None,
        }

    async def persist_node(state: SequenceGraphState) -> dict:
        """Save the hydrated sequence to MongoDB."""
        postures = state.get("hydrated_postures")
        if not postures:
            return {"error": "Cannot persist: no hydrated postures"}

        raw = state.get("composer_output") or {}
        sequence_doc = {
            "name": raw.get("name", "Untitled Sequence"),
            "postures": postures,
            "type": "generated",
            "duration_minutes": state["duration_minutes"],
            "user_id": ObjectId(state["user_id"]),
            "practice_theme_id": ObjectId(state["practice_theme_id"]),
            "user_notes": state.get("user_notes"),
            "created_at": datetime.utcnow(),
        }
        result = await db["sequences"].insert_one(sequence_doc)
        sequence_doc["_id"] = result.inserted_id

        return {
            "sequence_doc": {
                **sequence_doc,
                "reasoning": raw.get("reasoning", ""),
            },
            "error": None,
        }

    return {
        "profiler": profiler_node,
        "briefing": briefing_node,
        "reviewer": reviewer_node,
        "composer": composer_node,
        "hydrate": hydrate_node,
        "persist": persist_node,
    }
