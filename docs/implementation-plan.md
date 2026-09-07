# CareerPilot AI — Master Implementation & Execution Plan

This document outlines the phased roadmap for building, verifying, securing, and deploying CareerPilot AI.

---

## Roadmap & Phase Matrix

| Phase | Description | Key Deliverables | Verification Strategy |
|---|---|---|---|
| **Phase 1** | Architecture & Implementation Plan | `docs/architecture.md`, `docs/implementation-plan.md` | Formal architecture specification review |
| **Phase 2** | Project Skeleton & Base DevOps | Next.js 14 frontend, FastAPI backend, Dockerfiles, docker-compose, health check endpoints | Container builds, health check HTTP 200 |
| **Phase 3** | Database Architecture & Migrations | SQLAlchemy models, Alembic migrations, pgvector extension, seed data | DB unit tests, migration up/down execution |
| **Phase 4** | Authentication & Authorization | JWT token issuing, bcrypt/argon2 hashing, user-scoped RBAC, protected routes | Integration tests verifying cross-user isolation |
| **Phase 5** | Frontend Application & Design System | 18 SaaS UI views, Tailwind + shadcn/ui components, responsive dark/light layouts | Component rendering, UI routing tests |
| **Phase 6** | Resume Intelligence Agent | PyMuPDF / python-docx parser, Pydantic structured output, quality scoring | Resume parsing benchmark tests with real-world samples |
| **Phase 7** | Job Research Agent | Pasted text / URL parser, SSRF protection, job requirement extraction | Job ingestion tests, SSRF boundary attack tests |
| **Phase 8** | Skill Gap & Matching Engine | Deterministic 6-dimension weighted scorer, explanation generator | Comprehensive scoring math & edge case unit tests |
| **Phase 9** | Career Knowledge RAG | Hybrid chunker, embedding pipeline, pgvector similarity search, source attribution | RAG recall tests, user tenant isolation tests |
| **Phase 10** | Planner Agent & LangGraph | Multi-agent graph orchestrator, state transitions, cycle bounds, human checkpoints | Graph state transition unit tests |
| **Phase 11** | Resume Optimization Agent | Factual bullet re-writer, ATS keyword optimizer, diff view | Hallucination avoidance tests, ATS scoring tests |
| **Phase 12** | Cover Letter Agent | Grounded cover letter generator, tone customizer | Factual grounding checks against verified resume facts |
| **Phase 13** | Adaptive Interview Agent | Technical & behavioral question generator, real-time answer evaluator | Mock interview dialog simulation tests |
| **Phase 14** | Evaluator / Critic Agent | Independent quality gatekeeper, hallucination detector, revision loop | Guardrail & evaluation validation suite |
| **Phase 15** | Model Context Protocol (MCP) Server | JSON-RPC 2.0 tool server, user-scoped tool invocations | MCP client-server protocol integration tests |
| **Phase 16** | Learning Plan Agent | Priority gap roadmaps, milestones, project suggestions | Plan generation tests |
| **Phase 17** | Application Tracking | Kanban & Table application status management | CRUD & status transition tests |
| **Phase 18** | User-Scoped Agent Memory | User career trajectory & recurring weak skill tracker | Memory retrieval & isolation tests |
| **Phase 19** | Full Frontend-Backend Integration | API services, React Query hooks, live streaming, error handling | Full frontend-backend API integration tests |
| **Phase 20** | Security Hardening & Audit | Rate limiting, CORS, SSRF hardening, prompt injection defense, `SECURITY.md` | Security vulnerability test suite |
| **Phase 21** | Complete QA & End-to-End Testing | Unit, integration, E2E user flow tests, `docs/QA_REPORT.md` | Automated pytest suite + E2E browser runs |
| **Phase 22** | Docker, CI/CD & Deployment Readiness | Production multi-stage Dockerfiles, GitHub Actions workflow | `docker compose up --build` verification |
| **Phase 23** | Oracle AI Integration & Final Docs | Oracle AI Vector Search compatibility layer, comprehensive `README.md` | Dual-dialect schema verification & complete docs |

---

## Phase 1 Sign-Off Criteria
- [x] Complete System Architecture specification written in `docs/architecture.md`.
- [x] Comprehensive Execution Plan documented in `docs/implementation-plan.md`.
- [x] Implementation Plan artifact created in brain directory for tracking and user review.
