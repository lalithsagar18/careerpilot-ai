import uuid
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Interview(Base, TimestampMixin):
    __tablename__ = "interviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    job_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    interview_type: Mapped[str] = mapped_column(String(100), default="Technical")  # Technical, Behavioral, System Design, Data Science, Python, SQL, ML
    target_role: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="in_progress")  # in_progress, completed, abandoned
    total_questions: Mapped[int] = mapped_column(Integer, default=5)
    
    # Final Report & Aggregated Scores (0-100)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    category_scores: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON object {technical_accuracy, communication, etc}
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    weaknesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    improvement_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suggested_study_topics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array

    user = relationship("User", back_populates="interviews")
    job = relationship("Job", back_populates="interviews")
    questions = relationship("InterviewQuestion", back_populates="interview", cascade="all, delete-orphan", order_by="InterviewQuestion.order_index")

class InterviewQuestion(Base, TimestampMixin):
    __tablename__ = "interview_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id: Mapped[str] = mapped_column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), index=True, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), default="medium")
    expected_key_points: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    order_index: Mapped[int] = mapped_column(Integer, default=1)
    is_follow_up: Mapped[bool] = mapped_column(default=False)

    interview = relationship("Interview", back_populates="questions")
    answer = relationship("InterviewAnswer", back_populates="question", uselist=False, cascade="all, delete-orphan")

class InterviewAnswer(Base, TimestampMixin):
    __tablename__ = "interview_answers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_questions.id", ondelete="CASCADE"), index=True, nullable=False)
    user_answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Detailed Evaluation
    score: Mapped[float] = mapped_column(Float, nullable=False)  # 0-100
    technical_accuracy_score: Mapped[float] = mapped_column(Float, default=0.0)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0)
    depth_score: Mapped[float] = mapped_column(Float, default=0.0)
    communication_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    missed_points: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    suggested_ideal_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    question = relationship("InterviewQuestion", back_populates="answer")
