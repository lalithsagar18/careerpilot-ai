import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.skill_gap import SkillGap
from app.schemas.skill_gap import SkillGapCalculateRequest, SkillGapResponse, ScoreBreakdown, MatchedSkill, MissingSkill, PartialSkill
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.tools.scoring_engine import DeterministicScoringEngine
from app.api.deps import get_current_user
from app.core.ai_provider import get_ai_provider

router = APIRouter(prefix="/match", tags=["Job Match & Skill Gap"])

@router.post("/calculate", response_model=SkillGapResponse)
async def calculate_match(
    payload: SkillGapCalculateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fetch user resume
    res_stmt = select(Resume).where(Resume.id == payload.resume_id, Resume.user_id == current_user.id)
    resume = (await db.execute(res_stmt)).scalars().first()
    if not resume or not resume.candidate_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or not parsed.")

    # Fetch job
    job_stmt = select(Job).where(Job.id == payload.job_id, Job.user_id == current_user.id)
    job = (await db.execute(job_stmt)).scalars().first()
    if not job or not job.parsed_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found or not parsed.")

    cand_profile = CandidateProfile.model_validate(json.loads(resume.candidate_profile))
    job_data = StructuredJobData.model_validate(json.loads(job.parsed_data))

    # 1. Deterministic Calculation (Zero LLM hallucination in numeric score)
    breakdown, matched, missing, partial = DeterministicScoringEngine.calculate_match(cand_profile, job_data)

    # 2. AI Synthesis of the score explanation
    ai = get_ai_provider()
    expl_prompt = f"""
Candidate: {cand_profile.summary or cand_profile.full_name}
Target Job: {job_data.title} at {job_data.company}
Deterministic Match Score: {breakdown.overall_score}%
Required Skills Score: {breakdown.required_skill_score}%
Experience Score: {breakdown.experience_score}%
Matched Skills: {', '.join([m.skill_name for m in matched])}
Critical Missing Skills: {', '.join([m.skill_name for m in missing])}

Synthesize a 2-3 paragraph professional, objective explanation of this match score and prioritized gaps.
"""
    explanation_text = await ai.generate_text(expl_prompt, temperature=0.2)

    # Persist or update SkillGap record
    existing_stmt = select(SkillGap).where(
        SkillGap.user_id == current_user.id,
        SkillGap.resume_id == payload.resume_id,
        SkillGap.job_id == payload.job_id
    )
    skill_gap = (await db.execute(existing_stmt)).scalars().first()

    if not skill_gap:
        skill_gap = SkillGap(
            user_id=current_user.id,
            resume_id=payload.resume_id,
            job_id=payload.job_id,
            overall_match_score=breakdown.overall_score,
            required_skill_score=breakdown.required_skill_score,
            preferred_skill_score=breakdown.preferred_skill_score,
            experience_score=breakdown.experience_score,
            technology_score=breakdown.technology_score,
            education_score=breakdown.education_score,
            matching_skills=json.dumps([m.model_dump() for m in matched]),
            missing_skills=json.dumps([m.model_dump() for m in missing]),
            partial_skills=json.dumps([p.model_dump() for p in partial]),
            explanation=explanation_text
        )
        db.add(skill_gap)
    else:
        skill_gap.overall_match_score = breakdown.overall_score
        skill_gap.required_skill_score = breakdown.required_skill_score
        skill_gap.preferred_skill_score = breakdown.preferred_skill_score
        skill_gap.experience_score = breakdown.experience_score
        skill_gap.technology_score = breakdown.technology_score
        skill_gap.education_score = breakdown.education_score
        skill_gap.matching_skills = json.dumps([m.model_dump() for m in matched])
        skill_gap.missing_skills = json.dumps([m.model_dump() for m in missing])
        skill_gap.partial_skills = json.dumps([p.model_dump() for p in partial])
        skill_gap.explanation = explanation_text

    await db.commit()
    await db.refresh(skill_gap)

    return SkillGapResponse(
        id=skill_gap.id,
        user_id=skill_gap.user_id,
        resume_id=skill_gap.resume_id,
        job_id=skill_gap.job_id,
        score_breakdown=breakdown,
        matching_skills=matched,
        missing_skills=missing,
        partial_skills=partial,
        explanation=explanation_text,
        created_at=skill_gap.created_at
    )
