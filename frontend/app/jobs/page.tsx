"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  Briefcase,
  Globe,
  FileText,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Building2,
  MapPin,
  Clock,
  Layers,
  ShieldCheck,
} from "lucide-react";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedJob, setSelectedJob] = useState<any>(null);
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("Remote");
  const [sourceUrl, setSourceUrl] = useState("");
  const [rawDescription, setRawDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadJobs = async () => {
    try {
      const data = await ApiClient.listJobs();
      setJobs(data);
      if (data.length > 0 && !selectedJob) {
        setSelectedJob(data[0]);
      }
    } catch {
      // Mock initial job
      const mockJob = {
        id: "mock-job-1",
        title: "Senior AI / Backend Engineer",
        company: "NextGen AI Corp",
        location: "Remote / San Francisco",
        employment_type: "Full-time",
        seniority: "Senior",
        parsed_data: {
          title: "Senior AI / Backend Engineer",
          company: "NextGen AI Corp",
          summary: "Seeking a Senior Backend Engineer to build multi-agent architectures and high-scale FastAPI services.",
          required_skills: ["Python", "FastAPI", "PostgreSQL", "Docker", "System Design"],
          preferred_skills: ["LangGraph", "Vector Search", "TypeScript", "AWS"],
          required_technologies: ["Python", "PostgreSQL", "Docker"],
          required_years_experience: 4.0,
          required_education: "Bachelor's in Computer Science",
          responsibilities: [
            "Architect and deploy stateful agentic workflows in LangGraph.",
            "Optimize PostgreSQL pgvector embeddings index queries.",
            "Collaborate with product and UI engineering teams."
          ],
          keywords: ["Python", "FastAPI", "Agentic AI", "PostgreSQL", "pgvector", "LangGraph", "Docker"]
        }
      };
      setJobs([mockJob]);
      setSelectedJob(mockJob);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const newJob = await ApiClient.createJob({
        title: title || "Job Posting",
        company: company || "Target Company",
        location,
        source_url: sourceUrl || undefined,
        raw_description: rawDescription || "Senior Engineer role with Python, FastAPI, and PostgreSQL requirements.",
      });
      setSuccess("Job analyzed and requirements extracted by Job Research Agent!");
      setTitle("");
      setCompany("");
      setSourceUrl("");
      setRawDescription("");
      await loadJobs();
      setSelectedJob(newJob);
    } catch (err: any) {
      setError(err.message || "Failed to analyze job.");
    } finally {
      setLoading(false);
    }
  };

  const parsed = selectedJob?.parsed_data;

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-5 md:p-8 space-y-8 max-w-7xl mx-auto w-full">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border-white/[0.08]">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-purple-400 bg-purple-500/10 px-2.5 py-0.5 rounded-full border border-purple-500/20">
                Job Research Agent
              </span>
              <span className="text-xs text-gray-400">• SSRF Protected Scraping</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Job Research & Requirement Ingestion
            </h1>
            <p className="text-xs sm:text-sm text-gray-300">
              Ingest job postings from text or URLs with automatic requirement structuring and skill breakdown.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Job Ingestion Form */}
          <div className="glass-card p-6 rounded-3xl space-y-4 border-white/[0.08] shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Briefcase className="h-4 w-4 text-purple-400" /> Ingest Target Job Posting
            </h3>

            {error && (
              <div className="p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
                <AlertCircle className="h-4 w-4 text-rose-400 shrink-0" />
                <span>{error}</span>
              </div>
            )}
            {success && (
              <div className="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                <span>{success}</span>
              </div>
            )}

            <form onSubmit={handleAnalyze} className="space-y-3.5">
              <div>
                <label className="text-xs font-bold text-gray-300">Job Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Senior Backend AI Engineer"
                  className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-purple-500"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300">Company Name</label>
                <input
                  type="text"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="e.g. Stripe, OpenAI, Oracle"
                  className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-purple-500"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300">Job Posting URL (Optional)</label>
                <div className="relative mt-1.5">
                  <Globe className="absolute left-3.5 top-3 h-4 w-4 text-gray-500" />
                  <input
                    type="url"
                    value={sourceUrl}
                    onChange={(e) => setSourceUrl(e.target.value)}
                    placeholder="https://jobs.lever.co/company/..."
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300">Job Description Text</label>
                <textarea
                  rows={4}
                  value={rawDescription}
                  onChange={(e) => setRawDescription(e.target.value)}
                  placeholder="Paste complete job requirements, qualifications, and responsibilities..."
                  className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-purple-500"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-2xl bg-gradient-to-r from-purple-600 via-indigo-600 to-purple-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs shadow-md shadow-purple-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" /> Structuring Job Requirements...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" /> Analyze & Extract Requirements
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Analyzed Jobs List */}
          <div className="lg:col-span-2 glass-card p-6 md:p-8 rounded-3xl border-white/[0.08] space-y-4 flex flex-col justify-between shadow-xl">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-purple-400" /> Saved Target Job Postings
                </h3>
                <span className="text-xs text-gray-400 font-mono">{jobs.length} Posting(s)</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {jobs.map((j) => (
                  <button
                    key={j.id}
                    onClick={() => setSelectedJob(j)}
                    className={`p-4 rounded-2xl text-left transition-all border ${
                      selectedJob?.id === j.id
                        ? "bg-purple-600/15 border-purple-500/50 shadow-md"
                        : "bg-white/[0.02] border-white/[0.06] hover:border-white/[0.12]"
                    }`}
                  >
                    <p className="text-sm font-bold text-white truncate">{j.title}</p>
                    <p className="text-xs text-indigo-400 mt-1 font-semibold">{j.company}</p>
                    <div className="flex items-center justify-between mt-2 text-[11px] text-gray-400">
                      <span>{j.location || "Remote"}</span>
                      <span className="text-purple-300 font-bold font-mono">{j.seniority || "Mid-Senior"}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Selected Job Requirements Breakdown */}
            {selectedJob && parsed && (
              <div className="pt-4 border-t border-white/[0.08] space-y-4">
                <div>
                  <h4 className="text-base font-bold text-white flex items-center gap-2">
                    {parsed.title} <span className="text-xs text-purple-400 font-normal">at {parsed.company}</span>
                  </h4>
                  {parsed.summary && <p className="text-xs text-gray-300 mt-1 leading-relaxed">{parsed.summary}</p>}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Required Skills */}
                  <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] space-y-2">
                    <p className="text-xs font-bold text-indigo-300 font-mono uppercase">Required Core Competencies</p>
                    <div className="flex flex-wrap gap-1.5">
                      {(parsed.required_skills || []).map((s: string, idx: number) => (
                        <span key={idx} className="px-3 py-1 rounded-xl text-xs bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-semibold">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Preferred Skills */}
                  <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] space-y-2">
                    <p className="text-xs font-bold text-purple-300 font-mono uppercase">Preferred / Growth Areas</p>
                    <div className="flex flex-wrap gap-1.5">
                      {(parsed.preferred_skills || []).map((s: string, idx: number) => (
                        <span key={idx} className="px-3 py-1 rounded-xl text-xs bg-purple-500/10 text-purple-300 border border-purple-500/20 font-semibold">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
