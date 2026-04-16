"""
LangGraph definition for the sequence-generation workflow.

Assembles a ``StateGraph`` with conditional edges for the review loop
(human-in-the-loop) and a composer retry when hydration fails.
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from app.orchestration.state import SequenceGraphState

MAX_COMPOSER_RETRIES = 1


def _after_briefing(state: SequenceGraphState) -> str:
    """Skip the reviewer when the client already provided answered questions (pass 2)."""
    if state.get("answered_questions"):
        return "composer"
    return "reviewer"


def _after_reviewer(state: SequenceGraphState) -> str:
    """Route after the reviewer: pass to composer or interrupt with questions."""
    if state.get("review_passed"):
        return "composer"
    return END


def _after_hydrate(state: SequenceGraphState) -> str:
    """Route after hydration: persist if postures are valid, retry composer if allowed."""
    if state.get("hydrated_postures"):
        return "persist"
    retries = state.get("composer_retries") or 0
    if retries <= MAX_COMPOSER_RETRIES:
        return "composer"
    return END


def build_sequence_graph(node_fns: dict[str, Any]) -> StateGraph:
    """
    Construct and compile the sequence-generation graph.

    ``node_fns`` is the dict returned by ``build_node_functions`` — each value
    is an async callable that takes ``SequenceGraphState`` and returns a
    partial state dict.
    """
    graph = StateGraph(SequenceGraphState)

    graph.add_node("profiler", node_fns["profiler"])
    graph.add_node("briefing", node_fns["briefing"])
    graph.add_node("reviewer", node_fns["reviewer"])
    graph.add_node("composer", node_fns["composer"])
    graph.add_node("hydrate", node_fns["hydrate"])
    graph.add_node("persist", node_fns["persist"])

    graph.set_entry_point("profiler")
    graph.add_edge("profiler", "briefing")
    graph.add_conditional_edges("briefing", _after_briefing, {"reviewer": "reviewer", "composer": "composer"})
    graph.add_conditional_edges("reviewer", _after_reviewer, {"composer": "composer", END: END})
    graph.add_edge("composer", "hydrate")
    graph.add_conditional_edges("hydrate", _after_hydrate, {"persist": "persist", "composer": "composer", END: END})
    graph.add_edge("persist", END)

    return graph.compile()
