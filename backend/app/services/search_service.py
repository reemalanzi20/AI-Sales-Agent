from sqlalchemy.orm import Session

from app.database.crud import get_booking_by_phone


def search_booking(db: Session, phone: str):
    booking = get_booking_by_phone(db, phone)

    if booking is None:
        return None

    return {
        "customer_name": booking.customer_name,
        "phone": booking.phone,
        "appointment_date": booking.appointment_date,
        "appointment_time": booking.appointment_time,
    }