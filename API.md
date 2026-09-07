# CareerPilot AI — API & MCP Reference Specification

All endpoints are prefixed with `/api/v1`. Authenticated endpoints require `Authorization: Bearer <JWT_TOKEN>`.

---

## 1. Authentication Endpoints

### `POST /auth/register`
- **Body**: `{ "email": "string", "password": "string", "full_name": "string" }`
- **Response**: `201 Created` with JWT access token and User object.

### `POST /auth/login/json`
- **Body**: `{ "email": "string", "password": "string" }`
- **Response**: `200 OK` with JWT access token.

### `GET /auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Current user profile metadata.

---

## 2. Resume Management

### `POST /resumes/upload`
- **Form Data**: `file` (PDF/DOCX/TXT), `title` (string)
- **Response**: Parsed Candidate Profile and Resume Quality Assessment.

### `GET /resumes`
- **Response**: List of user's uploaded resumes and health scores.

### `GET /resumes/{resume_id}`
- **Response**: Full structured candidate profile.

---

## 3. Job Analysis & Deterministic Matching

### `POST /jobs`
- **Body**: `{ "title": "string", "company": "string", "raw_description": "string", "source_url": "optional" }`
- **Response**: Structured job requirements, required vs preferred skills.

### `POST /match/calculate`
- **Body**: `{ "resume_id": "string", "job_id": "string" }`
- **Response**: Deterministic 6-dimension match score, weights, matched/missing skill matrix, AI explanation.

---

## 4. Resume Optimization & Cover Letters

### `POST /optimize`
- **Body**: `{ "resume_id": "string", "job_id": "string", "custom_instructions": "string" }`
- **Response**: Bullet rewrites, projected ATS score, and anti-hallucination verification note.

### `POST /cover-letters`
- **Body**: `{ "resume_id": "string", "job_id": "string", "tone": "professional|executive|technical|energetic" }`
- **Response**: Tailored grounded cover letter with verified fact attributions.

---

## 5. Mock Interview Center

### `POST /interviews/start`
- **Body**: `{ "target_role": "string", "interview_type": "string", "total_questions": 4 }`
- **Response**: First generated interview question.

### `POST /interviews/answer`
- **Body**: `{ "question_id": "string", "user_answer_text": "string" }`
- **Response**: Real-time evaluation, scores, strengths, missed points, exemplar answer.

### `POST /interviews/{interview_id}/next-question`
- **Response**: Dynamic next question or follow-up.

### `GET /interviews/{interview_id}/report`
- **Response**: Comprehensive performance audit and category rubric.

---

## 6. Career Knowledge RAG

### `POST /knowledge/upload`
- **Form Data**: `file`, `title`, `category` (certificate|project|notes|portfolio)
- **Response**: Ingestion confirmation with chunk count.

### `POST /knowledge/search`
- **Body**: `{ "query": "string", "top_k": 4 }`
- **Response**: Top user-isolated vector chunks by cosine similarity.

### `POST /knowledge/qa`
- **Body**: `{ "query": "string", "top_k": 4 }`
- **Response**: Grounded synthesis citing user's uploaded documents.

---

## 7. Model Context Protocol (MCP) Tools

### `GET /mcp/tools`
- **Response**: List of available JSON-RPC 2.0 tools schemas (`get_candidate_profile`, `calculate_job_match`, `search_career_documents`, `get_interview_history`).

### `POST /mcp/execute`
- **Body**: `{ "tool": "calculate_job_match", "parameters": { "resume_id": "...", "job_id": "..." } }`
- **Response**: Structured tool execution result.
