"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  BrainCircuit,
  FileCheck2,
  GitPullRequest,
  Mic,
  Database,
  Search,
  CheckCircle2,
  TrendingUp,
  Award,
  Layers,
  Zap,
  Code2,
  Check,
  BarChart3,
  Bot,
} from "lucide-react";

export default function LandingPage() {
  const [activeTab, setActiveTab] = useState<"match" | "ats" | "interview">("match");

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <section className="relative w-full max-w-7xl px-4 sm:px-6 py-16 md:py-24 flex flex-col items-center text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card border-indigo-500/40 text-xs font-bold text-indigo-300 shadow-xl shadow-indigo-500/10">
          <Sparkles className="h-4 w-4 text-indigo-400 animate-pulse" />
          <span>Next-Gen Multi-Agent Career Intelligence & Deterministic Matching</span>
        </div>

        <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight max-w-5xl leading-[1.12]">
          Land Your Dream Role with <br />
          <span className="text-gradient">Agentic Intelligence & Mathematical Precision</span>
        </h1>

        <p className="text-base sm:text-xl text-gray-300 max-w-3xl font-normal leading-relaxed">
          CareerPilot AI combines <span className="text-white font-semibold underline decoration-indigo-500/50 decoration-2 underline-offset-4">deterministic 6-dimension skill scoring</span>, 
          LangGraph multi-agent orchestration, real-time adaptive mock interviews, and zero-hallucination ATS optimization.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 pt-4 w-full sm:w-auto">
          <Link
            href="/register"
            className="w-full sm:w-auto px-8 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm sm:text-base shadow-2xl shadow-indigo-600/40 flex items-center justify-center gap-2.5 hover:scale-[1.03] transition-all"
          >
            <Sparkles className="h-4 w-4" /> Launch Your Pilot Free <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/login"
            className="w-full sm:w-auto px-8 py-4 rounded-2xl glass-card text-gray-200 hover:text-white font-semibold text-sm sm:text-base border-white/[0.1] hover:border-indigo-500/40 transition-all flex items-center justify-center"
          >
            Sign In to Dashboard
          </Link>
        </div>

        {/* Live Interactive Simulation Widget */}
        <div className="w-full max-w-5xl pt-12">
          <div className="glass-card rounded-3xl border border-indigo-500/30 shadow-2xl shadow-indigo-500/10 p-6 md:p-8 space-y-6 text-left">
            {/* Tab Controls */}
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="text-xs font-bold text-white uppercase tracking-wider font-mono">
                  Live Agentic Engine Sandbox
                </span>
              </div>
              <div className="flex items-center gap-2 bg-gray-950/80 p-1.5 rounded-xl border border-white/[0.08]">
                <button
                  onClick={() => setActiveTab("match")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    activeTab === "match"
                      ? "bg-indigo-600 text-white shadow-md"
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  6-Dim Match Engine
                </button>
                <button
                  onClick={() => setActiveTab("ats")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    activeTab === "ats"
                      ? "bg-indigo-600 text-white shadow-md"
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  ATS Reframing
                </button>
                <button
                  onClick={() => setActiveTab("interview")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    activeTab === "interview"
                      ? "bg-indigo-600 text-white shadow-md"
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  Adaptive Interview
                </button>
              </div>
            </div>

            {/* Tab 1: Match Score Demo */}
            {activeTab === "match" && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
                <div className="md:col-span-1 p-6 rounded-2xl bg-gradient-to-b from-indigo-950/40 to-gray-950/80 border border-indigo-500/30 text-center space-y-3">
                  <span className="text-xs font-mono font-bold text-indigo-300 uppercase">Deterministic Match</span>
                  <div className="relative flex items-center justify-center my-2">
                    <div className="h-28 w-28 rounded-full border-4 border-indigo-500/30 flex items-center justify-center bg-indigo-950/30">
                      <span className="text-3xl font-black text-white">87.5%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-center gap-1.5 text-xs text-emerald-400 font-bold">
                    <CheckCircle2 className="h-3.5 w-3.5" /> High Alignment Tier
                  </div>
                </div>

                <div className="md:col-span-2 space-y-3 text-xs">
                  <p className="text-gray-300 font-semibold mb-2">
                    Target Role: <span className="text-white">Senior AI / Backend Engineer</span>
                  </p>
                  
                  <div className="space-y-2">
                    <div>
                      <div className="flex justify-between text-gray-400 mb-1">
                        <span>Required Skills (Python, FastAPI, Postgres - 40%)</span>
                        <span className="text-indigo-300 font-bold font-mono">92.0%</span>
                      </div>
                      <div className="w-full bg-gray-900 rounded-full h-2">
                        <div className="bg-indigo-500 h-2 rounded-full" style={{ width: "92%" }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-gray-400 mb-1">
                        <span>Experience Depth & Seniority (20%)</span>
                        <span className="text-purple-300 font-bold font-mono">100.0%</span>
                      </div>
                      <div className="w-full bg-gray-900 rounded-full h-2">
                        <div className="bg-purple-500 h-2 rounded-full" style={{ width: "100%" }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-gray-400 mb-1">
                        <span>Preferred & Architecture (LangGraph, Vector DB - 15%)</span>
                        <span className="text-emerald-300 font-bold font-mono">80.0%</span>
                      </div>
                      <div className="w-full bg-gray-900 rounded-full h-2">
                        <div className="bg-emerald-500 h-2 rounded-full" style={{ width: "80%" }}></div>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-gray-900/80 border border-white/[0.08] text-[11px] text-gray-300 mt-2">
                    <span className="font-bold text-indigo-300">Deterministic Guarantee:</span> Mathematical weighting guarantees identical scores across runs. No LLM randomness in numbers.
                  </div>
                </div>
              </div>
            )}

            {/* Tab 2: ATS Reframing Demo */}
            {activeTab === "ats" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-400">ATS Keyword Match: <strong className="text-emerald-400">78% ➔ 96%</strong></span>
                  <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold">
                    100% Factually Grounded
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-4 rounded-2xl bg-rose-950/20 border border-rose-500/20 space-y-2">
                    <span className="text-[10px] uppercase font-bold text-rose-400 font-mono">Original Bullet</span>
                    <p className="text-gray-300 leading-relaxed">
                      "Architected microservices that improved response latency by 35%."
                    </p>
                  </div>

                  <div className="p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
                    <span className="text-[10px] uppercase font-bold text-emerald-400 font-mono">Optimized ATS Bullet</span>
                    <p className="text-emerald-200 leading-relaxed font-medium">
                      "Architected high-throughput FastAPI and PostgreSQL microservices, reducing end-to-end P99 response latency by 35% across distributed containerized clusters."
                    </p>
                  </div>
                </div>

                <p className="text-[11px] text-gray-400 italic">
                  * Evaluator Agent audited: Zero hallucinated employers, false metrics, or fabricated tools.
                </p>
              </div>
            )}

            {/* Tab 3: Mock Interview Demo */}
            {activeTab === "interview" && (
              <div className="space-y-4 text-xs">
                <div className="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-500/30 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-indigo-300 flex items-center gap-1.5">
                      <Bot className="h-4 w-4" /> AI Interviewer Question
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono">
                      SYSTEMS ARCHITECTURE
                    </span>
                  </div>
                  <p className="text-white font-medium text-sm leading-relaxed">
                    "How do you design high-throughput vector search in PostgreSQL pgvector or Oracle 23ai while strictly preventing multi-tenant data leakage?"
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-gray-900/70 border border-white/[0.08] space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold">
                    <span className="text-emerald-400 flex items-center gap-1">
                      <CheckCircle2 className="h-3.5 w-3.5" /> AI Rubric Score: 92/100
                    </span>
                    <span className="text-gray-400">Relevance: 95% • Depth: 90%</span>
                  </div>
                  <p className="text-gray-300 text-[11px] leading-relaxed">
                    "Exceptional grasp of tenant isolation. You correctly highlighted composite indexing with user_id partitions before cosine distance calculation."
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full pt-16 text-left">
          <div className="glass-card glass-card-hover p-7 rounded-3xl space-y-3.5 border-white/[0.08]">
            <div className="h-12 w-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <BrainCircuit className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Deterministic Matching</h3>
            <p className="text-xs sm:text-sm text-gray-300 leading-relaxed">
              No hallucinated scores. 6-dimension mathematical weighting across required skills, experience, and tools.
            </p>
          </div>

          <div className="glass-card glass-card-hover p-7 rounded-3xl space-y-3.5 border-white/[0.08]">
            <div className="h-12 w-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <FileCheck2 className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Factually Grounded ATS Optimization</h3>
            <p className="text-xs sm:text-sm text-gray-300 leading-relaxed">
              Strictly reframes your verified achievements without inventing skills, companies, or metrics.
            </p>
          </div>

          <div className="glass-card glass-card-hover p-7 rounded-3xl space-y-3.5 border-white/[0.08]">
            <div className="h-12 w-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Mic className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Adaptive Mock Interviews</h3>
            <p className="text-xs sm:text-sm text-gray-300 leading-relaxed">
              Live technical and behavioral interview simulation with deep rubric feedback and follow-up probing.
            </p>
          </div>
        </div>
      </section>

      {/* Architecture Highlights Banner */}
      <section className="w-full border-t border-white/[0.08] bg-black/40 py-16 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-2 text-left">
            <h4 className="text-2xl font-bold text-white">Enterprise Security & Strict Multi-Tenancy</h4>
            <p className="text-xs sm:text-sm text-gray-300 max-w-xl">
              User-scoped vector partitioning, SSRF protection, prompt injection boundaries, and Model Context Protocol (MCP) tool integration.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="px-3.5 py-2 rounded-xl bg-white/[0.03] border border-white/[0.08] text-xs font-mono text-gray-300 flex items-center gap-2 shadow-sm">
              <CheckCircle2 className="h-4 w-4 text-emerald-400" /> PostgreSQL pgvector
            </span>
            <span className="px-3.5 py-2 rounded-xl bg-white/[0.03] border border-white/[0.08] text-xs font-mono text-gray-300 flex items-center gap-2 shadow-sm">
              <CheckCircle2 className="h-4 w-4 text-indigo-400" /> LangGraph Workflows
            </span>
            <span className="px-3.5 py-2 rounded-xl bg-white/[0.03] border border-white/[0.08] text-xs font-mono text-gray-300 flex items-center gap-2 shadow-sm">
              <CheckCircle2 className="h-4 w-4 text-purple-400" /> MCP Standard Tools
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
