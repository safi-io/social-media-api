import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship

from app.db.session import Base


class ProjectStatusEnum(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class VisibilityStatusEnum(enum.Enum):
    PUBLIC = "PUBLIC"
    UNLISTED = "UNLISTED"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    name = Column(String, nullable=False)
    description = Column(String)

    status = Column(Enum(ProjectStatusEnum, name="project_status", create_type=True))

    visibility = Column(Enum(VisibilityStatusEnum, name="visibility_status", create_type=True))

    external_urls = Column(JSONB, default=dict)
    analytics = Column(JSONB, default=dict)

    tech_stack = Column(ARRAY(String), default=list)

    # Relationship
    _assigned_members_relationships = relationship(
        "ProjectMember",
        foreign_keys="[ProjectMember.project_id]",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @property
    def assigned_members(self):
        return [mem.user for mem in self._assigned_members_relationships]
