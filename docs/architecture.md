# CareerPilot AI — System Architecture Specification

## 1. System Overview & Executive Summary
CareerPilot AI is an enterprise-grade, agentic career intelligence platform engineered as a hybrid deterministic and generative multi-agent system. The system combines modern web standards (Next.js 14 App Router, TypeScript, Tailwind CSS, shadcn/ui) with a robust asynchronous backend (Python FastAPI, SQLAlchemy 2.0 async, Pydantic v2, PostgreSQL + pgvector, LangGraph, Model Context Protocol).

The architecture strictly decouples deterministic calculation logic (e.g., scoring models, keyword matching, vector distance calculations, permission scopes) from generative AI tasks (e.g., profile structuring, contextual rewriting, semantic gap analysis, adaptive mock interview dialogue generation, explanation synthesis).

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT LAYER                                      |
|  Next.js 14 (App Router) + React 18 + Tailwind CSS + Lucide Icons + shadcn/ui    |
+-----------------------------------------+-----------------------------------------+
                                          | HTTPS / WSS / REST
                                          v
+-----------------------------------------------------------------------------------+
|                              API GATEWAY / BACKEND                                |
|  FastAPI + Pydantic v2 + JWT Auth + Rate Limiting + User Scoped Middleware       |
+-------------------+---------------------+--------------------+--------------------+
                    |                     |                    |
                    v                     v                    v
+-----------------------+ +-----------------------+ +-----------------------+
|  MULTI-AGENT SYSTEM   | |   KNOWLEDGE & RAG     | |     MCP SERVER        |
|  - Planner Agent      | |  - Document Ingestion | |  - Tool Definitions   |
|  - Resume Agent       | |  - Hybrid Chunking    | |  - JSON-RPC 2.0       |
|  - Job Research Agent | |  - Embeddings Router  | |  - User Scoped Tools  |
|  - Skill Gap Agent    | |  - Vector Store       | |  - Rate Limiting      |
|  - Resume Optimizer   | |  - Context Synthesis  | +-----------------------+
|  - Cover Letter Agent | +-----------------------+
|  - Interview Agent    |
|  - Learning Agent     |
|  - Evaluator/Critic   |
|  - LangGraph Engine   |
+-----------+-----------+
            |
            v
