"""
LangGraph definition for the sequence-generation workflow.

Assembles a ``StateGraph`` with conditional edges for the requirement-review
interrupt, the composer↔sequence-reviewer loop, and hydrate retries.
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from app.orchestration.state import SequenceGraphState

MAX_COMPOSER_RETRIES = 1
"""Hydration (catalogue) retries: extra composer runs after unresolved posture IDs."""

MAX_SEQUENCE_REVIEW_ROUNDS = 4
"""Maximum failed sequence reviews before stopping (first composition + up to three revisions)."""


def _after_briefing(state: SequenceGraphState) -> str:
    """Skip requirement review when the client already answered questions (pass 2)."""
    if state.get("answered_questions"):
        return "composer"
    return "requirement_reviewer"


def _after_requirement_reviewer(state: SequenceGraphState) -> str:
    """Route after requirement review: composer or interrupt with questions."""
    if state.get("review_passed"):
        return "composer"
    return END


def _after_sequence_reviewer(state: SequenceGraphState) -> str:
    """Route after sequence review: hydrate, revise composition, or end on error."""
    if state.get("error"):
        return END
    if state.get("sequence_review_passed"):
        return "hydrate"
    return "composer"


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
    graph.add_node("requirement_reviewer", node_fns["requirement_reviewer"])
    graph.add_node("composer", node_fns["composer"])
    graph.add_node("sequence_reviewer", node_fns["sequence_reviewer"])
    graph.add_node("hydrate", node_fns["hydrate"])
    graph.add_node("persist", node_fns["persist"])

    graph.set_entry_point("profiler")
    graph.add_edge("profiler", "briefing")
    graph.add_conditional_edges(
        "briefing",
        _after_briefing,
        {"requirement_reviewer": "requirement_reviewer", "composer": "composer"},
    )
    graph.add_conditional_edges(
        "requirement_reviewer",
        _after_requirement_reviewer,
        {"composer": "composer", END: END},
    )
    graph.add_edge("composer", "sequence_reviewer")
    graph.add_conditional_edges(
        "sequence_reviewer",
        _after_sequence_reviewer,
        {"hydrate": "hydrate", "composer": "composer", END: END},
    )
    graph.add_conditional_edges(
        "hydrate",
        _after_hydrate,
        {"persist": "persist", "composer": "composer", END: END},
    )
    graph.add_edge("persist", END)

    return graph.compile()
