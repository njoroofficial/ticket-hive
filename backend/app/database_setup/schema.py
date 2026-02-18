import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field
from app.models.event import EventBase
from app.models.user import UserDBBase
from app.models.booking import BookingBase
from decimal import Decimal
from sqlalchemy import DECIMAL, Column


# it inherits from the event model
class Event(EventBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)


# User model
class User(UserDBBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)


# Booking model
class Booking(BookingBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    total_price: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    booked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
