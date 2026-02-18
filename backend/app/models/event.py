import uuid
from datetime import datetime, timezone
from typing import Annotated
from pydantic import field_validator
from sqlmodel import Field, SQLModel
from decimal import Decimal

class EventBase(SQLModel):
    name: str = Field(min_length=1, max_length=120)
    date: datetime
    price: Annotated[Decimal, Field(gt=0)]
    location: str = Field(min_length=1, max_length=255)
    capacity: int = Field(ge=1, description="Maximum number of tickets available")

    @field_validator("name", "location")
    @classmethod
    def strip_and_validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be blank")
        return cleaned

    @field_validator("date")
    @classmethod
    def event_date_must_be_future(cls, value: datetime) -> datetime:
        event_date = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        if event_date <= datetime.now(timezone.utc):
            raise ValueError("event date must be in the future")
        return value


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    date: datetime | None = None
    price: Annotated[Decimal | None, Field(default=None, gt=0)]
    location: str | None = Field(default=None, min_length=1, max_length=255)
    capacity: int | None = Field(default=None, ge=1)

    @field_validator("name", "location")
    @classmethod
    def strip_and_validate_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be blank")
        return cleaned

    @field_validator("date")
    @classmethod
    def optional_event_date_must_be_future(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        event_date = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        if event_date <= datetime.now(timezone.utc):
            raise ValueError("event date must be in the future")
        return value


class EventRead(EventBase):
    id: uuid.UUID
