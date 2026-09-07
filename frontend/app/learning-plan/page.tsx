"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  GraduationCap,
  Sparkles,
  CheckCircle2,
  Circle,
  Clock,
  BookOpen,
  Code2,
  MessageSquare,
  ChevronRight,
  TrendingUp,
  Loader2,
} from "lucide-react";

export default function LearningPlanPage() {
  const [plans, setPlans] = useState<any[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await ApiClient.listLearningPlans();
      setPlans(data);
      if (data.length > 0 && !selectedPlan) {
        setSelectedPlan(data[0]);
      }
    } catch {
      // Fallback mock plan
      const mockPlan = {
        id: "plan-1",
        target_role: "Senior AI / Backend Engineer",
        summary: "Structured 4-week fast-track bridging LangGraph stateful agentic workflows, production pgvector indexing, and distributed async pipelines.",
        estimated_weeks: 4,
        completion_percentage: 50.0,
        items: [
          {
            id: "item-1",
            skill_name: "LangGraph Multi-Agent Workflows",
            priority: "critical",
            difficulty: "intermediate",
            objectives: [
              "Master TypedDict state graphs with conditional cyclic routing",
              "Implement Human-in-the-Loop checkpoints and interruptible steps",
              "Build error recovery and retry circuit breaker nodes"
            ],
            resources: ["LangGraph Official Docs & Tutorials", "Agentic Systems Patterns Guide"],
            project_suggestion: "Build a multi-agent code reviewer with automated linter and revision loops.",
            interview_practice_prompt: "Explain how you handle cyclic transitions and infinite loop guards in LangGraph state machines.",
            is_completed: true,
          },
          {
            id: "item-2",
            skill_name: "PostgreSQL pgvector & Oracle AI Vector Search",
            priority: "high",
            difficulty: "advanced",
            objectives: [
              "Configure HNSW cosine distance indexes for sub-millisecond retrieval",
              "Enforce strict tenant/user ownership partition constraints",
              "Implement hybrid chunking and reciprocal rank fusion (RRF)"
            ],
            resources: ["pgvector GitHub Specs", "Oracle 23ai Vector Search Documentation"],
            project_suggestion: "Create a RAG retrieval service with dynamic metadata filtering.",
            interview_practice_prompt: "Compare IVFFlat vs HNSW vector indexing trade-offs for production workloads.",
            is_completed: true,
          },
          {
            id: "item-3",
            skill_name: "Model Context Protocol (MCP) Server Engineering",
            priority: "high",
            difficulty: "intermediate",
            objectives: [
              "Implement JSON-RPC 2.0 tool endpoints",
              "Validate input schemas and sanitize arbitrary shell/SQL vulnerabilities",
              "Integrate rate limiting and telemetry audits"
            ],
            resources: ["Anthropic Model Context Protocol Specs"],
            project_suggestion: "Expose database analytics as typed MCP tools for client IDEs.",
            interview_practice_prompt: "How do you design secure sandboxed tool execution for LLM agents?",
            is_completed: false,
          },
          {
            id: "item-4",
            skill_name: "High-Scale Async FastAPI & Distributed Queues",
            priority: "medium",
            difficulty: "intermediate",
            objectives: [
              "Tune async connection pool sizes and pre-ping health checks",
              "Implement SSE (Server-Sent Events) for real-time LLM token streaming"
            ],
            resources: ["FastAPI Advanced Async Patterns"],
            project_suggestion: "Deploy an async agent gateway with streaming telemetry.",
            interview_practice_prompt: "How does Python asyncio event loop manage blocking I/O tasks versus worker threads?",
            is_completed: false,
          }
        ]
      };
      setPlans([mockPlan]);
      setSelectedPlan(mockPlan);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlans();
  }, []);

  const handleToggle = async (itemId: string) => {
    if (!selectedPlan) return;
    try {
      await ApiClient.toggleLearningItem(itemId);
      await loadPlans();
    } catch {
      // Local optimistic toggle
      const updatedItems = selectedPlan.items.map((it: any) =>
        it.id === itemId ? { ...it, is_completed: !it.is_completed } : it
      );
      const completedCount = updatedItems.filter((it: any) => it.is_completed).length;
      const pct = Math.round((completedCount / updatedItems.length) * 100);
      setSelectedPlan({ ...selectedPlan, items: updatedItems, completion_percentage: pct });
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Personalized Learning Roadmap</h1>
          <p className="text-sm text-gray-400 mt-1">
            Actionable milestone roadmaps, hands-on projects, and interview prompts generated by the Learning Plan Agent.
          </p>
        </div>

        {selectedPlan && (
          <div className="space-y-6">
            {/* Roadmap Header Summary Card */}
            <div className="glass-card p-6 rounded-2xl border-indigo-500/30 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Target Role Curriculum</span>
                  <h3 className="text-xl font-bold text-white mt-0.5">{selectedPlan.target_role}</h3>
                  <p className="text-xs text-gray-400 mt-1 max-w-2xl">{selectedPlan.summary}</p>
                </div>
                <div className="text-right sm:border-l sm:border-gray-800 sm:pl-6">
                  <span className="text-xs text-gray-400">Completion</span>
                  <p className="text-2xl font-extrabold text-emerald-400">{selectedPlan.completion_percentage}%</p>
                  <span className="text-[11px] text-indigo-300 font-medium">Est. {selectedPlan.estimated_weeks} Weeks</span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-gray-900 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${selectedPlan.completion_percentage}%` }}
                ></div>
              </div>
            </div>

            {/* Roadmap Milestone Items */}
            <div className="space-y-4">
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-purple-400" /> Milestone Action Items ({selectedPlan.items?.length || 0})
              </h4>

              <div className="space-y-4">
                {(selectedPlan.items || []).map((item: any, idx: number) => (
                  <div
                    key={item.id || idx}
                    className={`glass-card p-6 rounded-2xl transition-all border ${
                      item.is_completed
                        ? "bg-gray-950/40 border-emerald-500/30 opacity-90"
                        : "border-gray-800"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-3">
                        <button
                          onClick={() => handleToggle(item.id)}
                          className="mt-0.5 text-gray-400 hover:text-emerald-400 transition-colors"
                          title="Toggle completion"
                        >
                          {item.is_completed ? (
                            <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                          ) : (
                            <Circle className="h-5 w-5 text-gray-500 hover:text-gray-300" />
                          )}
                        </button>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className={`text-base font-bold ${item.is_completed ? "line-through text-gray-400" : "text-white"}`}>
                              {item.skill_name}
                            </span>
                            <span className="text-[10px] px-2 py-0.5 rounded-md font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                              {item.priority || "High"}
                            </span>
                            <span className="text-[10px] px-2 py-0.5 rounded-md font-semibold bg-gray-800 text-gray-400">
                              {item.difficulty || "Intermediate"}
                            </span>
                          </div>

                          {/* Objectives */}
                          <div className="mt-3 space-y-1.5">
                            <p className="text-xs font-semibold text-gray-300">Core Objectives:</p>
                            <ul className="space-y-1 text-xs text-gray-400">
                              {(item.objectives || []).map((obj: string, oIdx: number) => (
                                <li key={oIdx} className="flex items-start gap-1.5">
                                  <span className="text-indigo-400 font-bold">•</span>
                                  <span>{obj}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          {/* Project Suggestion & Interview Prompt */}
                          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-gray-800/80">
                            {item.project_suggestion && (
                              <div className="p-3 rounded-xl bg-gray-900/60 border border-gray-800 text-xs">
                                <p className="font-semibold text-indigo-300 flex items-center gap-1.5 mb-1">
                                  <Code2 className="h-3.5 w-3.5" /> Hands-On Project
                                </p>
                                <p className="text-gray-400 leading-relaxed">{item.project_suggestion}</p>
                              </div>
                            )}

                            {item.interview_practice_prompt && (
                              <div className="p-3 rounded-xl bg-gray-900/60 border border-gray-800 text-xs">
                                <p className="font-semibold text-purple-300 flex items-center gap-1.5 mb-1">
                                  <MessageSquare className="h-3.5 w-3.5" /> Interview Practice
                                </p>
                                <p className="text-gray-400 leading-relaxed">{item.interview_practice_prompt}</p>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
