import uuid
from typing import Optional
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="technical", nullable=False)  # technical, soft, domain, tool
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

class UserSkill(Base, TimestampMixin):
    __tablename__ = "user_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    skill_id: Mapped[str] = mapped_column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False)
    proficiency: Mapped[str] = mapped_column(String(50), default="intermediate")  # beginner, intermediate, advanced, expert
    years_experience: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    evidence: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

class JobSkill(Base, TimestampMixin):
    __tablename__ = "job_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    skill_id: Mapped[str] = mapped_column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False)
    is_required: Mapped[bool] = mapped_column(default=True, nullable=False)
    importance_weight: Mapped[float] = mapped_column(default=1.0)
