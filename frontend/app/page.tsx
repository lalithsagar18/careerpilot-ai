"use client";

import React from "react";
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
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <section className="relative w-full max-w-7xl px-6 py-20 md:py-28 flex flex-col items-center text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card border-indigo-500/30 text-xs font-semibold text-indigo-300 shadow-md">
          <Sparkles className="h-4 w-4 text-indigo-400" />
          <span>Next-Gen Multi-Agent Career Intelligence & Oracle AI Ready</span>
        </div>

        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight max-w-5xl leading-[1.15]">
          Supercharge Your Career with <br />
          <span className="text-gradient">Agentic Intelligence & Verified Data</span>
        </h1>

        <p className="text-lg sm:text-xl text-gray-400 max-w-3xl font-normal leading-relaxed">
          CareerPilot AI combines <span className="text-gray-200 font-medium">deterministic mathematical matching</span>, 
          LangGraph multi-agent workflows, adaptive mock interviews, and zero-hallucination resume optimization.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 pt-4">
          <Link
            href="/register"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-base shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 hover:scale-[1.02] transition-all"
          >
            Launch Your Pilot <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/login"
            className="w-full sm:w-auto px-8 py-4 rounded-xl glass-card text-gray-300 hover:text-white font-semibold text-base border-gray-700/80 hover:border-gray-600 transition-all flex items-center justify-center"
          >
            Sign In to Dashboard
          </Link>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full pt-16 text-left">
          <div className="glass-card glass-card-hover p-6 rounded-2xl space-y-3">
            <div className="h-12 w-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <BrainCircuit className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Deterministic Matching</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              No hallucinated scores. 6-dimension mathematical weighting across required skills, experience, and tools.
            </p>
          </div>

          <div className="glass-card glass-card-hover p-6 rounded-2xl space-y-3">
            <div className="h-12 w-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <FileCheck2 className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Factually Grounded ATS Optimization</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Strictly reframes your verified achievements without inventing skills, companies, or metrics.
            </p>
          </div>

          <div className="glass-card glass-card-hover p-6 rounded-2xl space-y-3">
            <div className="h-12 w-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Mic className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Adaptive Mock Interviews</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Live technical and behavioral interview simulation with deep rubric feedback and follow-up probing.
            </p>
          </div>
        </div>
      </section>

      {/* Architecture Highlights Banner */}
      <section className="w-full border-t border-gray-800/80 bg-gray-950/40 py-16 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-2 text-left">
            <h4 className="text-2xl font-bold text-white">Built for High Security & Data Privacy</h4>
            <p className="text-sm text-gray-400 max-w-xl">
              Strict user-scoped vector partitioning, SSRF protection, prompt injection boundaries, and Model Context Protocol (MCP) tool integration.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="px-3.5 py-1.5 rounded-lg bg-gray-900 border border-gray-800 text-xs font-mono text-gray-300 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-400" /> PostgreSQL pgvector
            </span>
            <span className="px-3.5 py-1.5 rounded-lg bg-gray-900 border border-gray-800 text-xs font-mono text-gray-300 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-indigo-400" /> LangGraph Workflows
            </span>
            <span className="px-3.5 py-1.5 rounded-lg bg-gray-900 border border-gray-800 text-xs font-mono text-gray-300 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-purple-400" /> MCP Standard Tools
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
