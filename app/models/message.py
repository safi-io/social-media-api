import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func

from app.db.session import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(Integer, ForeignKey("chat_rooms.id"), index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        index=True,
    )
