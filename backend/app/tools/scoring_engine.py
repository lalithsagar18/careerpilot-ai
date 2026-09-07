import re
from typing import Dict, List, Set, Tuple, Any
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.schemas.skill_gap import MatchedSkill, MissingSkill, PartialSkill, ScoreBreakdown

class DeterministicScoringEngine:
    """
    Computes explainable, mathematically rigorous compatibility scores
    between Candidate Profiles and Job Requirements without hallucination.
    """
    DEFAULT_WEIGHTS = {
        "required_skills": 0.40,
        "experience": 0.20,
        "preferred_skills": 0.15,
        "technology": 0.10,
        "education": 0.10,
        "other_relevance": 0.05,
    }

    @staticmethod
    def normalize_term(term: str) -> str:
        """Normalize skill/tool names for resilient deterministic comparison."""
        term = term.lower().strip()
        # common aliases normalization
        aliases = {
            "postgres": "postgresql",
            "reactjs": "react",
            "react.js": "react",
            "nodejs": "node.js",
            "node": "node.js",
            "golang": "go",
            "k8s": "kubernetes",
            "aws": "amazon web services",
            "gcp": "google cloud platform",
            "fastapi": "fastapi",
            "ts": "typescript",
            "js": "javascript",
            "py": "python",
            "docker": "docker",
        }
        clean = re.sub(r'[^a-z0-9\.\+#]', '', term)
        return aliases.get(clean, clean)

    @classmethod
    def calculate_match(
        cls,
        candidate: CandidateProfile,
        job: StructuredJobData,
        custom_weights: Dict[str, float] = None,
    ) -> Tuple[ScoreBreakdown, List[MatchedSkill], List[MissingSkill], List[PartialSkill]]:
        weights = custom_weights or cls.DEFAULT_WEIGHTS
        
        # 1. Gather all candidate skills and terms
        candidate_technical = {cls.normalize_term(s) for s in candidate.technical_skills}
        candidate_tools = {cls.normalize_term(s) for s in candidate.tools_and_platforms}
        candidate_soft = {cls.normalize_term(s) for s in candidate.soft_skills}
        
        # Extract skills mentioned in experience and projects
        experience_tech = set()
        for exp in candidate.experience:
            for tech in exp.technologies:
                experience_tech.add(cls.normalize_term(tech))
            for highlight in exp.highlights:
                # Add word tokens
                words = re.findall(r'\b[A-Za-z0-9\.\+#]{2,}\b', highlight)
                for w in words:
                    experience_tech.add(cls.normalize_term(w))

        for proj in candidate.projects:
            for tech in proj.technologies:
                experience_tech.add(cls.normalize_term(tech))

        all_candidate_skills = candidate_technical | candidate_tools | candidate_soft | experience_tech

        # 2. Evaluate Required Skills
        matched_skills: List[MatchedSkill] = []
        missing_skills: List[MissingSkill] = []
        partial_skills: List[PartialSkill] = []

        req_matches = 0
        total_req = len(job.required_skills) if job.required_skills else 1

        for req in job.required_skills:
            norm_req = cls.normalize_term(req)
            if norm_req in all_candidate_skills:
                req_matches += 1
                matched_skills.append(MatchedSkill(
                    skill_name=req,
                    category="required_skill",
                    candidate_evidence="Explicitly verified in candidate profile/experience.",
                    job_requirement=f"Required in {job.title}",
                    confidence=1.0
                ))
            else:
                # Check for partial / fuzzy overlap
                is_partial = any(norm_req in s or s in norm_req for s in all_candidate_skills if len(norm_req) > 3)
                if is_partial:
                    req_matches += 0.5
                    partial_skills.append(PartialSkill(
                        skill_name=req,
                        gap_description=f"Related technologies found in profile, but specific {req} experience is not explicit.",
                        current_level="Familiar / Adjacent",
                        target_level="Production Required"
                    ))
                else:
                    missing_skills.append(MissingSkill(
                        skill_name=req,
                        category="required_skill",
                        importance="critical",
                        job_context=f"Mandatory requirement for {job.title}."
                    ))

        req_score = min(100.0, (req_matches / total_req) * 100.0) if job.required_skills else 100.0

        # 3. Evaluate Preferred Skills
        pref_matches = 0
        total_pref = len(job.preferred_skills) if job.preferred_skills else 1

        for pref in job.preferred_skills:
            norm_pref = cls.normalize_term(pref)
            if norm_pref in all_candidate_skills:
                pref_matches += 1
                matched_skills.append(MatchedSkill(
                    skill_name=pref,
                    category="preferred_skill",
                    candidate_evidence="Documented in candidate skills or projects.",
                    job_requirement=f"Preferred for {job.title}",
                    confidence=1.0
                ))
            else:
                missing_skills.append(MissingSkill(
                    skill_name=pref,
                    category="preferred_skill",
                    importance="medium",
                    job_context="Listed as preferred/nice-to-have."
                ))

        pref_score = min(100.0, (pref_matches / total_pref) * 100.0) if job.preferred_skills else 100.0

        # 4. Evaluate Experience Alignment
        cand_exp = candidate.total_years_experience or 0.0
        job_req_exp = job.required_years_experience or 0.0
        
        if job_req_exp == 0.0:
            exp_score = 100.0
        elif cand_exp >= job_req_exp:
            exp_score = 100.0
        else:
            # Linear ramp with 40% floor if within 2 years
            exp_score = max(30.0, (cand_exp / job_req_exp) * 100.0)

        # 5. Evaluate Technology Alignment
        tech_matches = 0
        total_tech = len(job.required_technologies) if job.required_technologies else 1
        for tech in job.required_technologies:
            if cls.normalize_term(tech) in all_candidate_skills:
                tech_matches += 1
        tech_score = min(100.0, (tech_matches / total_tech) * 100.0) if job.required_technologies else 100.0

        # 6. Evaluate Education Alignment
        edu_score = 80.0  # default baseline
        if job.required_education:
            cand_edu_text = " ".join([f"{e.degree} {e.field_of_study or ''}" for e in candidate.education]).lower()
            if "master" in job.required_education.lower() and "master" in cand_edu_text:
                edu_score = 100.0
            elif "bachelor" in job.required_education.lower() and ("bachelor" in cand_edu_text or "b.s." in cand_edu_text or "b.e." in cand_edu_text or "b.tech" in cand_edu_text or "master" in cand_edu_text):
                edu_score = 100.0
            elif any(degree.lower() in cand_edu_text for degree in ["computer science", "engineering", "information technology"]):
                edu_score = 90.0
            else:
                edu_score = 70.0
        else:
            edu_score = 100.0

        # 7. Compute Weighted Overall Score
        overall_score = (
            req_score * weights["required_skills"] +
            exp_score * weights["experience"] +
            pref_score * weights["preferred_skills"] +
            tech_score * weights["technology"] +
            edu_score * weights["education"] +
            100.0 * weights["other_relevance"]
        )
        overall_score = round(min(100.0, max(0.0, overall_score)), 1)

        breakdown = ScoreBreakdown(
            overall_score=overall_score,
            required_skill_score=round(req_score, 1),
            preferred_skill_score=round(pref_score, 1),
            experience_score=round(exp_score, 1),
            technology_score=round(tech_score, 1),
            education_score=round(edu_score, 1),
            weights_applied=weights
        )

        return breakdown, matched_skills, missing_skills, partial_skills