+-----------------------------------------------------------------------------------+
|                             DATA & PERSISTENCE LAYER                              |
|  PostgreSQL 16 + pgvector (Default) <---> Oracle AI Database 23ai (Enterprise)   |
|  SQLAlchemy 2.0 Async ORM + Alembic Migrations + Tenant/User Isolation Filters    |
+-----------------------------------------+-----------------------------------------+
```

---

## 2. Frontend Architecture
- **Framework**: Next.js 14+ with App Router and Server/Client Component optimization.
- **State Management**: Zustand / React Context for client state, TanStack React Query for server state caching & mutation sync.
- **UI & Styling**: Tailwind CSS, Radix UI primitives, shadcn/ui custom components, Lucide icons.
- **Security**: HttpOnly cookie / Bearer Token auth handling, strict sanitization of Markdown/HTML outputs (DOMPurify), zero client-side API key leakage.
- **Key Modules & Pages**:
  - `/` Landing Page & Value Proposition
  - `/auth/login` & `/auth/register`
  - `/dashboard` Comprehensive Career & Job Match Hub
  - `/resumes` Resume Management, Parsing & Quality Health Score
  - `/jobs` Job Description & URL Ingestion & Semantic Analysis
  - `/match` Explainable Compatibility Match & Gap Matrix
  - `/learning-plan` Milestone-based Skill Acquisition Roadmaps
  - `/optimize` Resume Optimization Studio with Bullet Rewriting & ATS Scorer
  - `/cover-letter` Grounded Cover Letter Generator with Diff View
  - `/interview` Adaptive Mock Interview Simulator with Live Scoring
  - `/knowledge` Career Document RAG Ingestion & Semantic QA
  - `/applications` Kanban & Table Job Application Pipeline Tracker
  - `/settings` Profile, Preferences & AI Configuration

---

## 3. Backend Architecture & Service Decomposition
- **Framework**: FastAPI (asyncio) structured in clean onion/hexagonal architecture:
  - `api/`: API Routers, dependencies, middlewares, schemas validation.
  - `core/`: Application settings (Pydantic Settings), security, structured logging, error handlers.
  - `agents/`: Independent agent implementations with Pydantic structured output models.
  - `workflows/`: LangGraph state machine definitions, cycles, human approval checkpoints.
  - `tools/`: Deterministic execution engines (scoring algorithms, regex parsers, scrapers).
  - `rag/`: Ingestion, chunking, embedding generation, vector search retriever.
  - `mcp/`: Model Context Protocol server exposing tool capabilities over standard schema.
  - `db/`: Engine configuration, async session management, base models.
  - `models/`: SQLAlchemy ORM entity definitions.
  - `schemas/`: Pydantic input/output validation models.
  - `services/`: Business logic coordinators and transactional orchestrators.

---

## 4. Multi-Agent System & LangGraph Workflows

### 4.1 Agent Roles & Responsibilities
1. **Planner Agent**: Parses user intent, constructs dynamic execution sub-plans, controls conditional branching.
2. **Resume Intelligence Agent**: Parses raw document text into structured profile entities without fabrication.
3. **Job Research Agent**: Normalizes pasted descriptions or scraped web data into structured job requirements with SSRF and injection guards.
4. **Skill Gap Agent**: Deterministically correlates resume skills vs job requirements and categorizes missing/partial skills.
5. **Resume Optimization Agent**: Suggests factual enhancements and ATS-targeted improvements preserving strict factual integrity.
6. **Cover Letter Agent**: Generates highly contextualized, grounded cover letters based on verified resume facts only.
7. **Interview Agent**: Generates adaptive technical, behavioral, and system design interview questions, evaluating answers dynamically.
8. **Learning Plan Agent**: Builds step-by-step roadmaps, projects, and milestones for identified skill gaps.
9. **RAG Knowledge Agent**: Retrieves and synthesizes answers strictly grounded in user-provided documents.
10. **Evaluator / Critic Agent**: Independent quality and safety gatekeeper verifying factual grounding, absence of hallucinations, and scoring consistency.

### 4.2 LangGraph State Machine Architecture

```
                 +------------------+
                 |  START REQUEST   |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 |  Planner Node    |
                 +--------+---------+
                          |
        +-----------------+-----------------+
        |                 |                 |
        v                 v                 v
+---------------+ +---------------+ +---------------+
| Resume Agent  | |   Job Agent   | |  RAG Agent    |
+-------+-------+ +-------+-------+ +-------+-------+
        |                 |                 |
        +-----------------+-----------------+
                          |
                          v
                 +------------------+
                 |  Skill Gap Node  | <---+ (Deterministic Scoring Engine)
                 +--------+---------+
                          |
        +-----------------+-----------------+
        |                                   |
        v                                   v
+-----------------------+           +-----------------------+
| Resume Optimizer Node |           |  Cover Letter Node    |
+-----------+-----------+           +-----------+-----------+
            |                                   |
            +-----------------+-----------------+
                              |
                              v
                    +-------------------+
                    |  Evaluator Agent  |
                    +---------+---------+
                              |
                     [Passes Criteria?]
                     /                \
               (No / Max 2)        (Yes)
                   /                    \
                  v                      v
        +-------------------+  +--------------------+
        |  Revision Node    |  | Human Approval Node|
        +---------+---------+  +---------+----------+
                  |                      |
                  +-> (Back to Eval)     +-> [User Decision: Approve/Edit/Reject]
                                         |
                                         v
                               +--------------------+
                               |    FINAL OUTPUT    |
                               +--------------------+
