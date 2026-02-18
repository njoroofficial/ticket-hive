import uuid
from datetime import datetime, timezone
from pydantic import field_validator
from sqlmodel import Field, SQLModel
from typing import Annotated
from decimal import Decimal


class BookingBase(SQLModel):
    """Core fields shared across all booking representations."""
    event_id: uuid.UUID = Field(foreign_key="event.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    quantity: Annotated[int, Field(ge=1, le=10)] = 1

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("quantity must be at least 1")
        return value


class BookingCreate(SQLModel):
    """Payload the client sends — only event_id and quantity.
    user_id is injected from the authenticated user."""
    event_id: uuid.UUID
    quantity: Annotated[int, Field(ge=1, le=10)] = 1


class BookingRead(SQLModel):
    """What the API returns to the client."""
    id: uuid.UUID
    event_id: uuid.UUID
    user_id: uuid.UUID
    quantity: int
    total_price: Decimal
    booked_at: datetime