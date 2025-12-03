from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)

    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar_url = Column(String(255))

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False)

    # Relationship 1: All Follow records where THIS user is the follower
    _following_relationships = relationship(
        "Follow",
        foreign_keys="[Follow.follower_id]",
        back_populates="follower",  # ← Links back to Follow.follower
        cascade="all, delete-orphan"
    )

    # Relationship 2: All Follow records where THIS user is being followed
    _follower_relationships = relationship(
        "Follow",
        foreign_keys="[Follow.following_id]",
        back_populates="following",  # ← Links back to Follow.following
        cascade="all, delete-orphan"
    )

    last_login_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @property
    def followers(self):
        """Returns a list of User objects who follow this user."""
        # 'rel.follower' comes from the relationship in the Follow model
        return [rel.follower for rel in self._follower_relationships]

    @property
    def followings(self):
        """Returns a list of User objects this user is following."""
        # 'rel.following' comes from the relationship in the Follow model
        return [rel.following for rel in self._following_relationships]

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
