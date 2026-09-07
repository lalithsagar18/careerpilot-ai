import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Application(Base, TimestampMixin):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    job_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    resume_version_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("resume_versions.id", ondelete="SET NULL"), nullable=True)
    
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Saved")  # Saved, Preparing, Applied, Interview, Offer, Rejected, Withdrawn
    applied_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cover_letter_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    salary_offered: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume_version = relationship("ResumeVersion")
