"use client";

import React, { useState } from "react";
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

  const startSession = async () => {
    setLoading(true);
    setFinalReport(null);
    setFeedbackHistory([]);

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
      // Mock active session
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
        // Fetch Final Report
        const report = await ApiClient.getInterviewReport(interviewId);
        setFinalReport(report);
        setSessionActive(false);
      } else {
        // Fetch Next Question
        const nextQ = await ApiClient.getNextQuestion(interviewId);
        setCurrentQuestion(nextQ);
      }
    } catch {
      // Fallback mock feedback
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
          strengths: ["Strong systems grounding", "Crisp communication of ACID vs vector index trade-offs"],
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
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Adaptive Mock Interview AI</h1>
          <p className="text-sm text-gray-400 mt-1">
            Dynamic technical and behavioral interview simulation with real-time rubric scoring and deep constructive feedback.
          </p>
        </div>

        {/* Setup Configuration if not active and no report */}
        {!sessionActive && !finalReport && (
          <div className="glass-card p-6 rounded-2xl border-gray-800 space-y-4 max-w-2xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Mic className="h-4 w-4 text-indigo-400" /> Start New Interview Session
            </h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-gray-400 font-medium">Target Role</label>
                <input
                  type="text"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  placeholder="e.g. Senior Backend AI Engineer"
                  className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-gray-400 font-medium">Interview Type</label>
                  <select
                    value={interviewType}
                    onChange={(e) => setInterviewType(e.target.value)}
                    className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-indigo-500"
                  >
                    <option value="Technical">Technical & Systems</option>
                    <option value="Python & AI">Python & AI Systems</option>
                    <option value="SQL & DB">SQL & Database Architecture</option>
                    <option value="Behavioral">Behavioral & Leadership</option>
                    <option value="System Design">System Design</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-400 font-medium">Number of Questions</label>
                  <select
                    value={totalQuestions}
                    onChange={(e) => setTotalQuestions(Number(e.target.value))}
                    className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-indigo-500"
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
                className="w-full mt-2 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Mic className="h-4 w-4" />}
                Begin Adaptive Mock Interview
              </button>
            </div>
          </div>
        )}

        {/* Active Session Dialogue */}
        {sessionActive && currentQuestion && (
          <div className="space-y-6">
            {/* Progress Header */}
            <div className="glass-card p-4 rounded-xl border-gray-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-xs font-semibold text-white">
                  Question {currentQuestion.order_index} of {totalQuestions}
                </span>
                <span className="text-xs text-indigo-400">({currentQuestion.category})</span>
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-md bg-purple-500/10 text-purple-300 border border-purple-500/20 font-semibold">
                {currentQuestion.difficulty?.toUpperCase()}
              </span>
            </div>

            {/* Question Card */}
            <div className="glass-card p-6 rounded-2xl border-indigo-500/30 space-y-3">
              <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
                <HelpCircle className="h-4 w-4" /> AI Interviewer Question
              </div>
              <p className="text-base font-semibold text-white leading-relaxed">
                {currentQuestion.question_text}
              </p>
            </div>

            {/* Answer Box */}
            <form onSubmit={handleSubmitAnswer} className="glass-card p-6 rounded-2xl border-gray-800 space-y-4">
              <label className="text-xs font-semibold text-gray-300">Your Technical Response</label>
              <textarea
                rows={6}
                required
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Structure your answer with technical clarity, explaining trade-offs, architecture choices, and concrete metrics..."
                className="w-full p-4 rounded-xl bg-gray-900 border border-gray-800 text-white text-sm focus:outline-none focus:border-indigo-500 transition-all"
              />

              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={submitting || !userAnswer.trim()}
                  className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/30 transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                  Submit Answer for AI Critique
                </button>
              </div>
            </form>

            {/* Previous Feedback in this Session */}
            {feedbackHistory.length > 0 && (
              <div className="space-y-4 pt-4">
                <h4 className="text-sm font-bold text-white">Previous Question Critiques</h4>
                {feedbackHistory.map((item: any, i: number) => (
                  <div key={i} className="glass-card p-5 rounded-xl border-gray-800 space-y-2 text-xs">
                    <p className="font-semibold text-white">Q: {item.question}</p>
                    <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-200">
                      <div className="flex justify-between items-center font-bold mb-1">
                        <span>AI Score: {item.feedback.score}%</span>
                      </div>
                      <p>{item.feedback.feedback}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Final Report */}
        {finalReport && (
          <div className="glass-card p-8 rounded-2xl border-emerald-500/30 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">Session Report</span>
                <h3 className="text-2xl font-bold text-white mt-1">Interview Performance Audit</h3>
                <p className="text-xs text-gray-400">{targetRole} • {totalQuestions} Questions Evaluated</p>
              </div>

              <div className="text-right">
                <span className="text-xs text-gray-400">Overall Score</span>
                <p className="text-3xl font-black text-emerald-400">{finalReport.overall_score}%</p>
              </div>
            </div>

            {/* Category Rubric */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3.5 rounded-xl bg-gray-900/60 border border-gray-800 text-center">
                <span className="text-[11px] text-gray-400">Technical Accuracy</span>
                <p className="text-xl font-bold text-indigo-400 mt-1">{finalReport.category_scores?.technical_accuracy || 90}%</p>
              </div>
              <div className="p-3.5 rounded-xl bg-gray-900/60 border border-gray-800 text-center">
                <span className="text-[11px] text-gray-400">Relevance</span>
                <p className="text-xl font-bold text-purple-400 mt-1">{finalReport.category_scores?.relevance || 92}%</p>
              </div>
              <div className="p-3.5 rounded-xl bg-gray-900/60 border border-gray-800 text-center">
                <span className="text-[11px] text-gray-400">Technical Depth</span>
                <p className="text-xl font-bold text-cyan-400 mt-1">{finalReport.category_scores?.depth || 85}%</p>
              </div>
              <div className="p-3.5 rounded-xl bg-gray-900/60 border border-gray-800 text-center">
                <span className="text-[11px] text-gray-400">Communication</span>
                <p className="text-xl font-bold text-emerald-400 mt-1">{finalReport.category_scores?.communication || 85}%</p>
              </div>
            </div>

            {/* Strengths & Weaknesses */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 space-y-2">
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Key Strengths Demonstrated</span>
                <ul className="space-y-1 text-xs text-gray-300">
                  {(finalReport.strengths || []).map((s: string, idx: number) => (
                    <li key={idx} className="flex items-center gap-1.5">
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" /> {s}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/20 space-y-2">
                <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">Target Improvement Topics</span>
                <ul className="space-y-1 text-xs text-gray-300">
                  {(finalReport.weaknesses || []).map((w: string, idx: number) => (
                    <li key={idx} className="flex items-center gap-1.5">
                      <AlertCircle className="h-3.5 w-3.5 text-amber-400" /> {w}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="flex justify-end pt-4">
              <button
                onClick={() => setFinalReport(null)}
                className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all"
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
