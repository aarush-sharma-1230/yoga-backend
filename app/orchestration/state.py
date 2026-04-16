"""Shared state flowing through the sequence-generation LangGraph."""

from __future__ import annotations

from typing import TypedDict


class SequenceGraphState(TypedDict, total=False):
    """
    Single state object that travels through every node in the graph.

    Each node reads only the keys it needs and writes back its own output keys.
    After ``briefing_node`` runs, raw strategies and user_notes are never read
    again -- ``session_briefing`` becomes the sole practitioner context.
    """

    # --- Inputs (set once at graph entry) ---
    user_id: str
    duration_minutes: int
    practice_theme_id: str
    user_notes: str | None
    answered_questions: list[dict] | None

    # --- Populated by profiler_node ---
    profile_context: dict
    hard_strategy: dict
    medium_strategy: dict
    theme: dict

    # --- Populated by briefing_node (SummaryAgent) ---
    session_briefing: str

    # --- Populated by reviewer_node ---
    review_passed: bool
    review_questions: list[dict]

    # --- Populated by composer_node ---
    composer_output: dict | None
    review_qa_context: str | None

    # --- Populated by hydrate_node ---
    hydrated_postures: list[dict] | None

    # --- Populated by persist_node ---
    sequence_doc: dict | None

    # --- Control ---
    composer_retries: int
    error: str | None
