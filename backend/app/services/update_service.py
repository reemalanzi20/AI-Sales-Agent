from sqlalchemy.orm import Session

from app.database.crud import (
    get_booking_by_phone,
    get_booking_by_datetime,
    update_booking,
)


def change_booking(
    db: Session,
    phone: str,
    appointment_date: str,
    appointment_time: str,
):
    booking = get_booking_by_phone(db, phone)

    if booking is None:
        return False, "لم يتم العثور على حجز مرتبط بهذا الرقم."

    existing = get_booking_by_datetime(
        db,
        appointment_date,
        appointment_time,
    )

    if existing and existing.id != booking.id:
        return False, "عذراً، هذا الموعد محجوز بالفعل."

    update_booking(
        db,
        booking,
        appointment_date,
        appointment_time,
    )

    return True, "تم تعديل الموعد بنجاح."