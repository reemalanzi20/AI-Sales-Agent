from sqlalchemy.orm import Session

from app.database.crud import (
    create_booking,
    get_booking_by_datetime,
)


def save_booking(
    db: Session,
    customer_name: str,
    phone: str,
    appointment_date: str,
    appointment_time: str,
):
    existing = get_booking_by_datetime(
        db,
        appointment_date,
        appointment_time,
    )

    if existing:
        return False, "عذراً، هذا الموعد محجوز بالفعل. يرجى اختيار موعد آخر."

    create_booking(
        db=db,
        customer_name=customer_name,
        phone=phone,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
    )

    return True, "تم الحجز بنجاح."