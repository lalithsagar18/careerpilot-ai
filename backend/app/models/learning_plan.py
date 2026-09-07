import uuid
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class LearningPlan(Base, TimestampMixin):
    __tablename__ = "learning_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    skill_gap_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("skill_gaps.id", ondelete="SET NULL"), nullable=True)
    target_role: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_weeks: Mapped[int] = mapped_column(Integer, default=4)
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)

    user = relationship("User", back_populates="learning_plans")
    skill_gap = relationship("SkillGap", back_populates="learning_plans")
    items = relationship("LearningPlanItem", back_populates="learning_plan", cascade="all, delete-orphan", order_by="LearningPlanItem.order_index")

class LearningPlanItem(Base, TimestampMixin):
    __tablename__ = "learning_plan_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    learning_plan_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_plans.id", ondelete="CASCADE"), index=True, nullable=False)
    skill_name: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), default="high")  # high, medium, low
    difficulty: Mapped[str] = mapped_column(String(50), default="intermediate")
    objectives: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array
    resources: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of recommended courses/docs
    project_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    interview_practice_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    learning_plan = relationship("LearningPlan", back_populates="items")
