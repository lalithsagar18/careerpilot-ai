# CareerPilot AI — Multi-Agent Career Intelligence & Job Application Platform

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)]()
[![Next.js](https://img.shields.io/badge/frontend-Next.js%2014-black.svg)]()
[![LangGraph](https://img.shields.io/badge/agents-LangGraph-orange.svg)]()
[![MCP](https://img.shields.io/badge/protocol-MCP-blue.svg)]()
[![pgvector](https://img.shields.io/badge/vector-pgvector-336791.svg)]()
[![Oracle Ready](https://img.shields.io/badge/database-Oracle%20AI%2023ai-red.svg)]()

> An enterprise-grade, agentic AI career platform combining **deterministic mathematical matching**, LangGraph multi-agent orchestration, user-partitioned RAG, adaptive mock interviews, and zero-hallucination resume optimization.

---

## 1. Problem Statement & Mission
Modern job seekers face fragmented tools, hallucinated AI advice, and generic resume generators that fabricate skills or metrics. **CareerPilot AI** solves this by enforcing:
1. **Mathematical Scoring Integrity**: Compatibility scores are computed using an explainable 6-dimension weighted algorithm, not generated randomly by an LLM.
2. **Strict Anti-Fabrication Constraints**: The platform never hallucinates skills, companies, degrees, or metrics.
3. **Multi-Agent Orchestration**: 10 specialized agents coordinated via **LangGraph** with Human-in-the-Loop checkpoints and bounded revision cycles.
4. **Data Isolation & Security**: User-partitioned vector embeddings, SSRF protection on job URLs, and strict Model Context Protocol (MCP) tool sandboxing.
5. **Oracle AI Readiness**: Native support for PostgreSQL `pgvector` and Oracle AI Database 23ai Vector Search.

---

## 2. System Architecture

```
                                 CLIENT LAYER
                  Next.js 14 App Router + React 18 + Tailwind CSS
                                      |
                                      v HTTPS / REST
                              FASTAPI BACKEND
                     JWT Auth + User-Scoped Middleware
                                      |
       +------------------------------+------------------------------+
       |                              |                              |
       v                              v                              v
MULTI-AGENT GRAPH (LangGraph)  CAREER KNOWLEDGE RAG            MCP SERVER
- Planner Agent                - PyMuPDF Chunking              - get_candidate_profile
- Resume Intelligence Agent    - Embeddings Pipeline           - calculate_job_match
- Job Research Agent           - pgvector / Oracle 23ai        - search_career_documents
- Skill Gap Engine             - Grounded Citation QA          - get_interview_history
- Resume Optimizer             +-------------------------------+-----------------------+
- Cover Letter Agent
- Adaptive Interview Agent
- Learning Plan Agent
- Evaluator / Critic Agent
       |
       v
PERSISTENCE LAYER (PostgreSQL 16 + pgvector <--> Oracle AI Database 23ai)
```

---

## 3. Agent Catalog & Responsibilities

| Agent | Core Responsibility | Input | Output Schema |
|---|---|---|---|
| **Planner Agent** | Orchestrates dynamic workflows and branches | User prompt | Execution state graph |
| **Resume Intelligence Agent** | Parses PDF/DOCX into structured candidate facts | Raw document text | `CandidateProfile`, `ResumeQualityAssessment` |
| **Job Research Agent** | Normalizes job requirements with SSRF guards | Job description / URL | `StructuredJobData` |
| **Skill Gap Agent** | Calculates 6-dimension match score and gaps | Candidate profile + Job | `ScoreBreakdown`, `MatchedSkill`, `MissingSkill` |
| **Resume Optimization Agent** | Reframes verified achievements for ATS alignment | Candidate profile + Job | `ResumeOptimizationResponse`, `BulletRewrite` |
| **Cover Letter Agent** | Generates grounded, job-specific cover letters | Candidate profile + Job | `CoverLetterResponse` |
| **Adaptive Interview Agent** | Dynamic mock interview dialogue & rubric scoring | Role, question, answer | `InterviewQuestion`, `InterviewAnswerFeedback`, `InterviewReport` |
| **RAG Knowledge Agent** | Retrieves user documents and synthesizes answers | User query + Chunks | `GroundedQAResponse` |
| **Learning Plan Agent** | Generates milestone roadmaps & projects | Skill gaps + Role | `LearningPlanCreate`, `LearningPlanItemCreate` |
| **Evaluator / Critic Agent** | Anti-hallucination verification gatekeeper | Generated content + Facts | `EvaluationResult` |

---

## 4. Deterministic Job Match Scoring Algorithm

The job compatibility score is strictly computed in pure Python ([`DeterministicScoringEngine`](file:///c:/Users/Lalith%20Sagar/OneDrive/Desktop/careerpilot-ai/backend/app/tools/scoring_engine.py)):

$$\text{Overall Score} = 0.40 S_{\text{required}} + 0.20 S_{\text{experience}} + 0.15 S_{\text{preferred}} + 0.10 S_{\text{tech}} + 0.10 S_{\text{education}} + 0.05 S_{\text{relevance}}$$

- **Required Skills Coverage (40%)**: Exact match on mandatory job qualifications.
- **Experience Alignment (20%)**: Candidate years vs. required years.
- **Preferred Skills Coverage (15%)**: Bonus match on nice-to-have tools.
- **Technology Alignment (10%)**: Tech stack overlap.
- **Education Alignment (10%)**: Degree level and major alignment.
- **Other Relevance (5%)**: Domain and project overlap baseline.

The LLM is used exclusively for semantic normalization and synthesizing explainable summaries.

---

## 5. Technology Stack

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (Async), Alembic, PyMuPDF, python-docx.
- **AI & Orchestration**: LangGraph, LangChain, Google Gemini API (`gemini-1.5-pro`, `text-embedding-004`), Provider Abstraction Layer (`AIProvider`).
- **Database**: PostgreSQL 16 + `pgvector` (Default) and Oracle AI Database 23ai Vector Search (Enterprise Ready).
- **Tool Protocol**: Model Context Protocol (MCP) JSON-RPC 2.0.
- **DevOps**: Docker, Multi-Stage Dockerfiles, Docker Compose.

---

## 6. Quickstart & Installation

### Option A: Running with Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-org/careerpilot-ai.git
cd careerpilot-ai

# Copy environment variables
cp .env.example .env

# Build and start all services
docker compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/api/v1/docs`

---

### Option B: Local Development

#### 1. Backend Setup
```bash
# Create and activate virtual environment
python -m venv backend/venv
.\backend\venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt

# Run test suite
pytest

# Start backend dev server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 7. Model Context Protocol (MCP) Tools

CareerPilot AI embeds an MCP server providing typed, sandboxed tools:
- `get_candidate_profile(resume_id)`: Retrieves structured profile facts.
- `calculate_job_match(resume_id, job_id)`: Executes deterministic 6-dimension scoring.
- `search_career_documents(query, top_k)`: Executes user-isolated vector similarity search.
- `get_interview_history(limit)`: Retrieves mock interview performance history.

---

## 8. Oracle AI Database 23ai Integration

The system includes an enterprise vector abstraction (`VectorStoreProvider`):
- **PostgreSQL**: Stores chunks with `vector(768)` and HNSW cosine distance indexing.
- **Oracle 23ai**: Stores chunks with native `VECTOR` datatype and `VECTOR_DISTANCE(embedding, query_vec, COSINE)` in-database search.
- Toggle between backends by configuring `ORACLE_ENABLED=true` in `.env`.

---

## 9. Quality Assurance & Verification
- **Unit & Integration Tests**: 100% Passed (`pytest backend/tests`)
- **Frontend Production Build**: 17/17 Pages Built Successfully (`next build`)
- **Full QA Report**: See [`docs/QA_REPORT.md`](file:///c:/Users/Lalith%20Sagar/OneDrive/Desktop/careerpilot-ai/docs/QA_REPORT.md)
- **Acceptance Report**: See [`docs/FINAL_ACCEPTANCE_REPORT.md`](file:///c:/Users/Lalith%20Sagar/OneDrive/Desktop/careerpilot-ai/docs/FINAL_ACCEPTANCE_REPORT.md)

---

## 10. License
This project is licensed under the MIT License.