```

---

## 5. Deterministic Matching & Scoring Engine

The Compatibility Score is strictly computed using deterministic mathematical weighting and never hallucinated by LLM:

$$\text{Score} = w_{\text{req}} S_{\text{req}} + w_{\text{pref}} S_{\text{pref}} + w_{\text{exp}} S_{\text{exp}} + w_{\text{tech}} S_{\text{tech}} + w_{\text{edu}} S_{\text{edu}} + w_{\text{rel}} S_{\text{rel}}$$

Default Weights:
- Required Skills ($w_{\text{req}}$): **40%**
- Experience Alignment ($w_{\text{exp}}$): **20%**
- Preferred Skills ($w_{\text{pref}}$): **15%**
- Technology Alignment ($w_{\text{tech}}$): **10%**
- Education Alignment ($w_{\text{edu}}$): **10%**
- Other Relevance ($w_{\text{rel}}$): **5%**

The LLM is utilized exclusively for semantic normalization (e.g. mapping "Postgres" to "PostgreSQL") and generating human-readable explanations of the deterministic score breakdown.

---

## 6. Database Schema & Vector Search (PostgreSQL + Oracle AI)

### 6.1 Core Entities
- `users`: Authentication, credentials hash, profile metadata, timestamps.
- `resumes`: User resume master records, file metadata.
- `resume_versions`: Historical revisions, structured candidate profiles (JSONB), ATS scores.
- `jobs`: Parsed job postings, raw text, requirements (JSONB), source URL.
- `job_requirements`: Normalized skill/tech/education requirements with weights.
- `skills`: Master ontology of technical and soft skills.
- `user_skills` & `job_skills`: Associative join tables with proficiency and years of experience.
- `applications`: Job application tracking statuses (`SAVED`, `APPLIED`, `INTERVIEW`, `OFFER`, `REJECTED`).
- `skill_gaps`: Computed gap analyses per user-job pair.
- `learning_plans` & `learning_plan_items`: Actionable milestone and task items.
- `interviews`, `interview_questions`, `interview_answers`: Full transcripts, scores, and feedback.
- `documents` & `document_chunks`: RAG source metadata and chunk embeddings with `vector(1536/768)`.
- `agent_runs`: Audit logging of model invocations, latency, tokens, evaluation scores.
- `evaluations`: Quality, factual consistency, and groundedness review logs.
- `approvals`: Human-in-the-loop decision audits.

### 6.2 Vector Search Abstraction (PostgreSQL pgvector <-> Oracle 23ai)
An abstraction layer `VectorStoreProvider` enables seamless operation across:
1. **PostgreSQL**: `pgvector` HNSW cosine similarity index `vector_cosine_ops`.
2. **Oracle AI Vector Search 23ai**: `VECTOR` data type with `COSINE` distance and in-database vector search indexes.

---

## 7. Model Context Protocol (MCP) Server Architecture
The built-in MCP server adheres to JSON-RPC 2.0 specifications exposing secure, user-scoped tools:
- `get_candidate_profile(user_id)`
- `analyze_resume(resume_id)`
- `calculate_job_match(resume_id, job_id)`
- `get_skill_gaps(resume_id, job_id)`
- `create_learning_plan(skill_gap_id)`
- `search_career_documents(query, top_k)`
- `generate_interview_questions(job_id, category)`
- `get_interview_history(user_id)`

**Security Safeguards**:
- Strictly prevents arbitrary SQL or shell execution.
- Validates user permissions on every tool invocation.
- Rate-limited and logged via `AgentRun`.

---

## 8. Security Architecture & Threat Mitigation
- **Untrusted Input Sanitation**: PDF/DOCX content extracted via PyMuPDF/python-docx with size limits (10MB max), scanned for malicious macros/scripts, parsed as plain data.
- **SSRF Defense**: URL fetching rejects private IP ranges (RFC 1918, RFC 4193, loopback, link-local, AWS metadata 169.254.169.254), enforces domain allowlists, handles redirects securely.
- **Prompt Injection Defense**: Boundary token wrappers, strict system prompt isolation, treating retrieved chunks and user resumes as untrusted data inputs, output schema validation via Pydantic.
- **Data Isolation**: All database queries and vector similarity searches strictly filter by authenticated `user_id`. Cross-user data leakage is prevented at both the ORM and vector retriever levels.
- **Secret Zero**: All API keys, secrets, and database credentials loaded via environment variables; never exposed to the client bundle or logs.

---

## 9. Observability, Logging & Testing Strategy
- **Structured JSON Logging**: Request IDs, User IDs (anonymized), Agent names, Latencies, Token counts.
- **Test Strategy**:
  - **Unit Tests**: Deterministic scoring algorithms, Pydantic validations, chunkers, regex parsers.
  - **Integration Tests**: FastAPI endpoint auth, CRUD operations, pgvector queries, MCP tool calling.
  - **E2E Workflows**: Full lifecycle simulation from registration to resume parsing, job match, interview, RAG search, and human approval.
