"""Session API request body models."""

from pydantic import BaseModel


class SeriesData(BaseModel):
    sequence_id: str
