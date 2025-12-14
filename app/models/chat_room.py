from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.session import Base


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)

    user_one_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_two_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_one_id", "user_two_id", name="uq_chat_room_users"),
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        index=True,
    )

    user_one = relationship("User", foreign_keys=[user_one_id])
    user_two = relationship("User", foreign_keys=[user_two_id])
