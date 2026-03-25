"""Schema for LLM-generated custom yoga sequence.

Single flat item model (no discriminated union) so OpenAI structured outputs avoid oneOf on postures.items.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

POSTURE_INTENT_STATIC_HOLD = "static_hold"
POSTURE_INTENT_TRANSITIONAL_HUB = "transitional_hub"
POSTURE_INTENT_INTERVAL_SET = "interval_set"
POSTURE_INTENT_VINYASA_LOOP = "vinyasa_loop"

PostureIntent = Literal["static_hold", "transitional_hub", "interval_set", "vinyasa_loop"]


class PostureSlotIn(BaseModel):
    """Slot for interval_set work/recovery or vinyasa_loop cycle steps (posture_id + recommended_modification only)."""

    model_config = ConfigDict(extra="ignore")

    posture_id: str = Field(description="client_id from catalogue")
    recommended_modification: str = Field(
        description="Modification for this practitioner (from contraindications/chronic_pain) or empty string if none."
    )


class SequencePostureItem(BaseModel):
    """
    One posture row in the flat sequence. Intent-specific fields are optional in the JSON schema;
    a model_validator enforces which fields apply per posture_intent (OpenAI-compatible: no oneOf).
    """

    model_config = ConfigDict(extra="ignore")

    posture_intent: PostureIntent = Field(
        description="static_hold | transitional_hub | interval_set | vinyasa_loop"
    )

    posture_id: str | None = Field(
        default=None,
        description="Required for static_hold and transitional_hub. Omit or null for interval_set and vinyasa_loop.",
    )
    recommended_modification: str = Field(
        default="",
        description="For static_hold and transitional_hub. For interval_set and vinyasa_loop use empty string; use nested objects for modifications.",
    )
    hold_time_seconds: int | None = Field(
        default=None,
        description="Required for static_hold and interval_set (work interval, > 0). Omit or null for transitional_hub and vinyasa_loop.",
    )
    rounds: int | None = Field(
        default=None, description="Required for interval_set and vinyasa_loop (>= 1). Omit otherwise."
    )
    rest_time_seconds: int | None = Field(
        default=None, description="Required for interval_set (>= 0). Omit otherwise."
    )
    work_posture: PostureSlotIn | None = Field(default=None, description="Required for interval_set only.")
    recovery_posture: PostureSlotIn | None = Field(default=None, description="Required for interval_set only.")
    cycle_postures: list[PostureSlotIn] | None = Field(
        default=None,
        description="Required for vinyasa_loop: ordered poses repeated as a cycle (min 2). Each entry has posture_id and recommended_modification.",
    )

    @model_validator(mode="after")
    def validate_by_intent(self):
        """Enforce field presence per posture_intent."""
        intent = self.posture_intent

        if intent == POSTURE_INTENT_STATIC_HOLD:
            if not (self.posture_id and self.posture_id.strip()):
                raise ValueError("static_hold requires posture_id")
            if self.hold_time_seconds is None or self.hold_time_seconds <= 0:
                raise ValueError("static_hold requires hold_time_seconds > 0")
            if self.rounds is not None:
                raise ValueError("static_hold must not set rounds")
            if self.rest_time_seconds is not None:
                raise ValueError("static_hold must not set rest_time_seconds")
            if self.work_posture is not None or self.recovery_posture is not None:
                raise ValueError("static_hold must not set work_posture or recovery_posture")
            if self.cycle_postures is not None:
                raise ValueError("static_hold must not set cycle_postures")
            return self

        if intent == POSTURE_INTENT_TRANSITIONAL_HUB:
            if not (self.posture_id and self.posture_id.strip()):
                raise ValueError("transitional_hub requires posture_id")
            if self.hold_time_seconds is not None:
                raise ValueError("transitional_hub must not include hold_time_seconds")
            if self.rounds is not None:
                raise ValueError("transitional_hub must not set rounds")
            if self.rest_time_seconds is not None:
                raise ValueError("transitional_hub must not set rest_time_seconds")
            if self.work_posture is not None or self.recovery_posture is not None:
                raise ValueError("transitional_hub must not set work_posture or recovery_posture")
            if self.cycle_postures is not None:
                raise ValueError("transitional_hub must not set cycle_postures")
            return self

        if intent == POSTURE_INTENT_INTERVAL_SET:
            if self.posture_id is not None and str(self.posture_id).strip():
                raise ValueError("interval_set must not set posture_id")
            if self.work_posture is None or self.recovery_posture is None:
                raise ValueError("interval_set requires work_posture and recovery_posture")
            if self.rounds is None or self.rounds < 1:
                raise ValueError("interval_set requires rounds >= 1")
            if self.hold_time_seconds is None or self.hold_time_seconds <= 0:
                raise ValueError("interval_set requires hold_time_seconds > 0")
            if self.rest_time_seconds is None or self.rest_time_seconds < 0:
                raise ValueError("interval_set requires rest_time_seconds >= 0")
            if self.cycle_postures is not None:
                raise ValueError("interval_set must not set cycle_postures")
            return self

        if intent == POSTURE_INTENT_VINYASA_LOOP:
            if self.posture_id is not None and str(self.posture_id).strip():
                raise ValueError("vinyasa_loop must not set posture_id")
            if self.recommended_modification.strip():
                raise ValueError("vinyasa_loop must use empty top-level recommended_modification; set per cycle_postures entry")
            if self.hold_time_seconds is not None:
                raise ValueError("vinyasa_loop must not set hold_time_seconds")
            if self.rest_time_seconds is not None:
                raise ValueError("vinyasa_loop must not set rest_time_seconds")
            if self.work_posture is not None or self.recovery_posture is not None:
                raise ValueError("vinyasa_loop must not set work_posture or recovery_posture")
            if not self.cycle_postures or len(self.cycle_postures) < 2:
                raise ValueError("vinyasa_loop requires cycle_postures with at least 2 poses")
            if self.rounds is None or self.rounds < 1:
                raise ValueError("vinyasa_loop requires rounds >= 1")
            return self

        raise ValueError(f"Unknown posture_intent: {intent}")


# Alias for callers that referred to a single sequence posture type
SequencePosture = SequencePostureItem


class CustomSequenceOutput(BaseModel):
    """Structured output for a custom yoga sequence."""

    model_config = ConfigDict(extra="ignore")

    reasoning: str = Field(
        description="High-level reasoning explaining your sequence design: why you selected these postures, how you considered the practitioner's profile/safety, how you met the constraints, and the logic behind the flow."
    )
    name: str = Field(description="A short, descriptive name for the sequence (e.g. 'Morning Flow', 'Hip Opener')")
    postures: list[SequencePostureItem] = Field(
        description=(
            "Flat ordered list in flow order. Each item: posture_intent plus only the fields allowed for that intent. "
            "static_hold: posture_id, recommended_modification, hold_time_seconds>0. "
            "transitional_hub: posture_id, recommended_modification (no hold_time_seconds). "
            "interval_set: rounds>=1, hold_time_seconds>0, rest_time_seconds>=0, work_posture and recovery_posture "
            "(each posture_id + recommended_modification); top-level recommended_modification \"\". "
            "vinyasa_loop: rounds>=1, cycle_postures (min 2 objects, each posture_id + recommended_modification), "
            "top-level recommended_modification \"\". Valid catalogue client_ids only."
        )
    )
