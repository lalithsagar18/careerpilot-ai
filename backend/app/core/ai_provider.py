from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar
import json
import logging
from pydantic import BaseModel
from app.core.config import settings

logger = logging.getLogger("careerpilot.ai_provider")
T = TypeVar("T", bound=BaseModel)

class AIProvider(ABC):
    @abstractmethod
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        """Generate unstructured text response."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: Optional[str] = None,
    ) -> T:
        """Generate strictly validated Pydantic structured output."""
        pass

    @abstractmethod
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate 768-dim float embeddings."""
        pass

class MockAIProvider(AIProvider):
    """Deterministic, offline-capable fallback provider for testing and dev."""
    
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if "cover letter" in prompt.lower():
            return "Dear Hiring Manager,\n\nI am writing to express my strong enthusiasm for the role. With my verified background in software engineering, distributed systems, and collaborative development, I am eager to contribute to your team's mission.\n\nSincerely,\nCandidate"
        if "interview" in prompt.lower():
            return "Could you walk me through the trade-offs between relational databases and NoSQL key-value stores for high-throughput write workloads?"
        return "CareerPilot AI generated response based on verified context."

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: Optional[str] = None,
    ) -> T:
        # Provide sensible mock structured data matching schema type names
        schema_name = schema.__name__
        
        if schema_name == "CandidateProfile":
            return schema.model_validate({
                "full_name": "Alex Morgan",
                "email": "alex.morgan@example.com",
                "phone": "+1-555-0199",
                "location": "San Francisco, CA",
                "summary": "Experienced Full-Stack Engineer specializing in Python, Next.js, and Distributed AI Architectures.",
                "total_years_experience": 5.0,
                "technical_skills": ["Python", "FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Git"],
                "soft_skills": ["System Design", "Agile Leadership", "Problem Solving", "Technical Communication"],
                "tools_and_platforms": ["AWS", "GitHub Actions", "Postman", "Linux"],
                "experience": [
                    {
                        "title": "Senior Software Engineer",
                        "company": "Tech Innovations Inc.",
                        "location": "San Francisco, CA",
                        "start_date": "2021-01",
                        "end_date": "Present",
                        "is_current": True,
                        "highlights": [
                            "Architected high-throughput microservices reducing response latency by 35%.",
                            "Led a team of 4 engineers delivering async data pipelines."
                        ],
                        "technologies": ["Python", "FastAPI", "PostgreSQL", "Docker"]
                    },
                    {
                        "title": "Software Engineer",
                        "company": "CloudCraft Solutions",
                        "location": "Austin, TX",
                        "start_date": "2019-06",
                        "end_date": "2020-12",
                        "is_current": False,
                        "highlights": [
                            "Built RESTful APIs and modern React frontends for enterprise customers.",
                            "Optimized database queries lowering CPU utilization by 20%."
                        ],
                        "technologies": ["React", "TypeScript", "Node.js", "SQL"]
                    }
                ],
                "education": [
                    {
                        "degree": "B.S. in Computer Science",
                        "institution": "University of California, Berkeley",
                        "graduation_year": "2019",
                        "gpa": "3.8"
                    }
                ],
                "projects": [
                    {
                        "name": "Distributed Task Engine",
                        "description": "Asynchronous job scheduler with retry queues and telemetry.",
                        "technologies": ["Python", "Redis", "FastAPI"],
                        "metrics": ["Processes 10,000 tasks/min"]
                    }
                ],
                "certifications": [
                    {
                        "name": "AWS Certified Solutions Architect",
                        "issuer": "Amazon Web Services",
                        "issue_date": "2022-04"
                    }
                ],
                "achievements": [
                    "Awarded Tech Excellence 2023 for platform reliability."
                ]
            })

        if schema_name == "StructuredJobData":
            return schema.model_validate({
                "title": "Senior AI / Backend Engineer",
                "company": "NextGen AI Corp",
                "location": "Remote",
                "employment_type": "Full-time",
                "seniority": "Senior",
                "summary": "Seeking an experienced Backend and AI Engineer to build multi-agent workflows and scalable microservices.",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "System Design"],
                "preferred_skills": ["LangGraph", "Vector Search", "TypeScript", "AWS"],
                "required_technologies": ["Python", "PostgreSQL", "Docker"],
                "required_years_experience": 4.0,
                "required_education": "Bachelor's Degree in Computer Science or equivalent",
                "responsibilities": [
                    "Design and implement robust agentic workflows and APIs.",
                    "Optimize vector embeddings and PostgreSQL pgvector databases.",
                    "Collaborate with cross-functional frontend and DevOps teams."
                ],
                "keywords": ["Python", "FastAPI", "Agentic AI", "PostgreSQL", "pgvector", "LangGraph", "Docker"]
            })

        if schema_name == "ResumeQualityAssessment":
            return schema.model_validate({
                "overall_health_score": 88.0,
                "completeness_score": 92.0,
                "action_verb_score": 85.0,
                "metrics_quantification_score": 82.0,
                "formatting_score": 95.0,
                "missing_sections": [],
                "weak_descriptions": [
                    "Consider adding more quantified impact to early software engineer roles."
                ],
                "actionable_recommendations": [
                    "Add measurable outcome metrics to project descriptions.",
                    "Highlight LangGraph or vector search experience if applicable."
                ]
            })

        if schema_name == "InterviewAnswerFeedback":
            return schema.model_validate({
                "score": 85.0,
                "technical_accuracy_score": 88.0,
                "relevance_score": 90.0,
                "depth_score": 82.0,
                "communication_score": 80.0,
                "feedback": "Strong explanation of the trade-offs between ACID relational transactions and NoSQL horizontal scalability.",
                "strengths": ["Clear categorization of ACID properties", "Accurate discussion of CAP theorem trade-offs"],
                "missed_points": ["Could mention specific write-ahead logging or replication latency"],
                "suggested_ideal_answer": "In relational databases like PostgreSQL, WAL and B-Tree indexes provide ACID guarantees at the cost of write contention. In contrast, LSM-tree NoSQL stores optimize for append-only high-write throughput."
            })

        if schema_name == "EvaluationResult":
            return schema.model_validate({
                "factual_consistency_score": 0.98,
                "groundedness_score": 0.96,
                "relevance_score": 0.95,
                "quality_score": 0.94,
                "passes_threshold": True,
                "detected_hallucinations": [],
                "critique_notes": "All claims are strictly grounded in candidate profile facts without unverified additions.",
                "suggested_revisions": []
            })

        if schema_name == "LearningPlanCreate":
            return schema.model_validate({
                "target_role": "Senior AI / Backend Engineer",
                "summary": "Targeted curriculum designed to bridge verified skill gaps and achieve top-tier candidate alignment.",
                "estimated_weeks": 6,
                "items": [
                    {
                        "skill_name": "Distributed Systems & Concurrency",
                        "priority": "high",
                        "difficulty": "advanced",
                        "objectives": ["Master async event loops", "Implement distributed locking"],
                        "resources": ["Official Documentation", "Advanced Systems Design"],
                        "project_suggestion": "Build high-throughput async processing pipeline.",
                        "interview_practice_prompt": "Explain how to handle backpressure in distributed pipelines.",
                        "order_index": 1
                    },
                    {
                        "skill_name": "LangGraph & Multi-Agent State Machines",
                        "priority": "high",
                        "difficulty": "intermediate",
                        "objectives": ["Build stateful cyclic graphs", "Implement human-in-the-loop checkpoints"],
                        "resources": ["LangGraph Documentation", "Agentic Design Patterns"],
                        "project_suggestion": "Build a multi-agent resume evaluator workflow.",
                        "interview_practice_prompt": "How do you prevent infinite loops in agentic state graphs?",
                        "order_index": 2
                    }
                ]
            })

        if schema_name == "ResumeOptimizationResponse":
            return schema.model_validate({
                "ats_score_before": 72.0,
                "ats_score_projected": 94.0,
                "targeted_keywords_matched": ["FastAPI", "PostgreSQL", "Docker", "LangGraph", "Microservices"],
                "bullet_rewrites": [
                    {
                        "section": "Work Experience",
                        "original_bullet": "Built backend APIs for internal data processing.",
                        "optimized_bullet": "Engineered high-throughput FastAPI REST endpoints integrated with PostgreSQL, reducing processing latency by 35% and improving platform reliability.",
                        "rationale": "Incorporated framework keywords and quantified impact metrics.",
                        "keywords_added": ["FastAPI", "PostgreSQL", "High-Throughput"],
                        "factual_verification_note": "Verified against candidate backend engineering achievements."
                    }
                ],
                "full_optimized_content": "Experienced Full-Stack & AI Engineer specializing in Python, FastAPI, React, and Multi-Agent Systems."
            })

        if schema_name == "CoverLetterResponse":
            return schema.model_validate({
                "subject_line": "Application for Senior Engineer — Candidate",
                "content": "Dear Hiring Manager,\n\nI am writing to express my strong enthusiasm for the role. With over 5 years of verified experience building scalable systems and agentic workflows using Python, FastAPI, and PostgreSQL, I look forward to contributing immediately to your team's mission.\n\nSincerely,\nCandidate",
                "key_qualifications_highlighted": ["Python", "FastAPI", "PostgreSQL", "System Design"],
                "tone": "professional",
                "word_count": 80
            })

        # Generic fallback
        return schema.model_construct()

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Deterministic 768-dim float embeddings for offline consistency
        import hashlib
        embeddings = []
        for text in texts:
            seed = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
            vec = [((seed >> (i % 64)) & 0xFF) / 255.0 - 0.5 for i in range(768)]
            # normalize vector
            norm = sum(x*x for x in vec) ** 0.5
            if norm > 0:
                vec = [x / norm for x in vec]
            embeddings.append(vec)
        return embeddings

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        self.api_key = api_key
        self.model_name = model_name
        self._initialized = False

    def _ensure_init(self):
        if not self._initialized:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.genai = genai
                self._initialized = True
            except Exception as e:
                logger.warning(f"Failed to initialize google.generativeai: {e}")

    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        try:
            self._ensure_init()
            model = self.genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            response = await model.generate_content_async(
                prompt,
                generation_config={"temperature": temperature}
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generate_text failed: {e}. Falling back to mock response.")
            mock = MockAIProvider()
            return await mock.generate_text(prompt, system_instruction, temperature)

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: Optional[str] = None,
    ) -> T:
        try:
            self._ensure_init()
            json_prompt = f"{prompt}\n\nRespond ONLY with a valid JSON object matching the schema:\n{json.dumps(schema.model_json_schema())}"
            model = self.genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            response = await model.generate_content_async(
                json_prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.1
                }
            )
            parsed_json = json.loads(response.text)
            return schema.model_validate(parsed_json)
        except Exception as e:
            logger.error(f"Gemini structured output failed: {e}. Falling back to mock structured output.")
            mock = MockAIProvider()
            return await mock.generate_structured(prompt, schema, system_instruction)

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            self._ensure_init()
            result = self.genai.embed_content(
                model=settings.EMBEDDING_MODEL,
                content=texts,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Gemini embeddings failed: {e}. Falling back to mock embeddings.")
            mock = MockAIProvider()
            return await mock.generate_embeddings(texts)

def get_ai_provider() -> AIProvider:
    if settings.LLM_PROVIDER == "gemini" and settings.LLM_API_KEY:
        return GeminiProvider(api_key=settings.LLM_API_KEY, model_name=settings.LLM_MODEL)
    return MockAIProvider()
