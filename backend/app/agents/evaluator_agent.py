import logging
from typing import Dict, Any
from app.core.ai_provider import AIProvider, get_ai_provider
from app.schemas.evaluator import EvaluationResult

logger = logging.getLogger("careerpilot.agents.evaluator")

EVALUATOR_SYSTEM_PROMPT = """
You are the CareerPilot AI Independent Evaluator & Critic Agent.
Your responsibility is to act as a strict quality and truthfulness gatekeeper before presenting generated outputs to the user.

VERIFICATION PROTOCOL:
1. Check factual consistency against verified source candidate profile facts.
2. Check for unsupported claims, invented numbers, metrics, or technologies.
3. Check relevance to the target job description.
4. If hallucinations or unsupported claims exist, mark passes_threshold=False, list the detected hallucinations, and provide targeted revision instructions.
5. Max revision cycles are strictly bounded by application logic to prevent infinite loops.
"""

class EvaluatorCriticAgent:
    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    async def evaluate_artifact(
        self,
        artifact_type: str,
        generated_content: str,
        source_facts: Dict[str, Any],
        target_job_context: Dict[str, Any] = None
    ) -> EvaluationResult:
        prompt = f"""
ARTIFACT TYPE: {artifact_type}

GENERATED CONTENT TO AUDIT:
---
{generated_content}
---

VERIFIED SOURCE FACTS (GROUND TRUTH):
---
{source_facts}
---

TARGET JOB REQUIREMENTS:
---
{target_job_context or {}}
---

Evaluate factual consistency, groundedness, relevance, and overall quality:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=EvaluationResult,
            system_instruction=EVALUATOR_SYSTEM_PROMPT
        )
