from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, END
import json

from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.schemas.skill_gap import ScoreBreakdown, MatchedSkill, MissingSkill, PartialSkill
from app.schemas.optimizer import ResumeOptimizationResponse
from app.schemas.cover_letter import CoverLetterResponse
from app.schemas.evaluator import EvaluationResult

from app.tools.scoring_engine import DeterministicScoringEngine
from app.agents.optimizer_agent import ResumeOptimizationAgent
from app.agents.cover_letter_agent import CoverLetterAgent
from app.agents.evaluator_agent import EvaluatorCriticAgent

class CareerWorkflowState(TypedDict):
    user_id: str
    resume_raw_text: str
    job_raw_text: str
    candidate_profile: Optional[Dict[str, Any]]
    job_data: Optional[Dict[str, Any]]
    score_breakdown: Optional[Dict[str, Any]]
    matched_skills: Optional[List[Dict[str, Any]]]
    missing_skills: Optional[List[Dict[str, Any]]]
    partial_skills: Optional[List[Dict[str, Any]]]
    optimized_resume: Optional[Dict[str, Any]]
    cover_letter: Optional[Dict[str, Any]]
    evaluation_result: Optional[Dict[str, Any]]
    revision_count: int
    human_approved: bool
    status: str

# Node implementations
async def skill_gap_node(state: CareerWorkflowState) -> Dict[str, Any]:
    cand = CandidateProfile.model_validate(state["candidate_profile"])
    job = StructuredJobData.model_validate(state["job_data"])
    breakdown, matched, missing, partial = DeterministicScoringEngine.calculate_match(cand, job)
    return {
        "score_breakdown": breakdown.model_dump(),
        "matched_skills": [m.model_dump() for m in matched],
        "missing_skills": [m.model_dump() for m in missing],
        "partial_skills": [p.model_dump() for p in partial],
        "status": "skill_gap_analyzed"
    }

async def generator_node(state: CareerWorkflowState) -> Dict[str, Any]:
    cand = CandidateProfile.model_validate(state["candidate_profile"])
    job = StructuredJobData.model_validate(state["job_data"])
    
    optimizer = ResumeOptimizationAgent()
    opt_res = await optimizer.optimize_resume(candidate=cand, job=job)

    cl_agent = CoverLetterAgent()
    cl_res = await cl_agent.generate_cover_letter(candidate=cand, job=job)

    return {
        "optimized_resume": opt_res.model_dump(),
        "cover_letter": cl_res.model_dump(),
        "status": "generated"
    }

async def evaluator_node(state: CareerWorkflowState) -> Dict[str, Any]:
    evaluator = EvaluatorCriticAgent()
    opt = state["optimized_resume"]
    cand = state["candidate_profile"]
    job = state["job_data"]

    eval_result = await evaluator.evaluate_artifact(
        artifact_type="resume_and_cover_letter",
        generated_content=json.dumps(opt),
        source_facts=cand,
        target_job_context=job
    )

    return {
        "evaluation_result": eval_result.model_dump(),
        "status": "evaluated"
    }

def should_revise_or_proceed(state: CareerWorkflowState) -> str:
    eval_data = state.get("evaluation_result", {})
    passes = eval_data.get("passes_threshold", True)
    revision_count = state.get("revision_count", 0)

    if not passes and revision_count < 2:
        return "revision_node"
    return "human_checkpoint_node"

async def revision_node(state: CareerWorkflowState) -> Dict[str, Any]:
    # Increment revision count and adjust generation with evaluator feedback
    rev_count = state.get("revision_count", 0) + 1
    return {
        "revision_count": rev_count,
        "status": f"revised_cycle_{rev_count}"
    }

async def human_checkpoint_node(state: CareerWorkflowState) -> Dict[str, Any]:
    # Human-in-the-loop approval checkpoint
    return {
        "status": "awaiting_human_approval"
    }

def build_career_graph():
    builder = StateGraph(CareerWorkflowState)
    builder.add_node("skill_gap_node", skill_gap_node)
    builder.add_node("generator_node", generator_node)
    builder.add_node("evaluator_node", evaluator_node)
    builder.add_node("revision_node", revision_node)
    builder.add_node("human_checkpoint_node", human_checkpoint_node)

    builder.set_entry_point("skill_gap_node")
    builder.add_edge("skill_gap_node", "generator_node")
    builder.add_edge("generator_node", "evaluator_node")
    
    builder.add_conditional_edges(
        "evaluator_node",
        should_revise_or_proceed,
        {
            "revision_node": "revision_node",
            "human_checkpoint_node": "human_checkpoint_node"
        }
    )
    builder.add_edge("revision_node", "generator_node")
    builder.add_edge("human_checkpoint_node", END)

    return builder.compile()

career_workflow_app = build_career_graph()
