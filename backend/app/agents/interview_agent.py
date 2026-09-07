from datetime import datetime, timezone
import logging
from typing import List, Dict, Any, Optional
from app.core.ai_provider import AIProvider, get_ai_provider
from app.schemas.interview import InterviewAnswerFeedback, InterviewReport
from app.schemas.job import StructuredJobData

logger = logging.getLogger("careerpilot.agents.interview")

INTERVIEW_QUESTION_PROMPT = """
You are the CareerPilot AI Technical & Behavioral Interviewer.
Generate a realistic, insightful interview question tailored to the target role, seniority level, and previous candidate answers.
"""

INTERVIEW_EVAL_PROMPT = """
You are a Principal Engineer and Hiring Committee Evaluator.
Critique the candidate's answer for technical depth, correctness, structure, relevance, and communication.
Score the answer objectively (0-100) and highlight exact strengths, missing technical concepts, and an ideal exemplar answer.
"""

class AdaptiveInterviewAgent:
    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    async def generate_next_question(
        self,
        target_role: str,
        interview_type: str,
        order_index: int,
        previous_qa: List[Dict[str, str]] = None,
        job_data: Optional[StructuredJobData] = None
    ) -> Dict[str, Any]:
        context = ""
        if job_data:
            context += f"\nTarget Job: {job_data.title} at {job_data.company}. Key skills: {', '.join(job_data.required_skills)}"
        if previous_qa:
            context += "\nPrevious QA in this session:\n"
            for qa in previous_qa:
                context += f"Q: {qa.get('question')}\nA: {qa.get('answer')}\nScore: {qa.get('score')}\n"

        prompt = f"""
ROLE: {target_role}
INTERVIEW TYPE: {interview_type}
QUESTION NUMBER: {order_index}
CONTEXT: {context}

Generate question #{order_index} covering core competencies, edge cases, or adaptive follow-up on previous weaknesses:
"""
        q_text = await self.ai.generate_text(
            prompt=prompt,
            system_instruction=INTERVIEW_QUESTION_PROMPT,
            temperature=0.4
        )
        return {
            "question_text": q_text.strip(),
            "category": interview_type,
            "difficulty": "hard" if order_index > 3 else "medium",
            "order_index": order_index
        }

    async def generate_question(
        self,
        role: str,
        category: str = "technical",
        difficulty: str = "medium",
        history: list = None
    ) -> Dict[str, Any]:
        """Convenience wrapper matching Streamlit call signature."""
        return await self.generate_next_question(
            target_role=role,
            interview_type=category,
            order_index=len(history or []) + 1,
            previous_qa=history
        )

    async def evaluate_answer(
        self,
        question_text: str,
        user_answer_text: str = None,
        category: str = "Technical",
        answer_text: str = None,
    ) -> InterviewAnswerFeedback:
        ans = user_answer_text or answer_text or ""
        prompt = f"""
QUESTION:
{question_text}

CANDIDATE ANSWER:
{ans}

CATEGORY: {category}

Evaluate this response objectively:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=InterviewAnswerFeedback,
            system_instruction=INTERVIEW_EVAL_PROMPT
        )

    async def generate_final_report(
        self,
        interview_id: str,
        user_id: str,
        target_role: str,
        interview_type: str,
        qa_history: List[Dict[str, Any]]
    ) -> InterviewReport:
        now_dt = datetime.now(timezone.utc)
        if not qa_history:
            return InterviewReport(
                id=interview_id,
                user_id=user_id,
                target_role=target_role,
                interview_type=interview_type,
                status="completed",
                overall_score=0.0,
                total_questions=0,
                questions_answered=0,
                created_at=now_dt
            )

        avg_score = sum(qa.get("score", 0) for qa in qa_history) / len(qa_history)
        avg_tech = sum(qa.get("technical_accuracy_score", 0) for qa in qa_history) / len(qa_history)
        avg_rel = sum(qa.get("relevance_score", 0) for qa in qa_history) / len(qa_history)
        avg_depth = sum(qa.get("depth_score", 0) for qa in qa_history) / len(qa_history)
        avg_comm = sum(qa.get("communication_score", 0) for qa in qa_history) / len(qa_history)

        all_strengths = []
        all_missed = []
        for qa in qa_history:
            all_strengths.extend(qa.get("strengths", []))
            all_missed.extend(qa.get("missed_points", []))

        return InterviewReport(
            id=interview_id,
            user_id=user_id,
            target_role=target_role,
            interview_type=interview_type,
            status="completed",
            overall_score=round(avg_score, 1),
            category_scores={
                "technical_accuracy": round(avg_tech, 1),
                "relevance": round(avg_rel, 1),
                "depth": round(avg_depth, 1),
                "communication": round(avg_comm, 1),
            },
            strengths=list(set(all_strengths))[:5],
            weaknesses=list(set(all_missed))[:5],
            improvement_plan="Focus on deeper systems trade-offs and concrete performance metrics.",
            suggested_study_topics=["Distributed Systems", "Database Indexing", "Async Concurrency"],
            total_questions=len(qa_history),
            questions_answered=len(qa_history),
            created_at=now_dt
        )

