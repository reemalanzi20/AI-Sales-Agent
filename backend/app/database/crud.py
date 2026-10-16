from sqlalchemy.orm import Session
from app.models.booking import Booking


def create_booking(
    db: Session,
    customer_name: str,
    phone: str,
    appointment_date: str,
    appointment_time: str,
):
    booking = Booking(
        customer_name=customer_name,
        phone=phone,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status="قادم",
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


def get_all_bookings(db: Session):
    return db.query(Booking).all()


def get_booking_by_datetime(
    db: Session,
    appointment_date: str,
    appointment_time: str,
):
    return db.query(Booking).filter(
        Booking.appointment_date == appointment_date,
        Booking.appointment_time == appointment_time,
        Booking.status != "ملغي",
    ).first()


def get_booking_by_phone(
    db: Session,
    phone: str,
):
    return db.query(Booking).filter(
        Booking.phone == phone,
        Booking.status != "ملغي",
    ).first()


def update_booking(
    db: Session,
    booking: Booking,
    appointment_date: str,
    appointment_time: str,
):
    booking.appointment_date = appointment_date
    booking.appointment_time = appointment_time
    booking.status = "تم التعديل"

    db.commit()
    db.refresh(booking)

    return booking


def cancel_booking_status(
    db: Session,
    booking: Booking,
):
    booking.status = "ملغي"

    db.commit()
    db.refresh(booking)

    return booking