"""Structured LLM output for session transition guidance (static/interval vs vinyasa instruction-only)."""

from pydantic import BaseModel, Field


class TransitionGuidanceStep(BaseModel):
    """One spoken beat: only `instruction` and `sensory_cue`"""

    instruction: str = Field(description="Naturally spoken line(s) for this step under 50 words")
    sensory_cue: str | None = Field(
        default=None,
        description="Breath or body awareness; null when not needed under 25 words",
    )


class TransitionGuidanceOutput(BaseModel):
    """Transition response for static_hold and interval_set (instruction + optional sensory_cue per step)."""

    steps: list[TransitionGuidanceStep] = Field(
        description=(
            "Ordered steps. static_hold: 1 (hubs before the hold are spoken inside that step). "
            "interval_set: 2 × rounds; if hubs precede the block, step 0 also completes hub travel and the first timed-flow beat. "
            "Do not use this model for vinyasa_loop; use VinyasaTransitionGuidanceOutput instead."
        )
    )


class VinyasaTransitionStep(BaseModel):
    """One vinyasa timed-flow beat: a single spoken clip (no separate sensory_cue field)."""

    instruction: str = Field(description="Naturally spoken line(s) for this step under 50 words")


class VinyasaTransitionGuidanceOutput(BaseModel):
    """Transition response for vinyasa_loop only: one instruction per step, no sensory_cue in the schema."""

    steps: list[VinyasaTransitionStep] = Field(
        description=(
            "Ordered steps matching timed flow: rounds × len(cycle_postures). "
            "If hubs precede the block, step 0 includes hub travel plus the first cycle beat. "
            "Each object has only `instruction` (one clip per step)."
        )
    )
