import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [message, setMessage] = useState('')

  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'مرحبًا بك، أنا مساعد العيادة الذكي. كيف أستطيع مساعدتك؟',
    },
  ])

  const [isLoading, setIsLoading] = useState(false)
  const [activePage, setActivePage] = useState('dashboard')

  const [bookings, setBookings] = useState([])
  const [bookingsLoading, setBookingsLoading] = useState(false)
  const [bookingsError, setBookingsError] = useState('')

  const fetchBookings = async () => {
    setBookingsLoading(true)
    setBookingsError('')

    try {
      const response = await axios.get(
        'http://127.0.0.1:8000/bookings'
      )

      setBookings(response.data)
    } catch (error) {
      console.error('Error loading bookings:', error)

      setBookingsError(
        'حدث خطأ أثناء تحميل الحجوزات. تأكدي أن الباك إند يعمل.'
      )
    } finally {
      setBookingsLoading(false)
    }
  }

  useEffect(() => {
    fetchBookings()
  }, [])

  const openBookingsPage = async () => {
    setActivePage('bookings')
    await fetchBookings()
  }

  const sendMessage = async () => {
    if (!message.trim() || isLoading) return

    const userMessage = message.trim()

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        sender: 'user',
        text: userMessage,
      },
    ])

    setMessage('')
    setIsLoading(true)

    try {
      const response = await axios.get(
        'http://127.0.0.1:8000/chat',
        {
          params: {
            message: userMessage,
          },
        }
      )

      const botResponse =
        response.data.ai ||
        response.data.response ||
        response.data.reply ||
        response.data.message ||
        response.data

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          sender: 'bot',
          text:
            typeof botResponse === 'string'
              ? botResponse
              : JSON.stringify(botResponse),
        },
      ])

      await fetchBookings()
    } catch (error) {
      console.error('Error connecting to backend:', error)

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          sender: 'bot',
          text: 'حدث خطأ في الاتصال بالخادم. تأكدي أن الباك إند يعمل.',
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusClass = (status) => {
    if (status === 'ملغي') {
      return 'status-cancelled'
    }

    if (status === 'تم التعديل') {
      return 'status-updated'
    }

    return 'status-upcoming'
  }

  const totalBookings = bookings.length

  const uniqueCustomers = new Set(
    bookings.map((booking) => booking.phone)
  ).size

  const today = new Date().toISOString().split('T')[0]

  const todayBookings = bookings.filter(
    (booking) => booking.appointment_date === today
  ).length

  return (
    <div className="app" dir="rtl">
      <header className="header">
        <div>
          <h1>نظام مساعد المبيعات الذكي</h1>
          <p>خدمة العملاء والحجوزات باستخدام الذكاء الاصطناعي</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          متصل
        </div>
      </header>

      <main className="main">
        <aside className="sidebar">
          <h2>الخدمات</h2>

          <button
            type="button"
            className={`menu-button ${
              activePage === 'dashboard' ? 'active' : ''
            }`}
            onClick={() => setActivePage('dashboard')}
          >
            لوحة التحكم
          </button>

          <button
            type="button"
            className={`menu-button ${
              activePage === 'chat' ? 'active' : ''
            }`}
            onClick={() => setActivePage('chat')}
          >
            المحادثة الذكية
          </button>

          <button
            type="button"
            className={`menu-button ${
              activePage === 'bookings' ? 'active' : ''
            }`}
            onClick={openBookingsPage}
          >
            عرض الحجوزات
          </button>

          <button
            type="button"
            className="menu-button"
            onClick={() => {
              setActivePage('chat')
              setMessage('أريد حجز موعد جديد')
            }}
          >
            حجز موعد
          </button>

          <button
            type="button"
            className="menu-button"
            onClick={() => {
              setActivePage('chat')
              setMessage('أريد تعديل موعدي')
            }}
          >
            تعديل موعد
          </button>

          <button
            type="button"
            className="menu-button"
            onClick={() => {
              setActivePage('chat')
              setMessage('أريد إلغاء موعدي')
            }}
          >
            إلغاء موعد
          </button>

          <button
            type="button"
            className="menu-button"
            onClick={() => {
              setActivePage('chat')
              setMessage('أريد البحث عن موعدي')
            }}
          >
            البحث عن موعد
          </button>
        </aside>

        {activePage === 'dashboard' && (
          <section className="dashboard">
            <div className="dashboard-header">
              <div>
                <h2>لوحة التحكم</h2>
                <p>ملخص سريع لحالة النظام والحجوزات</p>
              </div>

              <button
                type="button"
                className="refresh-button"
                onClick={fetchBookings}
                disabled={bookingsLoading}
              >
                {bookingsLoading ? 'جاري التحديث...' : 'تحديث البيانات'}
              </button>
            </div>

            {bookingsError && (
              <div className="bookings-error">
                {bookingsError}
              </div>
            )}

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">📅</div>

                <div>
                  <p>إجمالي الحجوزات</p>
                  <h3>{totalBookings}</h3>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">👥</div>

                <div>
                  <p>عدد العملاء</p>
                  <h3>{uniqueCustomers}</h3>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🗓️</div>

                <div>
                  <p>حجوزات اليوم</p>
                  <h3>{todayBookings}</h3>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🤖</div>

                <div>
                  <p>حالة النظام</p>
                  <h3 className="system-online">متصل</h3>
                </div>
              </div>
            </div>

            <div className="dashboard-content">
              <div className="dashboard-section">
                <div className="section-header">
                  <div>
                    <h3>آخر الحجوزات</h3>
                    <p>أحدث المواعيد المسجلة في النظام</p>
                  </div>

                  <button
                    type="button"
                    className="small-button"
                    onClick={openBookingsPage}
                  >
                    عرض الكل
                  </button>
                </div>

                {bookingsLoading && (
                  <div className="empty-bookings">
                    جاري تحميل الحجوزات...
                  </div>
                )}

                {!bookingsLoading && bookings.length === 0 && (
                  <div className="empty-bookings">
                    لا توجد حجوزات حاليًا.
                  </div>
                )}

                {!bookingsLoading && bookings.length > 0 && (
                  <div className="table-container">
                    <table className="bookings-table">
                      <thead>
                        <tr>
                          <th>اسم العميل</th>
                          <th>رقم الجوال</th>
                          <th>التاريخ</th>
                          <th>الوقت</th>
                          <th>الحالة</th>
                        </tr>
                      </thead>

                      <tbody>
                        {bookings
                          .slice(-5)
                          .reverse()
                          .map((booking) => (
                            <tr key={booking.id}>
                              <td>{booking.customer_name}</td>
                              <td>{booking.phone}</td>
                              <td>{booking.appointment_date}</td>
                              <td>{booking.appointment_time}</td>

                              <td>
                                <span
                                  className={`status-badge ${getStatusClass(
                                    booking.status
                                  )}`}
                                >
                                  {booking.status || 'قادم'}
                                </span>
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>

              <div className="dashboard-section quick-actions">
                <div className="section-header">
                  <div>
                    <h3>إجراءات سريعة</h3>
                    <p>اختصارات لتنفيذ العمليات الأساسية</p>
                  </div>
                </div>

                <button
                  type="button"
                  className="quick-action-button"
                  onClick={() => {
                    setActivePage('chat')
                    setMessage('أريد حجز موعد جديد')
                  }}
                >
                  حجز موعد جديد
                </button>

                <button
                  type="button"
                  className="quick-action-button"
                  onClick={() => {
                    setActivePage('chat')
                    setMessage('أريد البحث عن موعدي')
                  }}
                >
                  البحث عن موعد
                </button>

                <button
                  type="button"
                  className="quick-action-button"
                  onClick={() => {
                    setActivePage('chat')
                    setMessage('أريد تعديل موعدي')
                  }}
                >
                  تعديل موعد
                </button>

                <button
                  type="button"
                  className="quick-action-button danger-button"
                  onClick={() => {
                    setActivePage('chat')
                    setMessage('أريد إلغاء موعدي')
                  }}
                >
                  إلغاء موعد
                </button>
              </div>
            </div>
          </section>
        )}

        {activePage === 'chat' && (
          <section className="chat-card">
            <div className="chat-header">
              <div>
                <h2>مساعد العيادة</h2>
                <p>متاح للرد على العملاء على مدار الساعة</p>
              </div>

              <div className="bot-icon">AI</div>
            </div>

            <div className="messages">
              {messages.map((item, index) => (
                <div
                  key={`${item.sender}-${index}`}
                  className={`message ${
                    item.sender === 'user'
                      ? 'user-message'
                      : 'bot-message'
                  }`}
                >
                  {item.text}
                </div>
              ))}

              {isLoading && (
                <div className="message bot-message">
                  جاري كتابة الرد...
                </div>
              )}
            </div>

            <div className="input-area">
              <input
                type="text"
                placeholder="اكتبي رسالتك هنا..."
                value={message}
                disabled={isLoading}
                onChange={(event) => setMessage(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') {
                    sendMessage()
                  }
                }}
              />

              <button
                type="button"
                onClick={sendMessage}
                disabled={isLoading}
              >
                {isLoading ? 'انتظري...' : 'إرسال'}
              </button>
            </div>
          </section>
        )}

        {activePage === 'bookings' && (
          <section className="bookings-card">
            <div className="bookings-header">
              <div>
                <h2>جميع الحجوزات</h2>
                <p>عرض المواعيد المحفوظة في قاعدة البيانات</p>
              </div>

              <button
                type="button"
                className="refresh-button"
                onClick={fetchBookings}
                disabled={bookingsLoading}
              >
                {bookingsLoading ? 'جاري التحديث...' : 'تحديث'}
              </button>
            </div>

            {bookingsError && (
              <div className="bookings-error">
                {bookingsError}
              </div>
            )}

            {!bookingsLoading &&
              !bookingsError &&
              bookings.length === 0 && (
                <div className="empty-bookings">
                  لا توجد حجوزات حاليًا.
                </div>
              )}

            {!bookingsError && bookings.length > 0 && (
              <div className="table-container">
                <table className="bookings-table">
                  <thead>
                    <tr>
                      <th>رقم الحجز</th>
                      <th>اسم العميل</th>
                      <th>رقم الجوال</th>
                      <th>تاريخ الموعد</th>
                      <th>وقت الموعد</th>
                      <th>الحالة</th>
                    </tr>
                  </thead>

                  <tbody>
                    {bookings.map((booking) => (
                      <tr key={booking.id}>
                        <td>{booking.id}</td>
                        <td>{booking.customer_name}</td>
                        <td>{booking.phone}</td>
                        <td>{booking.appointment_date}</td>
                        <td>{booking.appointment_time}</td>

                        <td>
                          <span
                            className={`status-badge ${getStatusClass(
                              booking.status
                            )}`}
                          >
                            {booking.status === "ملغي"
  ? "🔴 ملغي"
  : booking.status === "تم التعديل"
  ? "🟡 تم التعديل"
  : "🟢 قادم"}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default App