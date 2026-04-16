"""
Entry point for invoking the sequence-generation graph.

``run_sequence_generation`` builds the initial state, invokes the compiled
graph, and translates the final state into the response dict expected by the
``/sequence/generate`` endpoint.
"""

from __future__ import annotations

from typing import Any

from app.schemas.request_review import ReviewQuestionAnswered


def _format_review_qa_context(questions: list[ReviewQuestionAnswered]) -> str:
    """Render answered review questions into plain text for the composer prompt."""
    lines: list[str] = []
    for ra in questions:
        lines.append(f"Q: {ra.question}")
        lines.append(f"A: {', '.join(ra.answer)}")
        lines.append("")
    return "\n".join(lines).strip()


async def run_sequence_generation(
    *,
    compiled_graph,
    user_id: str,
    practice_theme_id: str,
    duration_minutes: int,
    user_notes: str | None = None,
    questions: list[ReviewQuestionAnswered] | None = None,
) -> dict[str, Any]:
    """
    Invoke the sequence-generation graph and return a response dict.

    Pass 1 (``questions is None``): full graph including reviewer.
    Pass 2 (``questions`` provided): skip reviewer, inject Q&A context.
    """
    initial_state: dict[str, Any] = {
        "user_id": user_id,
        "practice_theme_id": practice_theme_id,
        "duration_minutes": duration_minutes,
        "user_notes": user_notes,
        "composer_retries": 0,
    }

    if questions is not None:
        initial_state["answered_questions"] = [q.model_dump() for q in questions]
        initial_state["review_qa_context"] = _format_review_qa_context(questions)
        initial_state["review_passed"] = True

    final_state = await compiled_graph.ainvoke(initial_state)

    if final_state.get("error"):
        raise RuntimeError(final_state["error"])

    review_questions = final_state.get("review_questions") or []
    if not final_state.get("review_passed") and review_questions:
        return {
            "status": False,
            "questions": review_questions,
        }

    sequence_doc = final_state.get("sequence_doc")
    if not sequence_doc:
        raise RuntimeError("Sequence generation completed but produced no output")

    return {
        "status": True,
        "result": sequence_doc,
    }
