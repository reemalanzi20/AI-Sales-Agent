# 🤖 AI Sales & Clinic Appointment Assistant

نظام ذكي لإدارة حجوزات العيادات وخدمة العملاء يتكامل مع الذكاء الاصطناعي (Google Gemini API) لتقديم تجربة حجز وحوار تفاعلية باللغة الطبيعية، مع توفير لوحة تحكم متكاملة لإدارة البيانات.

---

## 🌟 المميزات الرئيسية (Key Features)

- **مساعد ذكي تفاعلي:** فهم طلبات الحجز والتعديل والإلغاء والاستعلام باللغة الطبيعية.
- **لوحة تحكم (Dashboard):** عرض إحصائيات فورية لعدد الحجوزات، العملاء، وحالة النظام.
- **إدارة الحجوزات:** حفظ وتحديث الحجوزات بشكل لحظي في قاعدة البيانات.
- **توثيق API تفاعلي:** توثيق متكامل للمسارات باستعمال Swagger UI / FastAPI Docs.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

- **Frontend:** React.js, Vite, Axios, CSS3
- **Backend:** Python, FastAPI, Uvicorn
- **Database:** SQLite, SQLAlchemy ORM
- **AI Integration:** Google Gemini API

---

## 📸 لقطات من الشاشة (Screenshots)

<img width="1917" height="1075" alt="لقطة شاشة 2026-10-16 182234" src="https://github.com/user-attachments/assets/bb7a4b1f-eed4-4596-9160-f5b7a9713182" />
<img width="1917" height="1077" alt="لقطة شاشة 2026-10-16 182018" src="https://github.com/user-attachments/assets/266f8ffa-3f1a-4ff1-acb1-befbfdaea806" />
<img width="1402" height="907" alt="لقطة شاشة 2026-10-16 181336" src="https://github.com/user-attachments/assets/345249a9-9ceb-4efd-920b-8a2a11f5391f" />
<img width="1407" height="908" alt="لقطة شاشة 2026-10-16 180728" src="https://github.com/user-attachments/assets/652db126-e5af-4d24-a53b-8d46ae1c9321" />
<img width="1407" height="916" alt="لقطة شاشة 2026-10-16 180714" src="https://github.com/user-attachments/assets/fa8dee38-048b-4af5-866d-6cd4adb58590" />
<img width="1412" height="912" alt="لقطة شاشة 2026-10-16 180609" src="https://github.com/user-attachments/assets/4d0e7b55-b900-4d8a-ad89-570cd123debc" />
<img width="1407" height="911" alt="لقطة شاشة 2026-10-16 180533" src="https://github.com/user-attachments/assets/683fe4df-e451-47d1-8dc0-8d36f3c15f9d" />
<img width="1403" height="907" alt="لقطة شاشة 2026-10-16 175727" src="https://github.com/user-attachments/assets/ca5da46e-6e1c-4aa1-8b75-a5da5a99f5d2" />
<img width="1402" height="910" alt="لقطة شاشة 2026-10-16 175641" src="https://github.com/user-attachments/assets/7d95fe84-2e15-4bce-8d54-c3560ff53f39" />

---

## 🚀 طريقة التشغيل محلياً (How to Run)

### 1. تشغيل الباك إند (Backend):
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reloadcd frontend
npm install
npm run dev
