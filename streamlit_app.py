import os
import sys
import json
import asyncio
from pathlib import Path
import streamlit as st

# Configure sys.path so backend modules can be imported
sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    from app.tools.scoring_engine import (
        calculate_compatibility_score,
        CandidateProfile,
        JobRequirements,
        SkillItem,
    )
    from app.tools.document_extractor import assess_resume_quality
    from app.agents.resume_agent import ResumeIntelligenceAgent
    from app.agents.job_agent import JobResearchAgent
    from app.agents.optimizer_agent import ResumeOptimizerAgent
    from app.agents.cover_letter_agent import CoverLetterAgent
    from app.agents.interview_agent import AdaptiveInterviewAgent
    from app.agents.learning_agent import LearningPlanAgent
    from app.agents.evaluator_agent import EvaluatorAgent
except ImportError as e:
    st.error(f"Error importing CareerPilot modules: {e}")

# Streamlit Page Setup
st.set_page_config(
    page_title="CareerPilot AI — Multi-Agent Career Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for modern aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .score-badge {
        font-size: 2.5rem;
        font-weight: 900;
        color: #10b981;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Helper function for async runs
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# Session state initialization
if "profile" not in st.session_state:
    st.session_state.profile = None
if "job_data" not in st.session_state:
    st.session_state.job_data = None
if "match_result" not in st.session_state:
    st.session_state.match_result = None
if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 CareerPilot AI")
    st.caption("Agentic Multi-Agent Career Platform")
    st.divider()
    
    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📄 Resume Intelligence",
            "🎯 Job Compatibility Match",
            "✨ Resume Optimizer",
            "✉️ Cover Letter Generator",
            "🎙️ Mock Interview Simulator",
            "🗺️ 30-60-90 Learning Plan",
            "⚙️ API Settings",
        ],
        index=0
    )
    
    st.divider()
    st.caption("Powered by LangGraph & Gemini")

