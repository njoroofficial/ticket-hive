import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from app.database_setup.schema import Event
from app.models.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, session: Session):
        self._db = session

    # Create and persist a new event row.
    def create_event(self, event_data: EventCreate) -> Event:
        event = Event.model_validate(event_data)
        try:
            self._db.add(event)
            self._db.commit()
            self._db.refresh(event)
            return event
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise RuntimeError("Failed to create event") from exc

    # Return all events ordered by date (soonest first).
    def list_events(self, offset=0, limit=10) -> list[Event]:
        statement = select(Event).order_by(Event.date).offset(offset).limit(limit)
        return list(self._db.exec(statement).all())

    # Fetch one event by id; raises LookupError when missing.
    def get_event(self, event_id: uuid.UUID) -> Event:
        event = self._db.get(Event, event_id)
        if not event:
            raise LookupError("Event not found")
        return event

    # Apply partial updates to an event and persist changes.
    def update_event(self, event_id: uuid.UUID, event_data: EventUpdate) -> Event:
        event = self.get_event(event_id)
        updates = event_data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(event, field, value)

        try:
            self._db.add(event)
            self._db.commit()
            self._db.refresh(event)
            return event
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise RuntimeError("Failed to update event") from exc

    # Delete an event by id.
    def delete_event(self, event_id: uuid.UUID) -> None:
        event = self.get_event(event_id)
        try:
            self._db.delete(event)
            self._db.commit()
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise RuntimeError("Failed to delete event") from exc
        