"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ApiClient } from "@/lib/api";
import {
  Kanban,
  Plus,
  Building2,
  Calendar,
  DollarSign,
  ChevronRight,
  Sparkles,
  Trash2,
  CheckCircle2,
  X,
} from "lucide-react";

const COLUMNS = ["Saved", "Preparing", "Applied", "Interview", "Offer", "Rejected"];

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [company, setCompany] = useState("");
  const [roleTitle, setRoleTitle] = useState("");
  const [status, setStatus] = useState("Saved");
  const [salary, setSalary] = useState("");
  const [notes, setNotes] = useState("");

  const loadApps = async () => {
    try {
      const data = await ApiClient.listApplications();
      setApplications(data);
    } catch {
      // Mock initial applications
      setApplications([
        {
          id: "app-1",
          company: "Stripe",
          role_title: "Senior Software Engineer — Platform",
          status: "Interview",
          salary_offered: "$195,000",
          notes: "Completed initial recruiter screen. Preparing for System Design round.",
        },
        {
          id: "app-2",
          company: "OpenAI",
          role_title: "AI Infrastructure Engineer",
          status: "Applied",
          salary_offered: "$220,000",
          notes: "Submitted tailored ATS-optimized resume v2.",
        },
        {
          id: "app-3",
          company: "NextGen AI Corp",
          role_title: "Senior AI / Backend Engineer",
          status: "Saved",
          salary_offered: "$185,000",
          notes: "Match score calculated deterministically at 87.5%.",
        }
      ]);
    }
  };

  useEffect(() => {
    loadApps();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!company || !roleTitle) return;

    try {
      await ApiClient.createApplication({
        company,
        role_title: roleTitle,
        status,
        salary_offered: salary,
        notes,
      });
      setShowAddModal(false);
      setCompany("");
      setRoleTitle("");
      setSalary("");
      setNotes("");
      await loadApps();
    } catch {
      const newApp = {
        id: `app-${Date.now()}`,
        company,
        role_title: roleTitle,
        status,
        salary_offered: salary,
        notes,
      };
      setApplications([...applications, newApp]);
      setShowAddModal(false);
      setCompany("");
      setRoleTitle("");
      setSalary("");
      setNotes("");
    }
  };

  const updateStatus = async (appId: string, newStatus: string) => {
    try {
      await ApiClient.updateApplication(appId, { status: newStatus });
      await loadApps();
    } catch {
      setApplications(
        applications.map((a) => (a.id === appId ? { ...a, status: newStatus } : a))
      );
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
                Pipeline Tracker
              </span>
              <span className="text-xs text-gray-400">• Interactive Kanban</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Job Applications Tracker
            </h1>
            <p className="text-xs sm:text-sm text-gray-300">
              Kanban pipeline and status tracking for all target roles and AI-optimized applications.
            </p>
          </div>

          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all hover:scale-[1.02]"
          >
            <Plus className="h-4 w-4" /> Add Application
          </button>
        </div>

        {/* Kanban Board Columns */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 overflow-x-auto pb-4">
          {COLUMNS.map((col) => {
            const colApps = applications.filter((a) => a.status === col);
            return (
              <div key={col} className="glass-card p-4 rounded-3xl border-white/[0.08] flex flex-col min-w-[220px] shadow-lg">
                <div className="flex items-center justify-between pb-3 border-b border-white/[0.06] mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-300 font-mono">{col}</span>
                  <span className="text-xs font-bold font-mono px-2 py-0.5 rounded-lg bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                    {colApps.length}
                  </span>
                </div>

                <div className="space-y-3 flex-1">
                  {colApps.map((app) => (
                    <div
                      key={app.id}
                      className="p-4 rounded-2xl bg-gray-950/80 border border-white/[0.08] hover:border-indigo-500/50 transition-all space-y-2.5 text-xs shadow-sm hover:shadow-indigo-500/10"
                    >
                      <p className="font-bold text-white leading-snug">{app.role_title}</p>
                      <p className="text-indigo-400 font-semibold">{app.company}</p>

                      {app.salary_offered && (
                        <span className="inline-block text-[11px] text-emerald-400 font-mono font-bold bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
                          {app.salary_offered}
                        </span>
                      )}

                      {app.notes && (
                        <p className="text-[11px] text-gray-400 line-clamp-2 italic leading-relaxed">{app.notes}</p>
                      )}

                      {/* Status quick select */}
                      <select
                        value={app.status}
                        onChange={(e) => updateStatus(app.id, e.target.value)}
                        className="w-full mt-2 py-1.5 px-2.5 rounded-xl bg-gray-900 border border-white/[0.08] text-[11px] text-gray-300 focus:outline-none focus:border-indigo-500 font-mono"
                      >
                        {COLUMNS.map((c) => (
                          <option key={c} value={c}>Stage: {c}</option>
                        ))}
                      </select>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Add Modal */}
        {showAddModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <div className="w-full max-w-md glass-card p-6 md:p-8 rounded-3xl border-white/[0.1] space-y-4 shadow-2xl">
              <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
                <h3 className="text-base font-bold text-white">Add Job Application</h3>
                <button
                  onClick={() => setShowAddModal(false)}
                  className="text-gray-400 hover:text-white"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <form onSubmit={handleCreate} className="space-y-3.5">
                <div>
                  <label className="text-xs font-bold text-gray-300">Company Name</label>
                  <input
                    type="text"
                    required
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="e.g. Google, Anthropic, Stripe"
                    className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-300">Role Title</label>
                  <input
                    type="text"
                    required
                    value={roleTitle}
                    onChange={(e) => setRoleTitle(e.target.value)}
                    placeholder="e.g. Senior Machine Learning Engineer"
                    className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs font-bold text-gray-300">Pipeline Stage</label>
                    <select
                      value={status}
                      onChange={(e) => setStatus(e.target.value)}
                      className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-indigo-500"
                    >
                      {COLUMNS.map((c) => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-xs font-bold text-gray-300">Target Salary</label>
                    <input
                      type="text"
                      value={salary}
                      onChange={(e) => setSalary(e.target.value)}
                      placeholder="$185,000"
                      className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-300">Notes & Interview Details</label>
                  <textarea
                    rows={3}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Referral contact, recruiter notes, system design dates..."
                    className="w-full mt-1.5 px-4 py-2.5 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-5 py-2.5 rounded-2xl glass-card text-xs font-semibold text-gray-300"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2.5 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md shadow-indigo-600/30"
                  >
                    Save Application
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
