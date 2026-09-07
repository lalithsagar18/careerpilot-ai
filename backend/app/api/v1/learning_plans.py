import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.skill_gap import SkillGap
from app.models.resume import Resume
from app.models.job import Job
from app.models.learning_plan import LearningPlan, LearningPlanItem
from app.schemas.learning_plan import LearningPlanResponse, LearningPlanItemResponse
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.schemas.skill_gap import MissingSkill, PartialSkill
from app.api.deps import get_current_user
from app.agents.learning_agent import LearningPlanAgent

router = APIRouter(prefix="/learning-plans", tags=["Learning Roadmaps"])

@router.post("/generate/{skill_gap_id}", response_model=LearningPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_learning_plan(
    skill_gap_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    gap_stmt = select(SkillGap).where(SkillGap.id == skill_gap_id, SkillGap.user_id == current_user.id)
    gap = (await db.execute(gap_stmt)).scalars().first()
    if not gap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill gap record not found.")

    res_stmt = select(Resume).where(Resume.id == gap.resume_id)
    resume = (await db.execute(res_stmt)).scalars().first()
    job_stmt = select(Job).where(Job.id == gap.job_id)
    job = (await db.execute(job_stmt)).scalars().first()

    cand = CandidateProfile.model_validate(json.loads(resume.candidate_profile))
    job_data = StructuredJobData.model_validate(json.loads(job.parsed_data))
    missing = [MissingSkill.model_validate(m) for m in json.loads(gap.missing_skills)]
    partial = [PartialSkill.model_validate(p) for p in json.loads(gap.partial_skills)]

    agent = LearningPlanAgent()
    plan_data = await agent.generate_plan(
        candidate=cand,
        job=job_data,
        missing_skills=missing,
        partial_skills=partial
    )

    plan = LearningPlan(
        user_id=current_user.id,
        skill_gap_id=gap.id,
        target_role=plan_data.target_role,
        summary=plan_data.summary,
        estimated_weeks=plan_data.estimated_weeks,
        completion_percentage=0.0
    )
    db.add(plan)
    await db.commit()
    await db.refresh(plan)

    items_response = []
    for i, item_in in enumerate(plan_data.items):
        item = LearningPlanItem(
            learning_plan_id=plan.id,
            skill_name=item_in.skill_name,
            priority=item_in.priority,
            difficulty=item_in.difficulty,
            objectives=json.dumps(item_in.objectives),
            resources=json.dumps(item_in.resources or []),
            project_suggestion=item_in.project_suggestion,
            interview_practice_prompt=item_in.interview_practice_prompt,
            order_index=i + 1,
            is_completed=False
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)

        items_response.append(LearningPlanItemResponse(
            id=item.id,
            learning_plan_id=item.learning_plan_id,
            skill_name=item.skill_name,
            priority=item.priority,
            difficulty=item.difficulty,
            objectives=item_in.objectives,
            resources=item_in.resources,
            project_suggestion=item.project_suggestion,
            interview_practice_prompt=item.interview_practice_prompt,
            order_index=item.order_index,
            is_completed=item.is_completed
        ))

    return LearningPlanResponse(
        id=plan.id,
        user_id=plan.user_id,
        skill_gap_id=plan.skill_gap_id,
        target_role=plan.target_role,
        summary=plan.summary,
        estimated_weeks=plan.estimated_weeks,
        completion_percentage=plan.completion_percentage,
        items=items_response,
        created_at=plan.created_at
    )

@router.get("", response_model=List[LearningPlanResponse])
async def list_learning_plans(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(LearningPlan).where(LearningPlan.user_id == current_user.id).order_by(LearningPlan.created_at.desc())
    plans = (await db.execute(stmt)).scalars().all()

    response_list = []
    for p in plans:
        item_stmt = select(LearningPlanItem).where(LearningPlanItem.learning_plan_id == p.id).order_by(LearningPlanItem.order_index)
        items = (await db.execute(item_stmt)).scalars().all()
        items_res = []
        for it in items:
            items_res.append(LearningPlanItemResponse(
                id=it.id,
                learning_plan_id=it.learning_plan_id,
                skill_name=it.skill_name,
                priority=it.priority,
                difficulty=it.difficulty,
                objectives=json.loads(it.objectives) if it.objectives else [],
                resources=json.loads(it.resources) if it.resources else [],
                project_suggestion=it.project_suggestion,
                interview_practice_prompt=it.interview_practice_prompt,
                order_index=it.order_index,
                is_completed=it.is_completed
            ))
        response_list.append(LearningPlanResponse(
            id=p.id,
            user_id=p.user_id,
            skill_gap_id=p.skill_gap_id,
            target_role=p.target_role,
            summary=p.summary,
            estimated_weeks=p.estimated_weeks,
            completion_percentage=p.completion_percentage,
            items=items_res,
            created_at=p.created_at
        ))
    return response_list

@router.patch("/items/{item_id}/toggle")
async def toggle_item_completed(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(LearningPlanItem)
        .join(LearningPlan, LearningPlanItem.learning_plan_id == LearningPlan.id)
        .where(LearningPlanItem.id == item_id, LearningPlan.user_id == current_user.id)
    )
    item = (await db.execute(stmt)).scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

    item.is_completed = not item.is_completed
    await db.commit()

    # Recalculate plan percentage
    all_items_stmt = select(LearningPlanItem).where(LearningPlanItem.learning_plan_id == item.learning_plan_id)
    all_items = (await db.execute(all_items_stmt)).scalars().all()
    completed_count = sum(1 for x in all_items if x.is_completed)
    pct = round((completed_count / len(all_items)) * 100.0, 1) if all_items else 0.0

    plan_stmt = select(LearningPlan).where(LearningPlan.id == item.learning_plan_id)
    plan = (await db.execute(plan_stmt)).scalars().first()
    if plan:
        plan.completion_percentage = pct
        await db.commit()

    return {"id": item.id, "is_completed": item.is_completed, "plan_completion_percentage": pct}
