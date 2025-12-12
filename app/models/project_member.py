from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    role = Column(String, nullable=False)

    project = relationship("Project", foreign_keys=[project_id], back_populates="_assigned_members_relationships")

    user = relationship("User", foreign_keys=[user_id])

    joined_at = Column(DateTime)
