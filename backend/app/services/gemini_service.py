import os

from dotenv import load_dotenv
from google import genai

from app.database.database import SessionLocal
from app.services.booking_service import save_booking
from app.services.update_service import change_booking
from app.services.cancel_service import cancel_booking
from app.services.search_service import search_booking
from app.services.parser_service import parse_gemini_response


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "لم يتم العثور على GEMINI_API_KEY داخل ملف .env"
    )

client = genai.Client(api_key=api_key)


# ==========================================
# قراءة ملف تعليمات النظام
# ==========================================

prompt_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "prompts",
    "system_prompt.txt",
)

prompt_path = os.path.abspath(prompt_path)

with open(prompt_path, "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()


# ==========================================
# حفظ حالة المحادثة مؤقتًا
# ==========================================

conversation_state = {
    "action": None,
    "customer_name": None,
    "phone": None,
    "appointment_date": None,
    "appointment_time": None,
}


def reset_conversation_state():
    conversation_state["action"] = None
    conversation_state["customer_name"] = None
    conversation_state["phone"] = None
    conversation_state["appointment_date"] = None
    conversation_state["appointment_time"] = None


def update_conversation_state(data: dict):
    """
    دمج المعلومات الجديدة مع المعلومات المحفوظة
    من الرسائل السابقة.
    """

    action = data.get("action")
    booking_data = data.get("booking") or {}
    phone = data.get("phone")

    if action in ["book", "update", "cancel", "search"]:
        conversation_state["action"] = action

    if booking_data.get("customer_name"):
        conversation_state["customer_name"] = booking_data.get(
            "customer_name"
        )

    if booking_data.get("phone"):
        conversation_state["phone"] = booking_data.get("phone")

    if phone:
        conversation_state["phone"] = phone

    if booking_data.get("appointment_date"):
        conversation_state["appointment_date"] = booking_data.get(
            "appointment_date"
        )

    if booking_data.get("appointment_time"):
        conversation_state["appointment_time"] = booking_data.get(
            "appointment_time"
        )


def get_context_text():
    """
    إرسال حالة المحادثة الحالية إلى Gemini
    حتى يعرف أن الرسالة تكملة لطلب سابق.
    """

    action = conversation_state["action"]

    if not action:
        return "لا توجد عملية سابقة قيد التنفيذ."

    action_names = {
        "book": "حجز موعد جديد",
        "update": "تعديل موعد موجود",
        "cancel": "إلغاء موعد",
        "search": "الاستعلام عن موعد",
    }

    return f"""
العملية الحالية التي بدأها العميل: {action_names.get(action, action)}

المعلومات التي جُمعت حتى الآن:
- الاسم: {conversation_state["customer_name"] or "غير موجود"}
- رقم الجوال: {conversation_state["phone"] or "غير موجود"}
- التاريخ: {conversation_state["appointment_date"] or "غير موجود"}
- الوقت: {conversation_state["appointment_time"] or "غير موجود"}

اعتبر رسالة العميل الجديدة تكملة للعملية الحالية.
لا تغيّر نوع العملية إلى حجز أو محادثة عادية.
استخدم نفس action الحالي، وأضف المعلومات الجديدة التي ذكرها العميل.
"""


# ==========================================
# التواصل مع Gemini
# ==========================================

def ask_gemini(message: str):
    current_context = get_context_text()

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=f"""
{SYSTEM_PROMPT}

معلومات مهمة عن سياق المحادثة:

{current_context}

قواعد إضافية مهمة جدًا:

- إذا كانت هناك عملية حالية، فاعتبر رسالة العميل تكملة لها.
- لا تبدأ حجزًا جديدًا إذا كانت العملية الحالية تعديلًا.
- لا تستخدم action = chat بسبب نقص المعلومات.
- احتفظ بنوع العملية نفسه، واطلب فقط المعلومات الناقصة.
- عند تعديل الموعد، لا تحتاج إلى اسم العميل.
- وقت مثل "8 مساء" يعني appointment_time = "8 مساء".
- تاريخ مثل "17 أغسطس" يعني appointment_date = "17 أغسطس".
- رقم مثل "050123123" اعتبره رقم الجوال.
- يجب أن يكون الرد JSON صحيحًا فقط.
- لا تكتب أي كلام خارج JSON.

رسالة العميل الحالية:
{message}
""",
    )

    text = response.text.strip()

    data = parse_gemini_response(text)

    if data is None:
        print("Gemini raw response:", text)

        return (
            "لم أتمكن من فهم الطلب. "
            "فضلاً، أعد كتابة المعلومات بشكل أوضح."
        )

    generated_action = data.get("action", "chat")

    # إذا كانت هناك عملية مستمرة وGemini أعاد chat،
    # نحافظ على العملية الأصلية.
    if (
        conversation_state["action"]
        and generated_action == "chat"
    ):
        data["action"] = conversation_state["action"]

    update_conversation_state(data)

    action = conversation_state["action"]
    reply = data.get("reply", "كيف يمكنني مساعدتك؟")

    customer_name = conversation_state["customer_name"]
    phone = conversation_state["phone"]
    appointment_date = conversation_state["appointment_date"]
    appointment_time = conversation_state["appointment_time"]

    db = SessionLocal()

    try:
        # ==================================
        # إنشاء حجز جديد
        # ==================================

        if action == "book":
            missing_fields = []

            if not customer_name:
                missing_fields.append("الاسم")

            if not phone:
                missing_fields.append("رقم الجوال")

            if not appointment_date:
                missing_fields.append("تاريخ الموعد")

            if not appointment_time:
                missing_fields.append("وقت الموعد")

            if missing_fields:
                return (
                    "لإتمام الحجز، أحتاج إلى: "
                    + "، ".join(missing_fields)
                    + "."
                )

            success, result = save_booking(
                db=db,
                customer_name=customer_name,
                phone=phone,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            )

            reset_conversation_state()

            if not success:
                return result

            return result

        # ==================================
        # تعديل حجز موجود
        # ==================================

        if action == "update":
            missing_fields = []

            if not phone:
                missing_fields.append("رقم الجوال")

            if not appointment_date:
                missing_fields.append("التاريخ الجديد")

            if not appointment_time:
                missing_fields.append("الوقت الجديد")

            if missing_fields:
                return (
                    "لتعديل الموعد، أحتاج إلى: "
                    + "، ".join(missing_fields)
                    + "."
                )

            success, result = change_booking(
                db=db,
                phone=phone,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            )

            reset_conversation_state()

            return result

        # ==================================
        # إلغاء الحجز
        # ==================================

        if action == "cancel":
            if not phone:
                return (
                    "فضلاً، أرسل رقم الجوال "
                    "المرتبط بالحجز لإلغاء الموعد."
                )

            success, result = cancel_booking(
                db=db,
                phone=phone,
            )

            reset_conversation_state()

            return result

        # ==================================
        # الاستعلام عن الحجز
        # ==================================

        if action == "search":
            if not phone:
                return (
                    "فضلاً، أرسل رقم الجوال "
                    "المرتبط بالحجز للبحث عن الموعد."
                )

            booking = search_booking(
                db=db,
                phone=phone,
            )

            reset_conversation_state()

            if booking is None:
                return "لم يتم العثور على حجز مرتبط بهذا الرقم."

            booking_status = booking.get("status", "قادم")

            return (
                f"تم العثور على الحجز:\n"
                f"اسم العميل: {booking['customer_name']}\n"
                f"رقم الجوال: {booking['phone']}\n"
                f"تاريخ الموعد: {booking['appointment_date']}\n"
                f"وقت الموعد: {booking['appointment_time']}\n"
                f"حالة الحجز: {booking_status}"
            )

        # ==================================
        # المحادثة العادية
        # ==================================

        return reply

    except Exception as error:
        print(f"Gemini service error: {error}")

        return (
            "حدث خطأ أثناء تنفيذ طلبك. "
            "يرجى المحاولة مرة أخرى."
        )

    finally:
        db.close()