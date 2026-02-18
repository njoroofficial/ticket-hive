import uuid
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session
from app.database_setup.database import get_session
from app.database_setup.schema import User
from app.models.booking import BookingCreate, BookingRead
from app.services.booking_service import BookingService
from app.auth.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> BookingRead:
    """Authenticated user books tickets for an event."""
    service = BookingService(session)
    try:
        return service.create_booking(booking_data, current_user.id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create booking at this time.",
        ) from exc


@router.get("/me", response_model=list[BookingRead], status_code=status.HTTP_200_OK)
def list_my_bookings(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[BookingRead]:
    """List all bookings for the currently logged-in user."""
    service = BookingService(session)
    return service.list_user_bookings(current_user.id)


@router.get("/{booking_id}", response_model=BookingRead, status_code=status.HTTP_200_OK)
def get_booking(
    booking_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> BookingRead:
    """Get a specific booking (must belong to the current user)."""
    service = BookingService(session)
    try:
        return service.get_booking(booking_id, current_user.id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(
    booking_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Cancel a booking (must belong to the current user)."""
    service = BookingService(session)
    try:
        service.cancel_booking(booking_id, current_user.id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to cancel booking at this time.",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/event/{event_id}",
    response_model=list[BookingRead],
    status_code=status.HTTP_200_OK,
)
def list_event_bookings(
    event_id: uuid.UUID,
    admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> list[BookingRead]:
    """Admin-only: list all bookings for a specific event."""
    service = BookingService(session)
    return service.list_event_bookings(event_id)