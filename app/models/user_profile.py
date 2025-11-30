from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    title = Column(String)
    bio = Column(String)
    skills = Column(ARRAY(String), default=list)
    cover_image_url = Column(String)
    location = Column(String)

    external_urls = Column(JSONB, default=dict)

    profile_strength = Column(Integer, default=0)

    user = relationship("User", back_populates="profile")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
