import uuid
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "pdf", "docx", "txt"
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Active parsed candidate profile
    candidate_profile: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    health_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    health_assessment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string

    # Relationships
    user = relationship("User", back_populates="resumes")
    versions = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan", order_by="desc(ResumeVersion.version_number)")
    skill_gaps = relationship("SkillGap", back_populates="resume", cascade="all, delete-orphan")

class ResumeVersion(Base, TimestampMixin):
    __tablename__ = "resume_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    target_job_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    profile_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    ats_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ats_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    change_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_approved: Mapped[bool] = mapped_column(default=False)

    resume = relationship("Resume", back_populates="versions")
    target_job = relationship("Job")
