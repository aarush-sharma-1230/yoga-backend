"""Structured LLM output for session transition guidance (unified steps[] for all posture intents)."""

from pydantic import BaseModel, Field


class TransitionGuidanceStep(BaseModel):
    """One spoken beat: only `instruction` and `sensory_cue` (no legacy transition_movement fields)."""

    instruction: str = Field(description="Spoken audio script for this segment (movement, pose name, alignment).")
    sensory_cue: str | None = Field(
        default=None,
        description="Breath or body awareness; null when not needed. For a transitional-hub run with one step, cue the final target hold only.",
    )


class TransitionGuidanceOutput(BaseModel):
    """Transition response: ordered steps matching the upcoming posture intent (see user prompt for exact count)."""

    steps: list[TransitionGuidanceStep] = Field(
        description=(
            "Ordered steps. static_hold: 1 (hubs before the hold are spoken inside that step). "
            "interval_set: 2 × rounds; if hubs precede the block, step 0 also completes hub travel and the first timed-flow beat. "
            "vinyasa_loop: rounds × len(cycle_postures); if hubs precede, step 0 includes hub travel plus the first cycle beat."
        )
    )
