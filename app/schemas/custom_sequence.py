"""Schema for LLM-generated custom yoga sequence.

Single flat item model (no discriminated union) so OpenAI structured outputs avoid oneOf on postures.items.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

POSTURE_INTENT_STATIC_HOLD = "static_hold"
POSTURE_INTENT_TRANSITIONAL_HUB = "transitional_hub"
POSTURE_INTENT_INTERVAL_SET = "interval_set"

PostureIntent = Literal["static_hold", "transitional_hub", "interval_set"]


class PostureSlotIn(BaseModel):
    """Work or recovery pose inside an interval_set (LLM input only; no posture_intent on slots)."""

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

    posture_intent: PostureIntent = Field(description="static_hold | transitional_hub | interval_set")

    posture_id: str | None = Field(
        default=None,
        description="Required for static_hold and transitional_hub. Omit or null for interval_set.",
    )
    recommended_modification: str = Field(
        default="",
        description="Required for static_hold and transitional_hub. For interval_set use empty string (modifications live on work_posture and recovery_posture only).",
    )
    hold_time_seconds: int | None = Field(
        default=None,
        description="Required for static_hold and interval_set (work interval, > 0). Omit or null for transitional_hub.",
    )
    rounds: int | None = Field(default=None, description="Required for interval_set (>= 1). Omit otherwise.")
    rest_time_seconds: int | None = Field(
        default=None, description="Required for interval_set (>= 0). Omit otherwise."
    )
    work_posture: PostureSlotIn | None = Field(default=None, description="Required for interval_set only.")
    recovery_posture: PostureSlotIn | None = Field(default=None, description="Required for interval_set only.")

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
            "(each posture_id + recommended_modification); use empty string for top-level recommended_modification; omit posture_id. "
            "Valid catalogue client_ids only."
        )
    )
