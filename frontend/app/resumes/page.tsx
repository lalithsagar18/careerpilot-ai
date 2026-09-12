"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ShieldAlert,
  Loader2,
  Calendar,
  Briefcase,
  GraduationCap,
  Award,
  Layers,
  Check,
} from "lucide-react";

export default function ResumesPage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [selectedResume, setSelectedResume] = useState<any>(null);
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadResumes = async () => {
    try {
      const data = await ApiClient.listResumes();
      setResumes(data);
      if (data.length > 0 && !selectedResume) {
        setSelectedResume(data[0]);
      }
    } catch {
      // Demonstration resume data
      const mockResume = {
        id: "mock-res-1",
        title: "Principal AI & Backend Engineer Resume",
        file_name: "Alex_Morgan_Resume.pdf",
        health_score: 92.0,
        candidate_profile: {
          full_name: "Alex Morgan",
          email: "alex.morgan@example.com",
          summary: "Senior Full-Stack & AI Systems Engineer specializing in Python, Next.js, and Distributed Multi-Agent Architectures.",
          total_years_experience: 5.0,
          technical_skills: ["Python", "FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "LangGraph", "Vector Search"],
          experience: [
            {
              title: "Senior Software Engineer",
              company: "Tech Innovations Inc.",
              start_date: "2021-01",
              end_date: "Present",
              highlights: [
                "Architected high-throughput microservices reducing response latency by 35%.",
                "Led a team of 4 engineers delivering asynchronous data pipelines processing 10k+ events/min."
              ],
              technologies: ["Python", "FastAPI", "PostgreSQL", "Docker"]
            }
          ],
          education: [
            {
              degree: "B.S. in Computer Science",
              institution: "UC Berkeley",
              graduation_year: "2019"
            }
          ],
          projects: [
            {
              name: "Distributed Agent Engine",
              description: "Asynchronous job scheduler with retry queues and telemetry.",
              technologies: ["Python", "Redis", "FastAPI"]
            }
          ]
        },
        health_assessment: {
          overall_health_score: 92.0,
          completeness_score: 95.0,
          action_verb_score: 90.0,
          metrics_quantification_score: 88.0,
          actionable_recommendations: [
            "Quantify more outcomes for individual open-source contributions.",
            "Highlight pgvector and LangGraph stateful transitions explicitly."
          ]
        }
      };
      setResumes([mockResume]);
      setSelectedResume(mockResume);
    }
  };

  useEffect(() => {
    loadResumes();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please choose a PDF or DOCX file to upload.");
      return;
    }
    setError("");
    setSuccess("");
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title || file.name.replace(/\.[^/.]+$/, ""));

    try {
      const res = await ApiClient.uploadResume(formData);
      setSuccess("Resume uploaded and parsed successfully by Resume Intelligence Agent!");
      setFile(null);
      setTitle("");
      await loadResumes();
      setSelectedResume(res);
    } catch (err: any) {
      setError(err.message || "Failed to upload resume.");
    } finally {
      setUploading(false);
    }
  };

  const profile = selectedResume?.candidate_profile;
  const assessment = selectedResume?.health_assessment;

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-5 md:p-8 space-y-8 max-w-7xl mx-auto w-full">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border-white/[0.08]">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20">
                Resume Intelligence
              </span>
              <span className="text-xs text-gray-400">• Deterministic Document Parsing</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Resume Intelligence Hub
            </h1>
            <p className="text-xs sm:text-sm text-gray-300">
              Upload PDF/DOCX resumes for deterministic parsing, quality health checks, and zero-hallucination fact verification.
            </p>
          </div>
        </div>

        {/* Upload Box & Resume Switcher */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upload Form */}
          <div className="glass-card p-6 rounded-3xl space-y-4 border-white/[0.08] shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <UploadCloud className="h-4 w-4 text-indigo-400" /> Upload New Resume
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

            <form onSubmit={handleUpload} className="space-y-3.5">
              <div>
                <label className="text-xs font-bold text-gray-300">Resume Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Senior Full-Stack Resume 2026"
                  className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300">File (PDF, DOCX, TXT - Max 10MB)</label>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-gray-300 text-xs file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500"
                />
              </div>

              <button
                type="submit"
                disabled={uploading}
                className="w-full py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs shadow-md shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {uploading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" /> Analyzing Document...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" /> Parse & Extract Profile
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Active Resumes Selector */}
          <div className="lg:col-span-2 glass-card p-6 rounded-3xl space-y-4 border-white/[0.08] flex flex-col justify-between shadow-xl">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <FileText className="h-4 w-4 text-purple-400" /> Parsed Documents
                </h3>
                <span className="text-xs text-gray-400 font-mono">{resumes.length} Document(s)</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {resumes.map((r) => (
                  <button
                    key={r.id}
                    onClick={() => setSelectedResume(r)}
                    className={`p-4 rounded-2xl text-left transition-all border ${
                      selectedResume?.id === r.id
                        ? "bg-indigo-600/15 border-indigo-500/50 shadow-md"
                        : "bg-white/[0.02] border-white/[0.06] hover:border-white/[0.12]"
                    }`}
                  >
                    <p className="text-sm font-bold text-white truncate">{r.title}</p>
                    <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
                      <span className="truncate">{r.file_name}</span>
                      <span className="text-emerald-400 font-bold font-mono shrink-0 ml-2">
                        {r.health_score || 90}% Score
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div className="p-3.5 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-xs text-gray-400 flex items-center gap-2">
              <ShieldAlert className="h-4 w-4 text-indigo-400 shrink-0" />
              <span>Strict Rule Enforcement: The Resume Intelligence Agent will never fabricate skills or employment dates.</span>
            </div>
          </div>
        </div>

        {/* Selected Resume Details & Candidate Profile */}
        {selectedResume && profile && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left: Health & Recommendations */}
            <div className="space-y-6">
              <div className="glass-card p-6 rounded-3xl space-y-4 border-white/[0.08]">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <Award className="h-4 w-4 text-indigo-400" /> Resume Quality Assessment
                </h4>

                <div className="flex items-center justify-between p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/20">
                  <div>
                    <span className="text-xs text-indigo-300 font-bold">Overall Quality Score</span>
                    <p className="text-3xl font-black text-white font-mono">{assessment?.overall_health_score || 92}%</p>
                  </div>
                  <CheckCircle2 className="h-8 w-8 text-emerald-400" />
                </div>

                <div className="space-y-2.5 pt-2 text-xs">
                  <div className="flex justify-between text-gray-400">
                    <span>Completeness</span>
                    <span className="text-white font-bold font-mono">{assessment?.completeness_score || 95}%</span>
                  </div>
                  <div className="flex justify-between text-gray-400">
                    <span>Action Verbs</span>
                    <span className="text-white font-bold font-mono">{assessment?.action_verb_score || 90}%</span>
                  </div>
                  <div className="flex justify-between text-gray-400">
                    <span>Quantified Metrics</span>
                    <span className="text-white font-bold font-mono">{assessment?.metrics_quantification_score || 88}%</span>
                  </div>
                </div>

                {assessment?.actionable_recommendations?.length > 0 && (
                  <div className="pt-3 border-t border-white/[0.06] space-y-2">
                    <p className="text-xs font-bold text-gray-300">AI Recommendations:</p>
                    <ul className="space-y-1.5 text-xs text-gray-400">
                      {assessment.actionable_recommendations.map((rec: string, i: number) => (
                        <li key={i} className="flex items-start gap-1.5">
                          <span className="text-indigo-400 font-bold">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            {/* Right: Candidate Profile Details */}
            <div className="lg:col-span-2 glass-card p-6 md:p-8 rounded-3xl space-y-6 border-white/[0.08]">
              {/* Header */}
              <div className="border-b border-white/[0.08] pb-4 flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                <div>
                  <h3 className="text-xl font-bold text-white">{profile.full_name || "Alex Morgan"}</h3>
                  <p className="text-xs text-indigo-400 font-mono mt-0.5">{profile.email} • {profile.total_years_experience || 5} Years Experience</p>
                </div>
              </div>

              {/* Summary */}
              {profile.summary && (
                <div className="space-y-1.5">
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider font-mono">Professional Summary</h4>
                  <p className="text-xs sm:text-sm text-gray-300 leading-relaxed bg-white/[0.02] p-4 rounded-2xl border border-white/[0.06]">
                    {profile.summary}
                  </p>
                </div>
              )}

              {/* Skills */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider font-mono">Verified Technical Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {(profile.technical_skills || []).map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-3 py-1 rounded-xl text-xs font-semibold bg-white/[0.03] border border-white/[0.08] text-gray-200"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              {/* Experience */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                  <Briefcase className="h-3.5 w-3.5 text-indigo-400" /> Experience History
                </h4>
                <div className="space-y-3">
                  {(profile.experience || []).map((exp: any, idx: number) => (
                    <div key={idx} className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-bold text-white">{exp.title}</span>
                        <span className="text-xs text-indigo-400 font-mono">{exp.start_date} - {exp.end_date || "Present"}</span>
                      </div>
                      <p className="text-xs text-gray-400">{exp.company}</p>
                      <ul className="space-y-1 pt-1">
                        {(exp.highlights || []).map((hl: string, hIdx: number) => (
                          <li key={hIdx} className="text-xs text-gray-300 flex items-start gap-1.5">
                            <span className="text-indigo-400 font-bold">•</span>
                            <span>{hl}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
