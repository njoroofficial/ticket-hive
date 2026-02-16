import uuid
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session
from app.database_setup.database import get_session
from app.models.event import EventCreate, EventRead, EventUpdate
from app.services.event_service import EventService

router = APIRouter()


@router.post("/events/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, session: Session = Depends(get_session)) -> EventRead:
    service = EventService(session)
    try:
        return service.create_event(event_data)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create event at this time.",
        ) from exc


@router.get("/events/", response_model=list[EventRead], status_code=status.HTTP_200_OK)
def list_events(session: Session = Depends(get_session)) -> list[EventRead]:
    service = EventService(session)
    return service.list_events()


@router.get("/events/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def get_event(event_id: uuid.UUID, session: Session = Depends(get_session)) -> EventRead:
    service = EventService(session)
    try:
        return service.get_event(event_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        ) from exc


@router.patch("/events/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
def update_event(
    event_id: uuid.UUID,
    event_data: EventUpdate,
    session: Session = Depends(get_session),
) -> EventRead:
    service = EventService(session)
    try:
        return service.update_event(event_id, event_data)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update event at this time.",
        ) from exc


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: uuid.UUID, session: Session = Depends(get_session)) -> Response:
    service = EventService(session)
    try:
        service.delete_event(event_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete event at this time.",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
