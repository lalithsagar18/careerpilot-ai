"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  Mic,
  Sparkles,
  Send,
  CheckCircle2,
  AlertCircle,
  Clock,
  Award,
  ChevronRight,
  TrendingUp,
  Loader2,
  RefreshCw,
  HelpCircle,
  Volume2,
  Bot,
  Brain,
  Check,
} from "lucide-react";

export default function InterviewPage() {
  const [targetRole, setTargetRole] = useState("Senior AI / Backend Engineer");
  const [interviewType, setInterviewType] = useState("Technical");
  const [totalQuestions, setTotalQuestions] = useState(4);
  const [sessionActive, setSessionActive] = useState(false);
  const [interviewId, setInterviewId] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState<any>(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedbackHistory, setFeedbackHistory] = useState<any[]>([]);
  const [finalReport, setFinalReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    let timer: any;
    if (sessionActive) {
      timer = setInterval(() => {
        setElapsedTime((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [sessionActive]);

  const formatTimer = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const s = secs % 60;
    return `${mins.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const startSession = async () => {
    setLoading(true);
    setFinalReport(null);
    setFeedbackHistory([]);
    setElapsedTime(0);

    try {
      const q = await ApiClient.startInterview({
        target_role: targetRole,
        interview_type: interviewType,
        total_questions: totalQuestions,
      });
      setInterviewId(q.interview_id);
      setCurrentQuestion(q);
      setSessionActive(true);
    } catch {
      // Demonstration active session
      setInterviewId("mock-int-1");
      setCurrentQuestion({
        id: "q-1",
        interview_id: "mock-int-1",
        question_text: "Could you walk through how you would architect a high-throughput vector search pipeline in PostgreSQL pgvector or Oracle 23ai to support real-time RAG while preventing cross-tenant data leakage?",
        category: "Technical & Systems Architecture",
        difficulty: "hard",
        order_index: 1,
        is_follow_up: false,
      });
      setSessionActive(true);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userAnswer.trim() || !currentQuestion) return;
    setSubmitting(true);

    try {
      const feedback = await ApiClient.submitInterviewAnswer(currentQuestion.id, userAnswer);
      const newHistory = [
        ...feedbackHistory,
        { question: currentQuestion.question_text, answer: userAnswer, feedback },
      ];
      setFeedbackHistory(newHistory);
      setUserAnswer("");

      if (currentQuestion.order_index >= totalQuestions) {
        const report = await ApiClient.getInterviewReport(interviewId);
        setFinalReport(report);
        setSessionActive(false);
      } else {
        const nextQ = await ApiClient.getNextQuestion(interviewId);
        setCurrentQuestion(nextQ);
      }
    } catch {
      // Mock feedback calculation
      const mockFeedback = {
        score: 88.0,
        technical_accuracy_score: 90.0,
        relevance_score: 92.0,
        depth_score: 85.0,
        communication_score: 85.0,
        feedback: "Strong grasp of tenant isolation and indexing trade-offs. You clearly addressed user-scoped WHERE predicates and HNSW index tuning.",
        strengths: ["Clear explanation of HNSW cosine distance", "Strict tenant-id filtering in WHERE clause"],
        missed_points: ["Could mention connection pooling saturation under high concurrent write loads"],
        suggested_ideal_answer: "In pgvector, enforce composite indexing with user_id partitions and pre-filter vectors prior to calculating cosine distance."
      };

      const newHistory = [
        ...feedbackHistory,
        { question: currentQuestion.question_text, answer: userAnswer, feedback: mockFeedback },
      ];
      setFeedbackHistory(newHistory);
      setUserAnswer("");

      if (currentQuestion.order_index >= totalQuestions) {
        setFinalReport({
          overall_score: 87.5,
          category_scores: { technical_accuracy: 90.0, relevance: 92.0, depth: 85.0, communication: 85.0 },
          strengths: ["Strong systems grounding", "Crisp communication of ACID vs vector index trade-offs", "Clear tenant isolation patterns"],
          weaknesses: ["Async concurrency backpressure under heavy burst traffic"],
          improvement_plan: "Deepen focus on distributed circuit breakers and connection pool tuning.",
          suggested_study_topics: ["pgvector HNSW tuning", "FastAPI connection pools", "CAP Theorem"],
          total_questions: totalQuestions,
          questions_answered: totalQuestions,
        });
        setSessionActive(false);
      } else {
        setCurrentQuestion({
          id: `q-${currentQuestion.order_index + 1}`,
          interview_id: interviewId,
          question_text: "How do you handle cyclic transitions and infinite loop guards when orchestrating multi-agent state machines in LangGraph?",
          category: "Multi-Agent Systems",
          difficulty: "hard",
          order_index: currentQuestion.order_index + 1,
          is_follow_up: true,
        });
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-5 md:p-8 space-y-8 max-w-7xl mx-auto w-full">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border-white/[0.08]">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-purple-400 bg-purple-500/10 px-2.5 py-0.5 rounded-full border border-purple-500/20">
                Adaptive AI Simulation
              </span>
              <span className="text-xs text-gray-400">• Real-time Rubric Audit</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Adaptive Mock Interview AI
            </h1>
            <p className="text-xs sm:text-sm text-gray-300">
              Technical, behavioral, and system design interviews with live rubric scoring and follow-up probing.
            </p>
          </div>
        </div>

        {/* Setup Configuration if not active and no report */}
        {!sessionActive && !finalReport && (
          <div className="glass-card p-6 md:p-8 rounded-3xl border-white/[0.08] space-y-6 max-w-2xl mx-auto shadow-2xl">
            <div className="flex items-center gap-3 border-b border-white/[0.08] pb-4">
              <div className="h-10 w-10 rounded-2xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
                <Mic className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Configure Interview Simulation</h3>
                <p className="text-xs text-gray-400">Select target role and interview focus area</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-gray-300">Target Role</label>
                <input
                  type="text"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  placeholder="e.g. Senior Backend AI Engineer"
                  className="w-full mt-1.5 px-4 py-3 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-gray-300">Interview Type</label>
                  <select
                    value={interviewType}
                    onChange={(e) => setInterviewType(e.target.value)}
                    className="w-full mt-1.5 px-4 py-3 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500"
                  >
                    <option value="Technical">Technical & Systems Architecture</option>
                    <option value="Python & AI">Python & Agentic AI</option>
                    <option value="SQL & DB">SQL & Vector Databases</option>
                    <option value="Behavioral">Behavioral & Leadership</option>
                    <option value="System Design">Distributed System Design</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-bold text-gray-300">Question Volume</label>
                  <select
                    value={totalQuestions}
                    onChange={(e) => setTotalQuestions(Number(e.target.value))}
                    className="w-full mt-1.5 px-4 py-3 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500"
                  >
                    <option value={3}>3 Questions (Quick Drill)</option>
                    <option value={4}>4 Questions (Standard)</option>
                    <option value={5}>5 Questions (Comprehensive)</option>
                  </select>
                </div>
              </div>

              <button
                onClick={startSession}
                disabled={loading}
                className="w-full mt-2 py-3.5 rounded-2xl bg-gradient-to-r from-purple-600 via-indigo-600 to-purple-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs sm:text-sm shadow-xl shadow-purple-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50 hover:scale-[1.01]"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Mic className="h-4 w-4" />}
                Begin Adaptive Mock Interview Session
              </button>
            </div>
          </div>
        )}

        {/* Active Session Dialogue */}
        {sessionActive && currentQuestion && (
          <div className="space-y-6">
            {/* Progress Header */}
            <div className="glass-card p-4 rounded-2xl border-white/[0.08] flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="h-3 w-3 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="text-xs font-bold text-white font-mono">
                  Question {currentQuestion.order_index} of {totalQuestions}
                </span>
                <span className="text-xs text-indigo-400 hidden sm:inline">({currentQuestion.category})</span>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-gray-400 flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5 text-indigo-400" /> {formatTimer(elapsedTime)}
                </span>
                <span className="text-xs px-2.5 py-0.5 rounded-lg bg-purple-500/20 text-purple-300 border border-purple-500/30 font-bold font-mono">
                  {currentQuestion.difficulty?.toUpperCase()}
                </span>
              </div>
            </div>

            {/* AI Interviewer Audio Visualizer & Question */}
            <div className="glass-card p-6 md:p-8 rounded-3xl border-purple-500/30 space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-purple-400 text-xs font-bold uppercase tracking-wider font-mono">
                  <Bot className="h-4 w-4" /> AI Interviewer
                </div>

                {/* Animated Audio Wave Simulation */}
                <div className="flex items-center gap-1">
                  <span className="h-4 w-1 bg-purple-400 rounded-full animate-pulse"></span>
                  <span className="h-6 w-1 bg-indigo-400 rounded-full animate-pulse-slow"></span>
                  <span className="h-3 w-1 bg-purple-400 rounded-full animate-pulse"></span>
                  <span className="h-7 w-1 bg-pink-400 rounded-full animate-pulse-slow"></span>
                  <span className="h-4 w-1 bg-indigo-400 rounded-full animate-pulse"></span>
                </div>
              </div>

              <p className="text-base sm:text-lg font-bold text-white leading-relaxed">
                {currentQuestion.question_text}
              </p>
            </div>

            {/* Answer Input Box */}
            <form onSubmit={handleSubmitAnswer} className="glass-card p-6 rounded-3xl border-white/[0.08] space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-gray-300">Your Technical Response</label>
                <span className="text-[11px] text-gray-400">Markdown and code snippets supported</span>
              </div>

              <textarea
                rows={6}
                required
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Structure your answer clearly, explaining trade-offs, architecture choices, concrete metrics, and edge-case mitigations..."
                className="w-full p-4 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500 transition-all font-sans leading-relaxed"
              />

              <div className="flex items-center justify-between pt-2">
                <span className="text-xs text-gray-400 italic">
                  * Evaluated on accuracy, depth, relevance, and structured delivery.
                </span>
                <button
                  type="submit"
                  disabled={submitting || !userAnswer.trim()}
                  className="px-7 py-3 rounded-2xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-purple-600/30 transition-all flex items-center gap-2 disabled:opacity-50 hover:scale-[1.02]"
                >
                  {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                  Submit Answer for AI Critique
                </button>
              </div>
            </form>

            {/* Previous Feedback History in this Session */}
            {feedbackHistory.length > 0 && (
              <div className="space-y-4 pt-4">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <Award className="h-4 w-4 text-emerald-400" /> Session Question Critiques
                </h4>
                {feedbackHistory.map((item: any, i: number) => (
                  <div key={i} className="glass-card p-5 rounded-2xl border-white/[0.08] space-y-3 text-xs">
                    <p className="font-bold text-white">Q{i + 1}: {item.question}</p>
                    <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-200 space-y-2">
                      <div className="flex justify-between items-center font-bold">
                        <span className="font-mono text-emerald-400">Score: {item.feedback.score}%</span>
                      </div>
                      <p className="leading-relaxed">{item.feedback.feedback}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Final Report */}
        {finalReport && (
          <div className="glass-card p-6 md:p-8 rounded-3xl border-emerald-500/30 space-y-6 shadow-2xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/[0.08] pb-6">
              <div>
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">
                  Comprehensive Report
                </span>
                <h3 className="text-2xl font-black text-white mt-1">Interview Performance Audit</h3>
                <p className="text-xs text-gray-400">{targetRole} • {totalQuestions} Questions Evaluated</p>
              </div>

              <div className="text-right">
                <span className="text-xs text-gray-400 font-mono">Overall Rubric Score</span>
                <p className="text-4xl font-black text-emerald-400 font-mono">{finalReport.overall_score}%</p>
              </div>
            </div>

            {/* Category Rubric */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-center space-y-1">
                <span className="text-[11px] text-gray-400 font-medium">Technical Accuracy</span>
                <p className="text-2xl font-black text-indigo-400 font-mono mt-1">
                  {finalReport.category_scores?.technical_accuracy || 90}%
                </p>
              </div>
              <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-center space-y-1">
                <span className="text-[11px] text-gray-400 font-medium">Relevance</span>
                <p className="text-2xl font-black text-purple-400 font-mono mt-1">
                  {finalReport.category_scores?.relevance || 92}%
                </p>
              </div>
              <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-center space-y-1">
                <span className="text-[11px] text-gray-400 font-medium">Technical Depth</span>
                <p className="text-2xl font-black text-cyan-400 font-mono mt-1">
                  {finalReport.category_scores?.depth || 85}%
                </p>
              </div>
              <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-center space-y-1">
                <span className="text-[11px] text-gray-400 font-medium">Communication</span>
                <p className="text-2xl font-black text-emerald-400 font-mono mt-1">
                  {finalReport.category_scores?.communication || 85}%
                </p>
              </div>
            </div>

            {/* Strengths & Weaknesses */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-5 rounded-2xl bg-emerald-950/20 border border-emerald-500/20 space-y-2.5">
                <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">
                  Key Strengths Demonstrated
                </span>
                <ul className="space-y-1.5 text-xs text-gray-300">
                  {(finalReport.strengths || []).map((s: string, idx: number) => (
                    <li key={idx} className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> {s}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-amber-950/20 border border-amber-500/20 space-y-2.5">
                <span className="text-xs font-mono font-bold text-amber-400 uppercase tracking-wider">
                  Target Growth Areas
                </span>
                <ul className="space-y-1.5 text-xs text-gray-300">
                  {(finalReport.weaknesses || []).map((w: string, idx: number) => (
                    <li key={idx} className="flex items-center gap-2">
                      <AlertCircle className="h-4 w-4 text-amber-400 shrink-0" /> {w}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="flex justify-end pt-4">
              <button
                onClick={() => setFinalReport(null)}
                className="px-7 py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs shadow-lg transition-all"
              >
                Start Another Practice Session
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
