from pydantic import BaseModel


class SeriesData(BaseModel):
    sequence_id: str


class GetInstructionsData(BaseModel):
    session_id: str
