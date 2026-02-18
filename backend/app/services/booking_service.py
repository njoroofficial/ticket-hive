import uuid
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlmodel import Session, select
from app.database_setup.schema import Booking, Event
from app.models.booking import BookingCreate


class BookingService:
    def __init__(self, session: Session):
        self._db = session

    def create_booking(self, booking_data: BookingCreate, user_id: uuid.UUID) -> Booking:
        """Book tickets for an event."""

        #    Fetch the event WITH A ROW-LEVEL LOCK
        #    This prevents concurrent transactions from reading the same row
        #    until this transaction commits/rolls back.

        statement = (
            select(Event)
            .where(Event.id == booking_data.event_id)
            .with_for_update()
        )
        event = self._db.exec(statement).first()
        if not event:
            raise LookupError("Event not found")


        event = self._db.get(Event, booking_data.event_id)
        if not event:
            raise LookupError("Event not found")

        #  Make sure the event hasn't already passed
        event_date = (
            event.date
            if event.date.tzinfo
            else event.date.replace(tzinfo=timezone.utc)
        )
        if event_date <= datetime.now(timezone.utc):
            raise ValueError("Cannot book a past event")

        # Count tickets already sold ──
        statement = select(func.coalesce(func.sum(Booking.quantity), 0)).where(
            Booking.event_id == booking_data.event_id
        )
        total_sold = self._db.exec(statement).one()

        # Check if this booking would exceed capacity ──
        if total_sold + booking_data.quantity > event.capacity:
            available = event.capacity - total_sold
            raise ValueError(
                f"Not enough tickets. Only {available} ticket(s) remaining."
            )

        # Calculate total price
        total_price = round(event.price * booking_data.quantity, 2)

        # Create the booking row
        booking = Booking(
            event_id=booking_data.event_id,
            user_id=user_id,
            quantity=booking_data.quantity,
            total_price=total_price,
        )

        try:
            self._db.add(booking)
            self._db.commit()
            self._db.refresh(booking)
            return booking
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise RuntimeError("Failed to create booking") from exc

    def list_user_bookings(self, user_id: uuid.UUID) -> list[Booking]:
        """Return all bookings for a specific user."""
        statement = (
            select(Booking)
            .where(Booking.user_id == user_id)
            .order_by(Booking.booked_at.desc())
        )
        return list(self._db.exec(statement).all())

    def get_booking(self, booking_id: uuid.UUID, user_id: uuid.UUID) -> Booking:
        """Fetch a single booking; ensures it belongs to the requesting user."""
        booking = self._db.get(Booking, booking_id)
        if not booking:
            raise LookupError("Booking not found")
        if booking.user_id != user_id:
            raise PermissionError("You do not own this booking")
        return booking

    def cancel_booking(self, booking_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """Cancel (delete) a booking owned by the user."""
        booking = self.get_booking(booking_id, user_id)
        try:
            self._db.delete(booking)
            self._db.commit()
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise RuntimeError("Failed to cancel booking") from exc

    def list_event_bookings(self, event_id: uuid.UUID) -> list[Booking]:
        """Admin: return all bookings for a given event."""
        statement = (
            select(Booking)
            .where(Booking.event_id == event_id)
            .order_by(Booking.booked_at.desc())
        )
        return list(self._db.exec(statement).all())