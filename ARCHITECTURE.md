# CareerPilot AI — Architectural Design & Reference

## 1. System Topology
CareerPilot AI is engineered as a decoupled, multi-agent AI architecture separating client rendering, asynchronous API gateways, agent orchestration state graphs, and hybrid database storage.

```
                    +-----------------------------+
                    |      Next.js 14 Client      |
                    | (React 18 + Tailwind + UI)  |
                    +--------------+--------------+
                                   | HTTPS / REST
                                   v
                    +-----------------------------+
                    |     FastAPI API Gateway     |
                    |   (JWT Auth + Middleware)   |
                    +--------------+--------------+
                                   |
            +----------------------+----------------------+
            |                      |                      |
            v                      v                      v
+-----------------------+ +-----------------------+ +-----------------------+
|  LangGraph Workflows  | |    RAG Vector Store   | |      MCP Server       |
| - Planner             | | - Hybrid Chunking     | | - get_candidate_prof  |
| - Resume Intelligence | | - pgvector Search     | | - calculate_match     |
| - Job Research        | | - Oracle 23ai Vector  | | - search_documents    |
| - Deterministic Match | | - Grounded QA Engine  | | - get_interview_hist  |
| - Resume Optimizer    | +-----------------------+ +-----------------------+
| - Cover Letter Agent  |
| - Adaptive Interview  |
| - Evaluator / Critic  |
+-----------------------+
            |
            v
+---------------------------------------------------------+
|                Database & Persistence                   |
|  PostgreSQL 16 + pgvector  <--->  Oracle AI DB 23ai     |
|  SQLAlchemy 2.0 Async ORM + Alembic Migration Pipeline  |
+---------------------------------------------------------+
```

---

## 2. Multi-Agent System Decomposition
1. **Planner Agent**: Interprets user goal and builds execution plan.
2. **Resume Intelligence Agent**: Extracts structured profile data without hallucinations.
3. **Job Research Agent**: Ingests job postings via raw text or SSRF-protected URL scraping.
4. **Skill Gap Engine**: Computes exact 6-dimension score using mathematical formulas.
5. **Resume Optimizer**: Suggests ATS keyword enhancements with bullet diffs.
6. **Cover Letter Agent**: Generates tailored letters grounded in verified facts.
7. **Adaptive Interview Agent**: Simulates technical/behavioral rounds with dynamic follow-ups.
8. **RAG Knowledge Agent**: Answers queries using user's uploaded career documents.
9. **Learning Plan Agent**: Designs step-by-step milestone roadmaps for skill gaps.
10. **Evaluator / Critic Agent**: Independent gatekeeper verifying factual consistency before presentation.

---

## 3. Deterministic Compatibility Scoring Formula

$$\text{Score} = 0.40 S_{\text{required}} + 0.20 S_{\text{experience}} + 0.15 S_{\text{preferred}} + 0.10 S_{\text{tech}} + 0.10 S_{\text{education}} + 0.05 S_{\text{relevance}}$$

All calculation logic executes in pure Python ([`DeterministicScoringEngine`](file:///c:/Users/Lalith%20Sagar/OneDrive/Desktop/careerpilot-ai/backend/app/tools/scoring_engine.py)). Generative AI is used exclusively for semantic normalization and synthesizing human-readable explanations.

---

## 4. Oracle AI 23ai Integration Path
The database layer supports dual dialects:
- **Default**: PostgreSQL 16 + `pgvector` (`Vector(768)` with HNSW index).
- **Enterprise**: Oracle AI Database 23ai (`VECTOR` column with `COSINE` distance and in-database vector search).
Both dialects interface seamlessly via the unified `VectorStoreProvider` abstraction.
