from pydantic import BaseModel


class SequenceData(BaseModel):
  sequence_id: str
