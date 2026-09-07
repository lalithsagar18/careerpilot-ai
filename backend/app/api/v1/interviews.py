import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.job import Job
from app.models.interview import Interview, InterviewQuestion, InterviewAnswer
from app.schemas.interview import (
    InterviewStartRequest,
    InterviewQuestionResponse,
    InterviewSubmitAnswerRequest,
    InterviewAnswerFeedback,
    InterviewReport
)
from app.schemas.job import StructuredJobData
from app.api.deps import get_current_user
from app.agents.interview_agent import AdaptiveInterviewAgent

router = APIRouter(prefix="/interviews", tags=["Mock Interview Center"])

@router.post("/start", response_model=InterviewQuestionResponse, status_code=status.HTTP_201_CREATED)
async def start_interview(
    payload: InterviewStartRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    job_data = None
    if payload.job_id:
        job_stmt = select(Job).where(Job.id == payload.job_id, Job.user_id == current_user.id)
        job_row = (await db.execute(job_stmt)).scalars().first()
        if job_row and job_row.parsed_data:
            job_data = StructuredJobData.model_validate(json.loads(job_row.parsed_data))

    interview = Interview(
        user_id=current_user.id,
        job_id=payload.job_id,
        interview_type=payload.interview_type,
        target_role=payload.target_role,
        status="in_progress",
        total_questions=payload.total_questions
    )
    db.add(interview)
    await db.commit()
    await db.refresh(interview)

    # Generate Question #1
    agent = AdaptiveInterviewAgent()
    q_data = await agent.generate_next_question(
        target_role=payload.target_role,
        interview_type=payload.interview_type,
        order_index=1,
        job_data=job_data
    )

    question = InterviewQuestion(
        interview_id=interview.id,
        question_text=q_data["question_text"],
        category=q_data["category"],
        difficulty=q_data["difficulty"],
        order_index=1,
        is_follow_up=False
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)

    return InterviewQuestionResponse.model_validate(question)

@router.post("/answer", response_model=InterviewAnswerFeedback)
async def submit_answer(
    payload: InterviewSubmitAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Retrieve question
    q_stmt = (
        select(InterviewQuestion)
        .join(Interview, InterviewQuestion.interview_id == Interview.id)
        .where(
            InterviewQuestion.id == payload.question_id,
            Interview.user_id == current_user.id
        )
    )
    q_row = (await db.execute(q_stmt)).scalars().first()
    if not q_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview question not found.")

    # Evaluate answer with agent
    agent = AdaptiveInterviewAgent()
    feedback = await agent.evaluate_answer(
        question_text=q_row.question_text,
        user_answer_text=payload.user_answer_text,
        category=q_row.category
    )

    # Save answer
    answer = InterviewAnswer(
        question_id=q_row.id,
        user_answer_text=payload.user_answer_text,
        score=feedback.score,
        technical_accuracy_score=feedback.technical_accuracy_score,
        relevance_score=feedback.relevance_score,
        depth_score=feedback.depth_score,
        communication_score=feedback.communication_score,
        feedback=feedback.feedback,
        strengths=json.dumps(feedback.strengths),
        missed_points=json.dumps(feedback.missed_points),
        suggested_ideal_answer=feedback.suggested_ideal_answer
    )
    db.add(answer)
    await db.commit()

    return feedback

@router.post("/{interview_id}/next-question", response_model=InterviewQuestionResponse)
async def get_next_question(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    int_stmt = select(Interview).where(Interview.id == interview_id, Interview.user_id == current_user.id)
    interview = (await db.execute(int_stmt)).scalars().first()
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")

    # Retrieve existing questions & answers
    q_stmt = select(InterviewQuestion).where(InterviewQuestion.interview_id == interview_id).order_by(InterviewQuestion.order_index)
    existing_q = (await db.execute(q_stmt)).scalars().all()

    next_index = len(existing_q) + 1
    if next_index > interview.total_questions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All questions for this interview session are complete.")

    qa_history = []
    for q in existing_q:
        ans_stmt = select(InterviewAnswer).where(InterviewAnswer.question_id == q.id)
        ans = (await db.execute(ans_stmt)).scalars().first()
        if ans:
            qa_history.append({
                "question": q.question_text,
                "answer": ans.user_answer_text,
                "score": ans.score
            })

    agent = AdaptiveInterviewAgent()
    q_data = await agent.generate_next_question(
        target_role=interview.target_role,
        interview_type=interview.interview_type,
        order_index=next_index,
        previous_qa=qa_history
    )

    question = InterviewQuestion(
        interview_id=interview.id,
        question_text=q_data["question_text"],
        category=q_data["category"],
        difficulty=q_data["difficulty"],
        order_index=next_index,
        is_follow_up=next_index > 1
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)

    return InterviewQuestionResponse.model_validate(question)

@router.get("/{interview_id}/report", response_model=InterviewReport)
async def get_interview_report(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    int_stmt = select(Interview).where(Interview.id == interview_id, Interview.user_id == current_user.id)
    interview = (await db.execute(int_stmt)).scalars().first()
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")

    q_stmt = select(InterviewQuestion).where(InterviewQuestion.interview_id == interview_id).order_by(InterviewQuestion.order_index)
    questions = (await db.execute(q_stmt)).scalars().all()

    qa_history = []
    for q in questions:
        ans_stmt = select(InterviewAnswer).where(InterviewAnswer.question_id == q.id)
        ans = (await db.execute(ans_stmt)).scalars().first()
        if ans:
            qa_history.append({
                "score": ans.score,
                "technical_accuracy_score": ans.technical_accuracy_score,
                "relevance_score": ans.relevance_score,
                "depth_score": ans.depth_score,
                "communication_score": ans.communication_score,
                "strengths": json.loads(ans.strengths) if ans.strengths else [],
                "missed_points": json.loads(ans.missed_points) if ans.missed_points else [],
            })

    agent = AdaptiveInterviewAgent()
    report = await agent.generate_final_report(
        interview_id=interview.id,
        user_id=current_user.id,
        target_role=interview.target_role,
        interview_type=interview.interview_type,
        qa_history=qa_history
    )

    # Update interview record
    interview.status = "completed"
    interview.overall_score = report.overall_score
    interview.category_scores = json.dumps(report.category_scores)
    interview.strengths = json.dumps(report.strengths)
    interview.weaknesses = json.dumps(report.weaknesses)
    interview.improvement_plan = report.improvement_plan
    interview.suggested_study_topics = json.dumps(report.suggested_study_topics)
    await db.commit()

    return report
