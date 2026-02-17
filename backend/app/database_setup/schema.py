import uuid
from typing import Optional
from sqlmodel import Field
from app.models.event import EventBase
from app.models.user import UserDBBase

# it inherits from the event model
class Event(EventBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)

# User model
class User(UserDBBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
