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
          notes: "Match score calculated at 87.5%.",
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
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Job Applications Tracker</h1>
            <p className="text-sm text-gray-400 mt-1">
              Kanban pipeline and status tracking for all target roles and AI-optimized applications.
            </p>
          </div>

          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition-all"
          >
            <Plus className="h-4 w-4" /> Add Application
          </button>
        </div>

        {/* Kanban Board Columns */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 overflow-x-auto pb-4">
          {COLUMNS.map((col) => {
            const colApps = applications.filter((a) => a.status === col);
            return (
              <div key={col} className="glass-card p-4 rounded-2xl border-gray-800 flex flex-col min-w-[200px]">
                <div className="flex items-center justify-between pb-3 border-b border-gray-800 mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-300">{col}</span>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-gray-900 text-indigo-400 border border-gray-800">
                    {colApps.length}
                  </span>
                </div>

                <div className="space-y-3 flex-1">
                  {colApps.map((app) => (
                    <div
                      key={app.id}
                      className="p-3.5 rounded-xl bg-gray-900/80 border border-gray-800 hover:border-indigo-500/50 transition-all space-y-2 text-xs"
                    >
                      <p className="font-semibold text-white leading-tight">{app.role_title}</p>
                      <p className="text-indigo-400 font-medium">{app.company}</p>

                      {app.salary_offered && (
                        <span className="inline-block text-[11px] text-emerald-400 font-mono">
                          {app.salary_offered}
                        </span>
                      )}

                      {app.notes && (
                        <p className="text-[11px] text-gray-400 line-clamp-2 italic">{app.notes}</p>
                      )}

                      {/* Status quick select */}
                      <select
                        value={app.status}
                        onChange={(e) => updateStatus(app.id, e.target.value)}
                        className="w-full mt-2 py-1 px-2 rounded-lg bg-gray-950 border border-gray-800 text-[10px] text-gray-300 focus:outline-none"
                      >
                        {COLUMNS.map((c) => (
                          <option key={c} value={c}>Move to {c}</option>
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
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="w-full max-w-md glass-card p-6 rounded-2xl border-gray-800 space-y-4 shadow-2xl">
              <h3 className="text-base font-bold text-white">Add Job Application</h3>
              <form onSubmit={handleCreate} className="space-y-3">
                <div>
                  <label className="text-xs text-gray-400 font-medium">Company</label>
                  <input
                    type="text"
                    required
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="e.g. Google, Anthropic"
                    className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs"
                  />
                </div>
                <div>
                  <label className="text-xs text-gray-400 font-medium">Role Title</label>
                  <input
                    type="text"
                    required
                    value={roleTitle}
                    onChange={(e) => setRoleTitle(e.target.value)}
                    placeholder="e.g. Senior Machine Learning Engineer"
                    className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-gray-400 font-medium">Pipeline Status</label>
                    <select
                      value={status}
                      onChange={(e) => setStatus(e.target.value)}
                      className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs"
                    >
                      {COLUMNS.map((c) => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-gray-400 font-medium">Target Salary</label>
                    <input
                      type="text"
                      value={salary}
                      onChange={(e) => setSalary(e.target.value)}
                      placeholder="$180,000"
                      className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-gray-400 font-medium">Notes</label>
                  <textarea
                    rows={3}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Referrals, recruiter contacts, interview dates..."
                    className="w-full mt-1 px-3 py-2 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-4 py-2 rounded-xl glass-card text-xs text-gray-300"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/30"
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
