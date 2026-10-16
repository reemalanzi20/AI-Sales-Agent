from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    phone = Column(String)
    appointment_date = Column(String)
    appointment_time = Column(String)

    status = Column(String, default="قادم")