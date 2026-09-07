import pytest
from app.tools.scoring_engine import DeterministicScoringEngine
from app.schemas.resume import CandidateProfile, ExperienceItem, EducationItem, ProjectItem
from app.schemas.job import StructuredJobData

def test_deterministic_scoring_exact_match():
    candidate = CandidateProfile(
        full_name="Jane Doe",
        summary="Senior Backend Engineer with Python and PostgreSQL expertise.",
        total_years_experience=5.0,
        technical_skills=["Python", "PostgreSQL", "FastAPI", "Docker", "Kubernetes"],
        soft_skills=["Leadership", "Communication"],
        tools_and_platforms=["AWS", "Git"],
        experience=[
            ExperienceItem(
                title="Senior Engineer",
                company="Tech Co",
                technologies=["Python", "FastAPI", "PostgreSQL"],
                highlights=["Designed microservices using Python and Docker."]
            )
        ],
        education=[
            EducationItem(
                degree="B.S. in Computer Science",
                institution="State University",
                graduation_year="2019"
            )
        ],
        projects=[
            ProjectItem(
                name="AI Cloud",
                description="Cloud service",
                technologies=["Python", "PostgreSQL"]
            )
        ]
    )

    job = StructuredJobData(
        title="Senior Python Engineer",
        company="Global Tech",
        required_skills=["Python", "PostgreSQL", "Docker"],
        preferred_skills=["Kubernetes", "AWS"],
        required_technologies=["Python", "PostgreSQL"],
        required_years_experience=4.0,
        required_education="Bachelor's in Computer Science",
        responsibilities=["Build high scale APIs"],
        keywords=["Python", "PostgreSQL", "Docker"]
    )

    breakdown, matched, missing, partial = DeterministicScoringEngine.calculate_match(candidate, job)

    assert breakdown.overall_score >= 95.0
    assert breakdown.required_skill_score == 100.0
    assert breakdown.preferred_skill_score == 100.0
    assert breakdown.experience_score == 100.0
    assert len(missing) == 0
    assert len(matched) == 5

def test_deterministic_scoring_missing_skills():
    candidate = CandidateProfile(
        full_name="Junior Dev",
        total_years_experience=1.0,
        technical_skills=["HTML", "CSS", "JavaScript"],
        experience=[],
        education=[]
    )

    job = StructuredJobData(
        title="Principal AI Engineer",
        company="AI Labs",
        required_skills=["Python", "PyTorch", "Distributed Systems", "PostgreSQL"],
        preferred_skills=["LangGraph", "Triton"],
        required_technologies=["Python", "PyTorch"],
        required_years_experience=8.0,
        required_education="Master's in AI"
    )

    breakdown, matched, missing, partial = DeterministicScoringEngine.calculate_match(candidate, job)

    assert breakdown.overall_score < 40.0
    assert len(missing) > 0
    assert any(m.skill_name == "PyTorch" for m in missing)