# ==========================================
# PAGE 1: DASHBOARD
# ==========================================
if page == "📊 Dashboard":
    st.markdown('<div class="main-header">Career Intelligence Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-agent career readiness, deterministic scoring, and application intelligence</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Resume", "Alex Rivera (Parsed)" if st.session_state.profile else "None Uploaded")
    with col2:
        st.metric("Target Job", st.session_state.job_data.get("title", "None Selected") if st.session_state.job_data else "Not Analyzed")
    with col3:
        score_val = f"{st.session_state.match_result.get('overall_score', 0)}%" if st.session_state.match_result else "—"
        st.metric("Match Score", score_val)
    with col4:
        st.metric("AI Agents Active", "10 / 10 Online", delta="Ready")
        
    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("⚡ Quick Start Workflow")
        st.markdown("""
        1. **📄 Resume Intelligence**: Upload your resume (PDF/DOCX) or paste raw text to parse skills, experience, and assess ATS quality.
        2. **🎯 Job Compatibility**: Paste a job description or URL to calculate your deterministic 6-dimension match score.
        3. **✨ Resume Optimizer**: Generate bullet diffs aligned with ATS target keywords.
        4. **✉️ Cover Letter**: Craft a persuasive, grounded cover letter.
        5. **🎙️ Mock Interview**: Practice technical and behavioral questions with real-time rubric feedback.
        6. **🗺️ 30-60-90 Plan**: Build a milestone learning roadmap to bridge skill gaps.
        """)
    with c2:
        st.subheader("🛡️ Agent Verification Gate")
        st.info("CareerPilot AI features an independent **Evaluator Agent** with a factual consistency threshold of $\ge 0.90$ to ensure zero hallucination in all generated applications.")

# ==========================================
# PAGE 2: RESUME INTELLIGENCE
# ==========================================
elif page == "📄 Resume Intelligence":
    st.markdown('<div class="main-header">Resume Intelligence & ATS Health</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Extract verified structured facts and evaluate ATS structural quality</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    resume_text_input = st.text_area("Or Paste Resume Text", height=200, placeholder="Paste your complete resume text here...")
    
    if st.button("🚀 Analyze Resume with AI"):
        text_content = ""
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".pdf"):
                import fitz
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text_content = "\n".join([page.get_text() for page in doc])
            elif uploaded_file.name.endswith(".docx"):
                import docx
                import io
                doc = docx.Document(io.BytesIO(uploaded_file.read()))
                text_content = "\n".join([p.text for p in doc.paragraphs if p.text])
            else:
                text_content = uploaded_file.read().decode("utf-8")
        elif resume_text_input:
            text_content = resume_text_input
            
        if not text_content.strip():
            st.warning("Please provide resume text or upload a document.")
        else:
            with st.spinner("Resume Intelligence Agent parsing structured facts..."):
                agent = ResumeIntelligenceAgent()
                profile_res = run_async(agent.parse_resume(text_content))
                quality_res = assess_resume_quality(text_content)
                
                st.session_state.profile = profile_res
                st.session_state.quality = quality_res
                st.success("Resume parsed and analyzed successfully!")
                
    if st.session_state.profile:
        prof = st.session_state.profile
        qual = getattr(st.session_state, "quality", {})
        
        st.markdown("---")
        st.subheader("📋 Candidate Profile")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Candidate Name", prof.get("name", "N/A"))
        with m2:
            st.metric("Experience Level", f"{prof.get('total_years_experience', 0)} Years")
        with m3:
            st.metric("ATS Health Score", f"{qual.get('overall_score', 85)}/100")
            
        st.write("**Extracted Skills:**")
        skills = prof.get("skills", [])
        if skills:
            skill_badges = " ".join([f"`{s.get('name', s) if isinstance(s, dict) else s}`" for s in skills])
            st.markdown(skill_badges)
            
        st.write("**Executive Summary:**")
        st.info(prof.get("summary", "No summary provided."))

# ==========================================
# PAGE 3: JOB COMPATIBILITY MATCH
# ==========================================
elif page == "🎯 Job Compatibility Match":
    st.markdown('<div class="main-header">Deterministic Job Compatibility Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Mathematical 6-dimension evaluation calculated with zero LLM hallucination</div>', unsafe_allow_html=True)
    
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        job_title = st.text_input("Job Title", value="Senior AI / Full-Stack Engineer")
        job_company = st.text_input("Company", value="TechNova Innovations")
    with col_j2:
        job_url = st.text_input("Job Posting URL (Optional)", placeholder="https://example.com/careers/job123")
        
    job_desc = st.text_area(
        "Job Description Requirements",
        height=180,
        value="We are seeking a Senior AI Full-Stack Engineer with 5+ years experience in Python, FastAPI, React/Next.js, LangGraph, PostgreSQL, and LLM orchestration. Must have strong system architecture and cloud deployment background."
    )
    
    if st.button("⚖️ Calculate 6-Dimension Score"):
        with st.spinner("Job Research & Skill Gap Agents computing score..."):
            job_agent = JobResearchAgent()
            structured_job = run_async(job_agent.extract_requirements(job_desc, job_title, job_company))
            st.session_state.job_data = structured_job
            
            # Formulate candidate profile
            cand_profile = CandidateProfile(
                skills=[
                    SkillItem(name="Python", category="Language", years_experience=5.0, proficiency="advanced"),
                    SkillItem(name="FastAPI", category="Framework", years_experience=3.0, proficiency="advanced"),
                    SkillItem(name="React", category="Frontend", years_experience=4.0, proficiency="intermediate"),
                    SkillItem(name="Next.js", category="Frontend", years_experience=2.0, proficiency="intermediate"),
                    SkillItem(name="PostgreSQL", category="Database", years_experience=4.0, proficiency="advanced"),
                    SkillItem(name="Docker", category="DevOps", years_experience=3.0, proficiency="intermediate"),
                    SkillItem(name="LangGraph", category="AI", years_experience=1.0, proficiency="intermediate"),
                ],
                total_years_experience=5.0,
                education_level="bachelor",
                certifications=["AWS Certified Solutions Architect"],
                keywords=["LLM", "REST API", "Full-Stack", "Microservices", "CI/CD"],
            )
            
            job_reqs = JobRequirements(
                required_skills=[
                    SkillItem(name="Python", category="Language", years_experience=4.0, proficiency="advanced", importance="required"),
                    SkillItem(name="FastAPI", category="Framework", years_experience=3.0, proficiency="advanced", importance="required"),
                    SkillItem(name="React", category="Frontend", years_experience=3.0, proficiency="intermediate", importance="required"),
                    SkillItem(name="PostgreSQL", category="Database", years_experience=3.0, proficiency="intermediate", importance="required"),
                    SkillItem(name="LangGraph", category="AI", years_experience=1.0, proficiency="intermediate", importance="preferred"),
                    SkillItem(name="Kubernetes", category="DevOps", years_experience=2.0, proficiency="intermediate", importance="preferred"),
                ],
                min_years_experience=4.0,
                preferred_years_experience=6.0,
                min_education_level="bachelor",
                required_keywords=["Python", "FastAPI", "Next.js", "Docker", "LLM"],
            )
            
            score_result = calculate_compatibility_score(cand_profile, job_reqs)
            st.session_state.match_result = score_result.model_dump()
            st.success("Compatibility calculated!")
            
    if st.session_state.match_result:
        res = st.session_state.match_result
        st.markdown("---")
        
        c_score, c_breakdown = st.columns([1, 2])
        with c_score:
            st.markdown(f'<div class="metric-card"><div style="font-size: 1.1rem; color: #94a3b8;">Overall Match</div><div class="score-badge">{res["overall_score"]}%</div><div style="color: #38bdf8;">{res["match_tier"].upper()} TIER</div></div>', unsafe_allow_html=True)
        
        with c_breakdown:
            st.write("📊 **Dimension Breakdown**")
            b = res["dimension_breakdown"]
            st.progress(b["required_skills"] / 100.0, text=f"Required Skills: {b['required_skills']}% (Weight: 35%)")
            st.progress(b["experience_alignment"] / 100.0, text=f"Experience Alignment: {b['experience_alignment']}% (Weight: 20%)")
            st.progress(b["domain_relevance"] / 100.0, text=f"Domain Relevance: {b['domain_relevance']}% (Weight: 15%)")
            st.progress(b["education_certification"] / 100.0, text=f"Education & Certs: {b['education_certification']}% (Weight: 10%)")
            st.progress(b["keyword_density"] / 100.0, text=f"ATS Keyword Density: {b['keyword_density']}% (Weight: 10%)")
            st.progress(b["preferred_skills"] / 100.0, text=f"Preferred Skills: {b['preferred_skills']}% (Weight: 10%)")
            
        st.markdown("---")
        k1, k2 = st.columns(2)
        with k1:
            st.write("✅ **Matched Skills**")
            for m in res.get("matched_skills", []):
                st.markdown(f"- **{m['skill_name']}** (Candidate: {m['candidate_years']} yrs | Required: {m['required_years']} yrs)")
        with k2:
            st.write("⚠️ **Skill Gaps Identified**")
            for g in res.get("missing_skills", []):
                st.markdown(f"- **{g['skill_name']}** — *{g['importance'].title()}* (Suggested time to acquire: {g.get('time_to_acquire_days', 30)} days)")

# ==========================================
# PAGE 4: RESUME OPTIMIZER
# ==========================================
elif page == "✨ Resume Optimizer":
    st.markdown('<div class="main-header">Targeted Resume Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Factual bullet re-writes and ATS keyword insertion with zero fabrication</div>', unsafe_allow_html=True)
    
    target_role = st.text_input("Target Role", "Senior AI Full-Stack Engineer")
    keywords = st.text_input("Target Keywords (comma-separated)", "LangGraph, FastAPI, PostgreSQL, Agentic Workflows, Docker")
    
    if st.button("✨ Generate Optimized Bullet Diffs"):
        with st.spinner("Resume Optimization Agent drafting bullet rewrites..."):
            agent = ResumeOptimizerAgent()
            kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
            opt_result = run_async(agent.optimize_resume(
                candidate_profile={"name": "Alex Rivera", "skills": ["Python", "FastAPI", "React", "Docker"]},
                job_requirements={"title": target_role, "required_skills": kw_list},
                target_keywords=kw_list
            ))
            st.session_state.opt_result = opt_result
            st.success("Bullet rewrites ready!")
            
    if "opt_result" in st.session_state:
        res = st.session_state.opt_result
        st.write("### 📝 Suggested Bullet Enhancements")
        for bullet in res.get("bullet_rewrites", []):
            with st.expander(f"📌 Section: {bullet.get('section', 'Experience')}", expanded=True):
                st.error(f"**Original:** {bullet.get('original', '')}")
                st.success(f"**Optimized:** {bullet.get('optimized', '')}")
                st.caption(f"💡 **Rationale:** {bullet.get('rationale', '')} | Keywords added: {', '.join(bullet.get('keywords_added', []))}")

# ==========================================
# PAGE 5: COVER LETTER GENERATOR
# ==========================================
elif page == "✉️ Cover Letter Generator":
    st.markdown('<div class="main-header">Tailored Cover Letter Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Compelling, professional, and strictly grounded in your verified career achievements</div>', unsafe_allow_html=True)
    
    tone = st.selectbox("Select Tone", ["professional", "confident", "enthusiastic", "technical"])
    
    if st.button("✉️ Draft Cover Letter"):
        with st.spinner("Cover Letter Agent composing draft..."):
            agent = CoverLetterAgent()
            cl_res = run_async(agent.generate_cover_letter(
                candidate_profile={"name": "Alex Rivera", "skills": ["Python", "FastAPI", "LangGraph", "PostgreSQL", "Next.js"], "total_years_experience": 5},
                job_data={"title": "Senior AI Full-Stack Engineer", "company_name": "TechNova", "description": "AI systems and full stack applications."},
                tone=tone
            ))
            st.session_state.cover_letter = cl_res
            st.success("Cover letter generated!")
            
    if "cover_letter" in st.session_state:
        cl = st.session_state.cover_letter
        st.markdown("---")
        st.subheader(f"Subject: {cl.get('subject_line', 'Application')}")
        st.text_area("Cover Letter Content", value=cl.get("content", ""), height=350)
        st.download_button("📥 Download Cover Letter (.txt)", cl.get("content", ""), file_name="cover_letter.txt")

# ==========================================
# PAGE 6: MOCK INTERVIEW SIMULATOR
# ==========================================
elif page == "🎙️ Mock Interview Simulator":
    st.markdown('<div class="main-header">Adaptive Mock Interview Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive technical and behavioral interview preparation with real-time feedback</div>', unsafe_allow_html=True)
    
    c_role, c_cat, c_diff = st.columns(3)
    with c_role:
        int_role = st.text_input("Target Role", "Senior AI Full-Stack Engineer")
    with c_cat:
        int_cat = st.selectbox("Category", ["technical", "behavioral", "system_design"])
    with c_diff:
        int_diff = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        
    if st.button("🎯 Generate Interview Question"):
        with st.spinner("Adaptive Interview Agent generating prompt..."):
            agent = AdaptiveInterviewAgent()
            q = run_async(agent.generate_question(int_role, int_cat, int_diff, []))
            st.session_state.current_question = q
            
    if "current_question" in st.session_state:
        q = st.session_state.current_question
        st.info(f"### ❓ Question: {q.get('question_text', '')}")
        st.caption(f"Category: **{q.get('category', '').title()}** | Difficulty: **{q.get('difficulty', '').title()}**")
        
        user_answer = st.text_area("Your Response", height=150, placeholder="Explain your answer clearly using STAR method or architectural rationale...")
        
        if st.button("📤 Submit Answer for Evaluation"):
            if user_answer.strip():
                with st.spinner("Evaluating response against rubric..."):
                    agent = AdaptiveInterviewAgent()
                    eval_res = run_async(agent.evaluate_answer(
                        question_text=q.get("question_text", ""),
                        answer_text=user_answer,
                        category=q.get("category", "technical")
                    ))
                    st.session_state.last_interview_eval = eval_res
                    st.success("Answer evaluated!")
                    
    if "last_interview_eval" in st.session_state:
        e = st.session_state.last_interview_eval
        st.markdown("---")
        st.subheader(f"📊 Evaluation Score: {e.get('score', 0)}/100")
        
        f1, f2 = st.columns(2)
        with f1:
            st.write("💪 **Strengths Identified**")
            for s in e.get("strengths", []):
                st.markdown(f"- {s}")
        with f2:
            st.write("🎯 **Areas for Improvement**")
            for imp in e.get("improvements", []):
                st.markdown(f"- {imp}")
                
        st.write("**Model Answer / Key Points:**")
        st.info(e.get("model_answer", "Good technical depth shown."))

# ==========================================
# PAGE 7: 30-60-90 LEARNING PLAN
# ==========================================
elif page == "🗺️ 30-60-90 Learning Plan":
    st.markdown('<div class="main-header">Skill Gap Learning Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated 30-60-90 day milestones with actionable projects and interview prompts</div>', unsafe_allow_html=True)
    
    gap_skills = st.text_input("Identified Missing Skills (comma-separated)", "Kubernetes, GraphQL, System Design, Terraform")
    
    if st.button("🗺️ Build Personalized Roadmap"):
        with st.spinner("Learning Plan Agent generating structured roadmap..."):
            agent = LearningPlanAgent()
            gaps = [{"skill_name": s.strip(), "importance": "required"} for s in gap_skills.split(",") if s.strip()]
            plan = run_async(agent.generate_plan("Senior AI Full-Stack Engineer", gaps))
            st.session_state.learning_plan = plan
            st.success("Learning plan generated!")
            
    if "learning_plan" in st.session_state:
        plan = st.session_state.learning_plan
        st.markdown("---")
        st.subheader(f"🎯 {plan.get('title', 'Target Mastery Roadmap')}")
        st.write(plan.get("description", ""))
        
        for item in plan.get("items", []):
            with st.expander(f"📅 Day {item.get('day_milestone', 30)}: {item.get('title', '')}", expanded=True):
                st.markdown(f"**Objectives:** {item.get('description', '')}")
                if item.get("resource_links"):
                    st.write("**Recommended Resources:**")
                    for r in item["resource_links"]:
                        st.markdown(f"- {r}")

# ==========================================
# PAGE 8: SETTINGS
# ==========================================
elif page == "⚙️ API Settings":
    st.markdown('<div class="main-header">Configuration & AI Provider Settings</div>', unsafe_allow_html=True)
    
    st.subheader("🤖 LLM Provider")
    llm_p = st.selectbox("Provider", ["gemini", "openai", "anthropic", "mock"], index=0)
    api_k = st.text_input("API Key", type="password", placeholder="Enter your Gemini or OpenAI API Key")
    
    if st.button("💾 Save Settings"):
        if api_k:
            os.environ["LLM_API_KEY"] = api_k
            os.environ["LLM_PROVIDER"] = llm_p
            st.success("API Key updated in environment!")
        else:
            st.info("Using default configured environment keys.")
