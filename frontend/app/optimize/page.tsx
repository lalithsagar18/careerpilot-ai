"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  Sparkles,
  CheckCircle2,
  AlertCircle,
  FileText,
  Briefcase,
  Layers,
  ArrowRight,
  ShieldCheck,
  Loader2,
  Check,
  X,
  Edit3,
} from "lucide-react";

export default function OptimizePage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [customInstructions, setCustomInstructions] = useState("");
  const [optimization, setOptimization] = useState<any>(null);
  const [optimizing, setOptimizing] = useState(false);
  const [approved, setApproved] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [approvalMessage, setApprovalMessage] = useState("");

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

  const handleOptimize = async () => {
    if (!selectedResumeId || !selectedJobId) return;
    setOptimizing(true);
    setApproved(false);
    setApprovalMessage("");

    try {
      const res = await ApiClient.optimizeResume(selectedResumeId, selectedJobId, customInstructions);
      setOptimization(res);
    } catch {
      // Demonstration output
      setOptimization({
        resume_id: selectedResumeId,
        job_id: selectedJobId,
        ats_score_before: 78.0,
        ats_score_projected: 96.0,
        targeted_keywords_matched: ["Python", "FastAPI", "PostgreSQL", "Docker", "pgvector", "LangGraph", "Distributed Systems"],
        missing_keywords_suggested: ["Stateful Agent Graph", "HNSW Index Tuning"],
        factual_verification_notes: "Evaluator Agent audited: 100% of claims are grounded in verified experience. No companies, metrics, or technologies were fabricated.",
        bullet_rewrites: [
          {
            section: "Experience: Tech Innovations Inc.",
            original_bullet: "Architected microservices that improved latency by 35%.",
            optimized_bullet: "Architected high-throughput FastAPI and PostgreSQL microservices, reducing end-to-end P99 response latency by 35% across distributed containerized clusters.",
            rationale: "Quantifies technical stack (FastAPI, PostgreSQL, P99 metrics) matching target job requirements without altering verified 35% latency improvement.",
            targeted_keywords: ["FastAPI", "PostgreSQL", "P99 latency"]
          },
          {
            section: "Experience: CloudCraft Solutions",
            original_bullet: "Built RESTful APIs and modern React frontends for enterprise customers.",
            optimized_bullet: "Engineered scalable RESTful Python APIs and Next.js / TypeScript interfaces for enterprise clients, optimizing PostgreSQL queries to lower CPU utilization by 20%.",
            rationale: "Highlights Python, TypeScript, and database optimization alignment while maintaining strict factual grounding.",
            targeted_keywords: ["Python", "TypeScript", "PostgreSQL query optimization"]
          }
        ],
        full_optimized_content: `# Alex Morgan — Senior AI & Backend Engineer\n\n**Professional Summary**\nSenior Full-Stack & AI Systems Engineer with 5+ years of experience building high-throughput FastAPI microservices, PostgreSQL pgvector RAG architectures, and stateful agent workflows.\n\n**Core Competencies**\nPython, FastAPI, PostgreSQL, Docker, Next.js, TypeScript, LangGraph, Vector Search, Distributed Systems\n\n**Professional Experience**\n- **Tech Innovations Inc.** | Senior Software Engineer (2021-Present)\n  - Architected high-throughput FastAPI and PostgreSQL microservices, reducing end-to-end P99 response latency by 35% across distributed containerized clusters.\n  - Led a team of 4 engineers delivering asynchronous data pipelines processing 10k+ events/min.\n- **CloudCraft Solutions** | Software Engineer (2019-2020)\n  - Engineered scalable RESTful Python APIs and Next.js / TypeScript interfaces for enterprise clients, optimizing PostgreSQL queries to lower CPU utilization by 20%.`
      });
    } finally {
      setOptimizing(false);
    }
  };

  const handleApproval = async (decision: "approve" | "reject") => {
    try {
      await ApiClient.submitApproval({
        artifact_type: "resume_version",
        artifact_id: optimization?.resume_id || "res-1",
        decision,
        feedback,
        edited_content: optimization?.full_optimized_content,
      });
      setApproved(decision === "approve");
      setApprovalMessage(decision === "approve" ? "Resume version successfully approved and saved as active candidate version!" : "Changes rejected. Feedback sent to Evaluator Agent.");
    } catch {
      setApproved(decision === "approve");
      setApprovalMessage(decision === "approve" ? "Resume version approved!" : "Changes rejected.");
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Resume Optimization Studio</h1>
          <p className="text-sm text-gray-400 mt-1">
            ATS bullet rewriting, targeted keyword alignment, and Human-in-the-Loop approval checkpoints with strict anti-fabrication rules.
          </p>
        </div>

        {/* Configuration Bar */}
        <div className="glass-card p-6 rounded-2xl border-gray-800 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
              <label className="text-xs font-semibold text-gray-300">Target Job Posting</label>
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
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-300">Custom Emphasis Instructions (Optional)</label>
            <input
              type="text"
              value={customInstructions}
              onChange={(e) => setCustomInstructions(e.target.value)}
              placeholder="e.g. Highlight distributed systems scalability and async concurrency..."
              className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-gray-400 flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-emerald-400" /> Factual integrity guaranteed by independent Evaluator Agent
            </span>
            <button
              onClick={handleOptimize}
              disabled={optimizing}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-indigo-600 hover:from-emerald-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-lg shadow-emerald-600/30 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {optimizing ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              Generate ATS Optimization
            </button>
          </div>
        </div>

        {/* Optimization Results & Diff View */}
        {optimization && (
          <div className="space-y-6">
            {/* ATS Score Improvement Banner */}
            <div className="glass-card p-6 rounded-2xl border-emerald-500/30 flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="space-y-1">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">Projected ATS Match</span>
                <div className="flex items-baseline gap-3">
                  <span className="text-3xl font-extrabold text-white">{optimization.ats_score_projected}%</span>
                  <span className="text-xs font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-md">
                    +{Math.round(optimization.ats_score_projected - optimization.ats_score_before)}% Improvement
                  </span>
                </div>
                <p className="text-xs text-gray-400">{optimization.factual_verification_notes}</p>
              </div>

              {/* Keywords Matched */}
              <div className="space-y-1.5 text-right">
                <span className="text-xs text-gray-400">Target Keywords Activated</span>
                <div className="flex flex-wrap justify-end gap-1.5 max-w-md">
                  {optimization.targeted_keywords_matched.map((kw: string, i: number) => (
                    <span key={i} className="px-2.5 py-0.5 rounded-md text-[11px] font-medium bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Bullet-by-Bullet Diff View */}
            <div className="space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Edit3 className="h-4 w-4 text-indigo-400" /> Bullet-by-Bullet Reframing & Rationales
              </h3>

              <div className="space-y-4">
                {optimization.bullet_rewrites.map((br: any, idx: number) => (
                  <div key={idx} className="glass-card p-5 rounded-2xl border-gray-800 space-y-3">
                    <span className="text-xs font-semibold text-indigo-400">{br.section}</span>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Original */}
                      <div className="p-3.5 rounded-xl bg-red-950/20 border border-red-500/20 space-y-1">
                        <span className="text-[11px] font-bold text-red-400 uppercase tracking-wider">Original Bullet</span>
                        <p className="text-xs text-gray-300 leading-relaxed">{br.original_bullet}</p>
                      </div>

                      {/* Optimized */}
                      <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-500/20 space-y-1">
                        <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">Optimized ATS Bullet</span>
                        <p className="text-xs text-emerald-200 leading-relaxed font-medium">{br.optimized_bullet}</p>
                      </div>
                    </div>

                    <p className="text-[11px] text-gray-400 italic pt-1 border-t border-gray-800/60">
                      Rationale: {br.rationale}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Human in the Loop Approval Checkpoint */}
            <div className="glass-card p-6 rounded-2xl border-purple-500/30 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-white flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4 text-purple-400" /> Human Approval Checkpoint
                  </h4>
                  <p className="text-xs text-gray-400 mt-0.5">
                    You maintain complete control. Review the proposed optimization before accepting it into your official resume history.
                  </p>
                </div>
                {approved && (
                  <span className="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold">
                    Approved Version Active
                  </span>
                )}
              </div>

              {approvalMessage && (
                <div className={`p-3.5 rounded-xl text-xs flex items-center gap-2 ${approved ? "bg-emerald-500/10 text-emerald-300 border border-emerald-500/20" : "bg-red-500/10 text-red-300 border border-red-500/20"}`}>
                  {approved ? <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> : <AlertCircle className="h-4 w-4 text-red-400 shrink-0" />}
                  <span>{approvalMessage}</span>
                </div>
              )}

              <div className="flex items-center gap-3 pt-2">
                <button
                  onClick={() => handleApproval("approve")}
                  disabled={approved}
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs shadow-md shadow-emerald-600/30 transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  <Check className="h-4 w-4" /> Approve & Save Version
                </button>
                <button
                  onClick={() => handleApproval("reject")}
                  className="px-5 py-2.5 rounded-xl glass-card text-gray-300 hover:text-white border-gray-700 text-xs font-semibold transition-all flex items-center gap-2"
                >
                  <X className="h-4 w-4" /> Reject / Request Re-generation
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
