from sqlalchemy.orm import Session

from app.database.crud import (
    get_booking_by_phone,
    cancel_booking_status,
)


def cancel_booking(db: Session, phone: str):
    booking = get_booking_by_phone(db, phone)

    if booking is None:
        return False, "لم يتم العثور على أي حجز بهذا الرقم."

    cancel_booking_status(db, booking)

    return True, "تم إلغاء الحجز بنجاح."