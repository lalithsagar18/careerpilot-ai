import uuid
from typing import Optional
from sqlalchemy import String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Evaluation(Base, TimestampMixin):
    __tablename__ = "evaluations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "resume_optimization", "cover_letter", "rag_answer", "interview_evaluation"
    target_id: Mapped[str] = mapped_column(String(36), nullable=False)
    
    # Evaluation Metrics (0.0 to 1.0 or 0 to 100)
    factual_consistency_score: Mapped[float] = mapped_column(Float, default=1.0)
    groundedness_score: Mapped[float] = mapped_column(Float, default=1.0)
    relevance_score: Mapped[float] = mapped_column(Float, default=1.0)
    quality_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    passes_threshold: Mapped[bool] = mapped_column(Boolean, default=True)
    critique_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detected_hallucinations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    revision_count: Mapped[int] = mapped_column(default=0)

class Approval(Base, TimestampMixin):
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "resume_version", "cover_letter", "learning_plan"
    artifact_id: Mapped[str] = mapped_column(String(36), nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, approved, rejected, edited
    user_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    final_artifact_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
