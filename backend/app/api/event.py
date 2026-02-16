from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from app.database_setup.schema import Event
from app.database_setup.database import get_session
from app.models.event import EventCreate, EventRead

router = APIRouter()

@router.post("/events/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, session: Session = Depends(get_session)) -> EventRead:
    # Convert the Pydantic model (EventCreate) to the DB model (Event)
    event = Event.model_validate(event_data)

    # Add and save event to database
    try:
        session.add(event)
        session.commit()
        session.refresh(event)
    except SQLAlchemyError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create event at this time.",
        ) from exc

    return event
