"""Stored sequence posture shapes as persisted on `sequences.postures` in MongoDB."""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


class StoredCanonicalPostureRef(BaseModel):
    """
    Canonical posture snapshot embedded in a sequence (top-level static/transitional
    or nested under interval_set / vinyasa_loop).
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(alias="_id")
    name: str
    sanskrit_name: str
    client_id: str
    posture_intent: str
    recommended_modification: str = ""
    hold_time_seconds: int | None = None


class StoredStaticHoldItem(BaseModel):
    """Top-level static hold row as stored on a sequence."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    posture_intent: Literal["static_hold"]
    id: str = Field(alias="_id")
    name: str
    sanskrit_name: str
    client_id: str
    recommended_modification: str = ""
    hold_time_seconds: int


class StoredTransitionalHubItem(BaseModel):
    """Top-level transitional hub row as stored on a sequence."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    posture_intent: Literal["transitional_hub"]
    id: str = Field(alias="_id")
    name: str
    sanskrit_name: str
    client_id: str
    recommended_modification: str = ""


class StoredIntervalSetItem(BaseModel):
    """Interval work/recovery pair block as stored on a sequence."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    posture_intent: Literal["interval_set"]
    rounds: int
    hold_time_seconds: int
    rest_time_seconds: int
    work_posture: StoredCanonicalPostureRef
    recovery_posture: StoredCanonicalPostureRef


class StoredVinyasaLoopItem(BaseModel):
    """Vinyasa cycle block as stored on a sequence."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    posture_intent: Literal["vinyasa_loop"]
    rounds: int
    cycle_postures: list[StoredCanonicalPostureRef]


StoredSequencePostureItem = Union[
    StoredStaticHoldItem, StoredTransitionalHubItem, StoredIntervalSetItem, StoredVinyasaLoopItem
]

StoredSequencePosture = Annotated[
    StoredSequencePostureItem,
    Field(discriminator="posture_intent"),
]
