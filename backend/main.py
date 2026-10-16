from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.gemini_service import ask_gemini

from app.database.database import (
    SessionLocal,
    Base,
    engine,
)

from app.database.crud import get_all_bookings

# استيراد الموديل حتى يتم إنشاء الجدول
from app.models.booking import Booking

# إنشاء الجداول إذا لم تكن موجودة
Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # تم التعديل ليسمح بالاتصال من أي نطاق محلي للواجهة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Sales Agent is running 🚀"
    }


@app.get("/chat")
def chat(message: str):
    reply = ask_gemini(message)

    return {
        "user": message,
        "ai": reply,
    }


@app.get("/bookings")
def bookings():
    db = SessionLocal()

    try:
        data = get_all_bookings(db)

        result = []

        for booking in data:
            result.append(
                {
                    "id": booking.id,
                    "customer_name": booking.customer_name,
                    "phone": booking.phone,
                    "appointment_date": booking.appointment_date,
                    "appointment_time": booking.appointment_time,
                    "status": booking.status,
                }
            )

        result

        return result

    finally:
        db.close()