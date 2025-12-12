from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from app.db.session import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    role = Column(String, nullable=False)
    joined_at = Column(DateTime)
