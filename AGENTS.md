# CareerPilot AI — Multi-Agent Architecture & Specification

## 1. Multi-Agent Overview
CareerPilot AI employs 10 specialized AI agents orchestrated via **LangGraph** with typed states, bounded cycles, deterministic calculation nodes, and Human-in-the-Loop checkpoints.

---

## 2. Agent Catalog & Responsibilities

| Agent | Responsibility | Primary Input | Output Schema |
|---|---|---|---|
| **Planner Agent** | Interprets user goals and orchestrates dynamic sub-workflows | User prompt / request | Sub-task execution graph |
| **Resume Intelligence Agent** | Parses raw document text into structured profile facts without hallucination | Raw PDF/DOCX text | `CandidateProfile`, `ResumeQualityAssessment` |
| **Job Research Agent** | Normalizes job postings and scrapes safe URLs with SSRF guards | Job description / URL | `StructuredJobData` |
| **Skill Gap Agent** | Deterministically correlates skills and calculates 6-dimension match score | Candidate profile + Job requirements | `ScoreBreakdown`, `MatchedSkill`, `MissingSkill` |
| **Resume Optimization Agent** | Reframes verified achievements and aligns ATS keywords with bullet diffs | Candidate profile + Target job | `ResumeOptimizationResponse`, `BulletRewrite` |
| **Cover Letter Agent** | Generates personalized, persuasive cover letters grounded in verified facts | Candidate profile + Target job | `CoverLetterResponse` |
| **Adaptive Interview Agent** | Simulates technical & behavioral interview dialogue with real-time feedback | Role, category, previous answers | `InterviewQuestion`, `InterviewAnswerFeedback`, `InterviewReport` |
| **RAG Knowledge Agent** | Retrieves user documents and synthesizes grounded answers with citations | Query + Vector chunks | `GroundedQAResponse` |
| **Learning Plan Agent** | Builds step-by-step milestone roadmaps, projects, and interview prompts | Skill gaps + Candidate level | `LearningPlanCreate`, `LearningPlanItemCreate` |
| **Evaluator / Critic Agent** | Independent truthfulness gatekeeper verifying zero fabrication | Generated artifact + Ground truth | `EvaluationResult` |

---

## 3. LangGraph Workflow Graph

```
                      +-------------------+
                      |   User Request    |
                      +---------+---------+
                                |
                                v
                      +-------------------+
                      |   Planner Node    |
                      +---------+---------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
+---------------+       +---------------+       +---------------+
| Resume Agent  |       |   Job Agent   |       |   RAG Agent   |
+-------+-------+       +-------+-------+       +-------+-------+
        |                       |                       |
        +-----------------------+-----------------------+
                                |
                                v
                      +-------------------+
                      |  Skill Gap Node   | <--- Deterministic 6-Dim Formula
                      +---------+---------+
                                |
        +-----------------------+-----------------------+
        |                                               |
        v                                               v
+-----------------------+                       +-----------------------+
|  Resume Optimizer     |                       |  Cover Letter Agent   |
+-----------+-----------+                       +-----------+-----------+
            |                                               |
            +-----------------------+-----------------------+
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
                        +-> (Back to Eval)     +-> [User: Approve / Edit / Reject]
                                               |
                                               v
                                     +--------------------+
                                     |    FINAL OUTPUT    |
                                     +--------------------+
```

---

## 4. Evaluator Feedback Loop & Safety Bounds
- **Maximum Revisions**: Hard-bounded to 2 cycles to prevent infinite recursion.
- **Factual Consistency Threshold**: Must score $\ge 0.90$ on groundedness without detected hallucinations before proceeding to human review.
- **Human Approval**: The user retains sovereign control over all finalized resume versions and submitted applications.
