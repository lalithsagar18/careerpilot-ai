import uuid
from typing import Optional, List
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    company: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Full-time, Remote, etc.
    seniority: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Senior, Mid, Junior, Lead
    source_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    raw_description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Structured extraction
    parsed_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string

    # Relationships
    user = relationship("User", back_populates="jobs")
    requirements = relationship("JobRequirement", back_populates="job", cascade="all, delete-orphan")
    skill_gaps = relationship("SkillGap", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="job", cascade="all, delete-orphan")

class JobRequirement(Base, TimestampMixin):
    __tablename__ = "job_requirements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # "required_skill", "preferred_skill", "education", "experience", "technology"
    requirement_text: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[float] = mapped_column(default=1.0)
    normalized_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    job = relationship("Job", back_populates="requirements")
