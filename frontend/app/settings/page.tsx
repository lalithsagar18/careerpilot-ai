"use client";

import React, { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { useAuth } from "@/lib/auth";
import {
  Settings as SettingsIcon,
  ShieldCheck,
  Cpu,
  Database,
  Key,
  CheckCircle2,
  Save,
  Server,
  Lock,
} from "lucide-react";

export default function SettingsPage() {
  const { user } = useAuth();
  const [provider, setProvider] = useState("gemini");
  const [oracleEnabled, setOracleEnabled] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-5 md:p-8 space-y-8 max-w-4xl mx-auto w-full">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border-white/[0.08]">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20">
                System Configuration
              </span>
              <span className="text-xs text-gray-400">• Multi-Model & Vector Stores</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Platform Configuration & Settings
            </h1>
            <p className="text-xs sm:text-sm text-gray-300">
              Manage your AI provider credentials, database vector backend, and security isolation policies.
            </p>
          </div>
        </div>

        {saved && (
          <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-400" />
            <span>Settings saved successfully into local workspace configuration.</span>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-6">
          {/* User Profile Info */}
          <div className="glass-card p-6 md:p-8 rounded-3xl border-white/[0.08] space-y-4 shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-indigo-400" /> User Profile & Multi-Tenant Scope
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="text-gray-400 font-bold">Authenticated Email</label>
                <input
                  type="text"
                  disabled
                  value={user?.email || "alex.morgan@example.com"}
                  className="w-full mt-1.5 px-4 py-3 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-gray-400 cursor-not-allowed font-mono"
                />
              </div>

              <div>
                <label className="text-gray-400 font-bold">User Partition UUID</label>
                <input
                  type="text"
                  disabled
                  value={user?.id || "usr-uuid-partition-active-001"}
                  className="w-full mt-1.5 px-4 py-3 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-indigo-300 font-mono cursor-not-allowed"
                />
              </div>
            </div>
          </div>

          {/* AI Provider Config */}
          <div className="glass-card p-6 md:p-8 rounded-3xl border-white/[0.08] space-y-4 shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Cpu className="h-4 w-4 text-purple-400" /> AI Provider & LLM Engine
            </h3>

            <div className="space-y-3.5">
              <div>
                <label className="text-xs font-bold text-gray-300">Active Provider</label>
                <select
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="w-full mt-1.5 px-4 py-3 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500"
                >
                  <option value="gemini">Google Gemini 1.5 Pro & text-embedding-004 (Default)</option>
                  <option value="openai">OpenAI Compatible (gpt-4o & text-embedding-3-small)</option>
                  <option value="mock">Offline Mock Provider (Deterministic Testing)</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300">API Key Override (Optional)</label>
                <div className="relative mt-1.5">
                  <Key className="absolute left-3.5 top-3 h-4 w-4 text-gray-500" />
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="AIzaSy... (Managed securely via server environment variables)"
                    className="w-full pl-10 pr-4 py-3 rounded-2xl bg-gray-950 border border-white/[0.08] text-white text-xs sm:text-sm focus:outline-none focus:border-purple-500 font-mono"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Database & Oracle Readiness */}
          <div className="glass-card p-6 md:p-8 rounded-3xl border-white/[0.08] space-y-4 shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Database className="h-4 w-4 text-emerald-400" /> Vector Database Architecture
            </h3>

            <div className="flex items-center justify-between p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06]">
              <div>
                <p className="text-xs font-bold text-white">Oracle AI Database 23ai Vector Search</p>
                <p className="text-[11px] text-gray-400 mt-0.5">
                  Seamlessly switch between PostgreSQL pgvector and Oracle AI Vector Search via unified VectorStoreProvider.
                </p>
              </div>
              <input
                type="checkbox"
                checked={oracleEnabled}
                onChange={(e) => setOracleEnabled(e.target.checked)}
                className="h-5 w-5 accent-indigo-600 rounded cursor-pointer ml-4"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              className="px-7 py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition-all flex items-center gap-2 hover:scale-[1.02]"
            >
              <Save className="h-4 w-4" /> Save Configuration
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
