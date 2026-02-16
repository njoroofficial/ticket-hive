import uuid
from datetime import datetime, timezone
from typing import Annotated
from pydantic import field_validator
from sqlmodel import Field, SQLModel


class EventBase(SQLModel):
    name: str = Field(min_length=1, max_length=120)
    date: datetime
    price: Annotated[float, Field(gt=0)]
    location: str = Field(min_length=1, max_length=255)

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


class EventRead(EventBase):
    id: uuid.UUID
