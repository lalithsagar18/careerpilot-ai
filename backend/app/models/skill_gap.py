import uuid
from typing import Optional
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class SkillGap(Base, TimestampMixin):
    __tablename__ = "skill_gaps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)

    # Deterministic Scores (0-100)
    overall_match_score: Mapped[float] = mapped_column(Float, nullable=False)
    required_skill_score: Mapped[float] = mapped_column(Float, nullable=False)
    preferred_skill_score: Mapped[float] = mapped_column(Float, nullable=False)
    experience_score: Mapped[float] = mapped_column(Float, nullable=False)
    technology_score: Mapped[float] = mapped_column(Float, nullable=False)
    education_score: Mapped[float] = mapped_column(Float, nullable=False)

    # Detailed Matrices (JSON)
    matching_skills: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array
    missing_skills: Mapped[str] = mapped_column(Text, nullable=False)   # JSON array
    partial_skills: Mapped[str] = mapped_column(Text, nullable=False)   # JSON array
    explanation: Mapped[str] = mapped_column(Text, nullable=False)      # AI synthesis of deterministic score

    # Relationships
    resume = relationship("Resume", back_populates="skill_gaps")
    job = relationship("Job", back_populates="skill_gaps")
    learning_plans = relationship("LearningPlan", back_populates="skill_gap", cascade="all, delete-orphan")
