"""Request-scoped LLM micro-USD accumulation without FastAPI or DI imports."""

from __future__ import annotations

import contextvars
from typing import Optional

_micro_stack: contextvars.ContextVar[Optional[list[int]]] = contextvars.ContextVar("request_llm_cost_micro_stack", default=None)


def start_request_llm_cost_tracking() -> None:
    """Begin accumulating micro-USD for the current asyncio context; replaces any prior list."""
    _micro_stack.set([])


def stop_request_llm_cost_tracking() -> None:
    """Clear tracking for this context."""
    _micro_stack.set(None)


def add_request_llm_cost_micro(delta: int) -> None:
    """Add micro-USD to the current request total if tracking is active."""
    if delta <= 0:
        return
    bucket = _micro_stack.get()
    if bucket is not None:
        bucket.append(delta)


def get_request_llm_cost_micro_total() -> int:
    """Return accumulated micro-USD for this context, or 0 if not tracking."""
    bucket = _micro_stack.get()
    if not bucket:
        return 0
    return sum(bucket)


def is_request_llm_cost_tracking() -> bool:
    """Return True when request-level accumulation is active."""
    return _micro_stack.get() is not None
