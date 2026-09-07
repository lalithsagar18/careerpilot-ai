import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.skill_gap import SkillGap
from app.models.application import Application
from app.models.learning_plan import LearningPlan
from app.models.interview import Interview
from app.schemas.resume import CandidateProfile
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard Intelligence"])

@router.get("/metrics")
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Resumes
    res_stmt = select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.created_at.desc())
    resumes = (await db.execute(res_stmt)).scalars().all()
    latest_resume = resumes[0] if resumes else None
    resume_score = latest_resume.health_score if (latest_resume and latest_resume.health_score) else 85.0

    # 2. Extract Top Skills
    top_skills = []
    if latest_resume and latest_resume.candidate_profile:
        try:
            cand = CandidateProfile.model_validate(json.loads(latest_resume.candidate_profile))
            top_skills = cand.technical_skills[:8]
        except Exception:
            top_skills = ["Python", "FastAPI", "React", "PostgreSQL"]
    else:
        top_skills = ["Python", "TypeScript", "React", "PostgreSQL", "Docker", "Machine Learning"]

    # 3. Match Scores & Skill Gaps
    gap_stmt = select(SkillGap).where(SkillGap.user_id == current_user.id)
    gaps = (await db.execute(gap_stmt)).scalars().all()
    avg_match_score = round(sum(g.overall_match_score for g in gaps) / len(gaps), 1) if gaps else 78.5

    critical_gaps = []
    for g in gaps:
        if g.missing_skills:
            try:
                for ms in json.loads(g.missing_skills):
                    critical_gaps.append(ms.get("skill_name"))
            except Exception:
                pass
    critical_gaps = list(set(critical_gaps))[:6]

    # 4. Applications breakdown
    app_stmt = select(Application).where(Application.user_id == current_user.id)
    apps = (await db.execute(app_stmt)).scalars().all()
    app_stats = {
        "total": len(apps),
        "saved": sum(1 for a in apps if a.status == "Saved"),
        "applied": sum(1 for a in apps if a.status == "Applied"),
        "interview": sum(1 for a in apps if a.status == "Interview"),
        "offer": sum(1 for a in apps if a.status == "Offer"),
    }

    # 5. Learning Plans
    lp_stmt = select(LearningPlan).where(LearningPlan.user_id == current_user.id)
    plans = (await db.execute(lp_stmt)).scalars().all()
    avg_learning_progress = round(sum(p.completion_percentage for p in plans) / len(plans), 1) if plans else 0.0

    # 6. Interviews
    int_stmt = select(Interview).where(Interview.user_id == current_user.id)
    interviews = (await db.execute(int_stmt)).scalars().all()
    avg_interview_score = round(sum(i.overall_score for i in interviews if i.overall_score) / len([i for i in interviews if i.overall_score]), 1) if [i for i in interviews if i.overall_score] else 82.0

    # 7. Composite Career Score (Weighted combination of Resume, Match, Interview, Learning)
    career_score = round(
        resume_score * 0.30 +
        avg_match_score * 0.30 +
        avg_interview_score * 0.25 +
        (avg_learning_progress or 60.0) * 0.15,
        1
    )

    return {
        "career_score": career_score,
        "resume_score": resume_score,
        "job_match_score": avg_match_score,
        "interview_performance_score": avg_interview_score,
        "learning_progress": avg_learning_progress,
        "total_resumes": len(resumes),
        "total_jobs": len(gaps),
        "top_skills": top_skills,
        "skill_gaps": critical_gaps or ["LangGraph", "Kubernetes", "Vector Search"],
        "applications": app_stats,
        "recent_activity": [
            {"type": "resume_parsed", "title": "Resume Analyzed", "time": "Recently", "score": f"{resume_score}%"},
            {"type": "job_matched", "title": "Job Match Calculated", "time": "Recently", "score": f"{avg_match_score}%"},
            {"type": "interview", "title": "Mock Interview Evaluation", "time": "Recently", "score": f"{avg_interview_score}%"}
        ]
    }
