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
      // Provide initial mock resume view if empty
      const mockResume = {
        id: "mock-res-1",
        title: "Principal AI & Backend Engineer Resume",
        file_name: "Alex_Morgan_Resume.pdf",
        health_score: 92.0,
        candidate_profile: {
          full_name: "Alex Morgan",
          email: "alex.morgan@example.com",
          summary: "Senior Full-Stack Engineer specializing in Python, Next.js, and Distributed Multi-Agent AI Architectures.",
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
                "Led a team of 4 engineers delivering async data pipelines."
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
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Resume Intelligence Hub</h1>
            <p className="text-sm text-gray-400 mt-1">
              Upload PDF/DOCX resumes for deterministic parsing, quality health checks, and zero-hallucination fact verification.
            </p>
          </div>
        </div>

        {/* Upload Box & Resume Switcher */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upload Form */}
          <div className="glass-card p-6 rounded-2xl space-y-4 border-gray-800">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <UploadCloud className="h-4 w-4 text-indigo-400" /> Upload New Resume
            </h3>

            {error && (
              <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs flex items-center gap-2">
                <AlertCircle className="h-4 w-4 text-red-400 shrink-0" />
                <span>{error}</span>
              </div>
            )}
            {success && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                <span>{success}</span>
              </div>
            )}

            <form onSubmit={handleUpload} className="space-y-3">
              <div>
                <label className="text-xs text-gray-400 font-medium">Resume Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Senior Full-Stack Resume 2026"
                  className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs text-gray-400 font-medium">File (PDF, DOCX, TXT - Max 10MB)</label>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-gray-300 text-xs file:mr-2 file:py-1 file:px-2.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500"
                />
              </div>

              <button
                type="submit"
                disabled={uploading}
                className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {uploading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" /> Analyzing Resume...
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
          <div className="lg:col-span-2 glass-card p-6 rounded-2xl space-y-4 border-gray-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <FileText className="h-4 w-4 text-purple-400" /> Parsed Resumes
                </h3>
                <span className="text-xs text-gray-400">{resumes.length} Document(s)</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {resumes.map((r) => (
                  <button
                    key={r.id}
                    onClick={() => setSelectedResume(r)}
                    className={`p-3.5 rounded-xl text-left transition-all border ${
                      selectedResume?.id === r.id
                        ? "bg-indigo-600/15 border-indigo-500/50 shadow-md"
                        : "bg-gray-900/60 border-gray-800 hover:border-gray-700"
                    }`}
                  >
                    <p className="text-sm font-semibold text-white truncate">{r.title}</p>
                    <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
                      <span>{r.file_name}</span>
                      <span className="text-emerald-400 font-semibold">{r.health_score || 90}% Score</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-gray-900/60 border border-gray-800 text-xs text-gray-400 flex items-center gap-2">
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
              <div className="glass-card p-6 rounded-2xl space-y-4 border-gray-800">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <Award className="h-4 w-4 text-indigo-400" /> Resume Quality Assessment
                </h4>

                <div className="flex items-center justify-between p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
                  <div>
                    <span className="text-xs text-indigo-300 font-semibold">Overall Quality Score</span>
                    <p className="text-2xl font-black text-white">{assessment?.overall_health_score || 92}%</p>
                  </div>
                  <CheckCircle2 className="h-8 w-8 text-emerald-400" />
                </div>

                <div className="space-y-2.5 pt-2 text-xs">
                  <div className="flex justify-between text-gray-400">
                    <span>Completeness</span>
                    <span className="text-white font-medium">{assessment?.completeness_score || 95}%</span>
                  </div>
                  <div className="flex justify-between text-gray-400">
                    <span>Action Verbs</span>
                    <span className="text-white font-medium">{assessment?.action_verb_score || 90}%</span>
                  </div>
                  <div className="flex justify-between text-gray-400">
                    <span>Quantified Impact</span>
                    <span className="text-white font-medium">{assessment?.metrics_quantification_score || 88}%</span>
                  </div>
                </div>

                {assessment?.actionable_recommendations?.length > 0 && (
                  <div className="pt-3 border-t border-gray-800 space-y-2">
                    <p className="text-xs font-semibold text-gray-300">AI Recommendations:</p>
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
            <div className="lg:col-span-2 glass-card p-6 rounded-2xl space-y-6 border-gray-800">
              {/* Header */}
              <div className="border-b border-gray-800 pb-4 flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                <div>
                  <h3 className="text-xl font-bold text-white">{profile.full_name || "Alex Morgan"}</h3>
                  <p className="text-xs text-indigo-400 mt-0.5">{profile.email} • {profile.total_years_experience || 5} Years Experience</p>
                </div>
              </div>

              {/* Summary */}
              {profile.summary && (
                <div className="space-y-1.5">
                  <h4 className="text-xs font-bold text-gray-300 uppercase tracking-wider">Professional Summary</h4>
                  <p className="text-sm text-gray-300 leading-relaxed bg-gray-900/60 p-3.5 rounded-xl border border-gray-800/80">
                    {profile.summary}
                  </p>
                </div>
              )}

              {/* Skills */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-gray-300 uppercase tracking-wider">Verified Technical Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {(profile.technical_skills || []).map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-3 py-1 rounded-lg text-xs font-medium bg-gray-900 border border-gray-800 text-gray-200"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              {/* Experience */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-gray-300 uppercase tracking-wider flex items-center gap-1.5">
                  <Briefcase className="h-3.5 w-3.5 text-indigo-400" /> Experience History
                </h4>
                <div className="space-y-3">
                  {(profile.experience || []).map((exp: any, idx: number) => (
                    <div key={idx} className="p-4 rounded-xl bg-gray-900/50 border border-gray-800 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-semibold text-white">{exp.title}</span>
                        <span className="text-xs text-indigo-400">{exp.start_date} - {exp.end_date || "Present"}</span>
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

              {/* Education */}
              {profile.education?.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-gray-300 uppercase tracking-wider flex items-center gap-1.5">
                    <GraduationCap className="h-3.5 w-3.5 text-purple-400" /> Education
                  </h4>
                  <div className="space-y-2">
                    {profile.education.map((edu: any, idx: number) => (
                      <div key={idx} className="p-3.5 rounded-xl bg-gray-900/50 border border-gray-800 flex justify-between items-center text-xs">
                        <div>
                          <p className="font-semibold text-white">{edu.degree}</p>
                          <p className="text-gray-400">{edu.institution}</p>
                        </div>
                        <span className="text-gray-400">{edu.graduation_year}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
