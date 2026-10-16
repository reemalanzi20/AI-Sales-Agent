from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    ai_message = Column(String)