# Contributing to CareerPilot AI

Thank you for contributing to CareerPilot AI! We welcome code contributions, issue reports, and enhancements.

## 1. Development Principles
- **No Hallucinations**: Never allow LLMs to fabricate candidate skills, work experience, metrics, or credentials.
- **Deterministic Match Scoring**: All numeric compatibility formulas must reside in pure application code ([`DeterministicScoringEngine`](file:///c:/Users/Lalith%20Sagar/OneDrive/Desktop/careerpilot-ai/backend/app/tools/scoring_engine.py)).
- **User Scoping & Isolation**: Every database query, vector search, and MCP tool execution must be authenticated and isolated by `user_id`.
- **Typed Models**: Use strict Pydantic v2 schemas and SQLAlchemy 2.0 async mapped columns.

## 2. Local Setup

### Backend
```bash
python -m venv backend/venv
.\backend\venv\Scripts\activate
pip install -r backend/requirements.txt
pytest
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker compose up --build
```

## 3. Pull Request Guidelines
1. Run all tests locally before opening a PR: `pytest` and `npm run build`.
2. Ensure no secrets, tokens, or private credentials are included.
3. Keep changes cohesive and accompanied by unit/integration tests.
