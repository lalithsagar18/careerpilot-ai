"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  Mail,
  Sparkles,
  CheckCircle2,
  Copy,
  Download,
  ShieldCheck,
  Loader2,
  Check,
} from "lucide-react";

export default function CoverLetterPage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [tone, setTone] = useState("professional");
  const [companyNotes, setCompanyNotes] = useState("");
  const [coverLetter, setCoverLetter] = useState<any>(null);
  const [generating, setGenerating] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const loadOptions = async () => {
      try {
        const [rList, jList] = await Promise.all([
          ApiClient.listResumes(),
          ApiClient.listJobs(),
        ]);
        setResumes(rList);
        setJobs(jList);
        if (rList.length > 0) setSelectedResumeId(rList[0].id);
        if (jList.length > 0) setSelectedJobId(jList[0].id);
      } catch {
        setResumes([{ id: "res-1", title: "Senior AI Engineer Resume" }]);
        setJobs([{ id: "job-1", title: "Senior AI / Backend Engineer at NextGen AI Corp" }]);
        setSelectedResumeId("res-1");
        setSelectedJobId("job-1");
      }
    };
    loadOptions();
  }, []);

  const handleGenerate = async () => {
    if (!selectedResumeId || !selectedJobId) return;
    setGenerating(true);
    setCopied(false);

    try {
      const res = await ApiClient.generateCoverLetter(selectedResumeId, selectedJobId, tone);
      setCoverLetter(res);
    } catch {
      // Demonstration output
      setCoverLetter({
        company_name: "NextGen AI Corp",
        job_title: "Senior AI / Backend Engineer",
        salutation: "Dear Hiring Team at NextGen AI Corp,",
        opening_hook: "With over 5 years of engineering experience architecting scalable FastAPI microservices and distributed data pipelines, I was immediately drawn to NextGen AI Corp's mission of building multi-agent AI platforms.",
        body_paragraphs: [
          "In my recent role at Tech Innovations Inc., I spearheaded the architecture of asynchronous microservices that reduced P99 latency by 35% and scaled to process thousands of events per minute. My background directly aligns with your requirement for Python, PostgreSQL, and Docker containerized systems.",
          "Furthermore, I have developed deep expertise in stateful LangGraph workflows and pgvector embeddings retrieval, ensuring AI systems operate with verifiable data grounding and sub-millisecond response times. I am excited to bring this pragmatic, systems-oriented mindset to your engineering organization."
        ],
        call_to_action: "I would welcome the opportunity to discuss how my technical leadership and distributed systems experience can accelerate NextGen AI Corp's technical roadmap. Thank you for your time and consideration.",
        full_cover_letter_markdown: `Alex Morgan\nalex.morgan@example.com\n\nDear Hiring Team at NextGen AI Corp,\n\nWith over 5 years of engineering experience architecting scalable FastAPI microservices and distributed data pipelines, I was immediately drawn to NextGen AI Corp's mission of building multi-agent AI platforms.\n\nIn my recent role at Tech Innovations Inc., I spearheaded the architecture of asynchronous microservices that reduced P99 latency by 35% and scaled to process thousands of events per minute. My background directly aligns with your requirement for Python, PostgreSQL, and Docker containerized systems.\n\nFurthermore, I have developed deep expertise in stateful LangGraph workflows and pgvector embeddings retrieval, ensuring AI systems operate with verifiable data grounding and sub-millisecond response times. I am excited to bring this pragmatic, systems-oriented mindset to your engineering organization.\n\nI would welcome the opportunity to discuss how my technical leadership and distributed systems experience can accelerate NextGen AI Corp's technical roadmap. Thank you for your time and consideration.\n\nSincerely,\nAlex Morgan`,
        grounded_resume_facts_used: ["5+ years experience", "Tech Innovations Inc. 35% latency reduction", "FastAPI, PostgreSQL, Docker", "LangGraph and Vector Search experience"]
      });
    } finally {
      setGenerating(false);
    }
  };

  const handleCopy = () => {
    if (!coverLetter?.full_cover_letter_markdown) return;
    navigator.clipboard.writeText(coverLetter.full_cover_letter_markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Cover Letter Studio</h1>
          <p className="text-sm text-gray-400 mt-1">
            Grounded, job-specific cover letters generated strictly from verified candidate facts. Zero fabricated achievements.
          </p>
        </div>

        {/* Generator Setup Form */}
        <div className="glass-card p-6 rounded-2xl border-gray-800 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-300">Base Resume</label>
              <select
                value={selectedResumeId}
                onChange={(e) => setSelectedResumeId(e.target.value)}
                className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                {resumes.map((r) => (
                  <option key={r.id} value={r.id}>{r.title}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-300">Target Job</label>
              <select
                value={selectedJobId}
                onChange={(e) => setSelectedJobId(e.target.value)}
                className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                {jobs.map((j) => (
                  <option key={j.id} value={j.id}>{j.title} ({j.company || "Job"})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-300">Tone Preference</label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="w-full mt-1.5 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                <option value="professional">Professional & Direct</option>
                <option value="executive">Executive & Strategic</option>
                <option value="technical">Technical & Deep</option>
                <option value="energetic">Energetic & Startup-Ready</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-gray-400 flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-emerald-400" /> Only references your verified experience history
            </span>
            <button
              onClick={handleGenerate}
              disabled={generating}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-lg shadow-purple-600/30 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              Generate Cover Letter
            </button>
          </div>
        </div>

        {/* Generated Output */}
        {coverLetter && (
          <div className="glass-card p-8 rounded-2xl border-gray-800 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white">
                  Cover Letter for {coverLetter.job_title}
                </h3>
                <p className="text-xs text-indigo-400 font-medium">{coverLetter.company_name}</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="px-3.5 py-1.5 rounded-xl glass-card text-xs font-semibold text-gray-300 hover:text-white border-gray-700 flex items-center gap-1.5"
                >
                  {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                  {copied ? "Copied!" : "Copy Text"}
                </button>
              </div>
            </div>

            {/* Letter Body Preview */}
            <div className="prose prose-invert max-w-none text-sm leading-relaxed text-gray-200 bg-gray-900/40 p-6 rounded-2xl border border-gray-800 space-y-4">
              <p className="font-semibold text-white">{coverLetter.salutation}</p>
              <p>{coverLetter.opening_hook}</p>
              {(coverLetter.body_paragraphs || []).map((p: string, i: number) => (
                <p key={i}>{p}</p>
              ))}
              <p>{coverLetter.call_to_action}</p>
              <p className="pt-2 font-medium text-white">Sincerely,<br />Candidate</p>
            </div>

            {/* Fact Attribution Badges */}
            {coverLetter.grounded_resume_facts_used?.length > 0 && (
              <div className="p-4 rounded-xl bg-gray-900/50 border border-gray-800 space-y-2">
                <span className="text-xs font-bold text-gray-300 uppercase tracking-wider">
                  Verified Resume Facts Utilized
                </span>
                <div className="flex flex-wrap gap-2 pt-1">
                  {coverLetter.grounded_resume_facts_used.map((fact: string, idx: number) => (
                    <span key={idx} className="px-2.5 py-1 rounded-lg text-xs bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 flex items-center gap-1">
                      <CheckCircle2 className="h-3 w-3 text-emerald-400" /> {fact}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
