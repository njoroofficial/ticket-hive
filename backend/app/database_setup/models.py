import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Event(SQLModel, table = True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    date: datetime
    location: str
    price: float