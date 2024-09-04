from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    description: str
    time: datetime
    id: int
