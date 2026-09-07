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
      <div className="flex-1 p-6 md:p-8 space-y-8 max-w-4xl mx-auto">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Platform Configuration & Settings</h1>
          <p className="text-sm text-gray-400 mt-1">
            Manage your AI provider credentials, database vector backend, and security isolation policies.
          </p>
        </div>

        {saved && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-400" />
            <span>Settings saved successfully.</span>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-6">
          {/* User Profile Info */}
          <div className="glass-card p-6 rounded-2xl border-gray-800 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-indigo-400" /> User Profile & Identity
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="text-gray-400">Authenticated Email</label>
                <input
                  type="text"
                  disabled
                  value={user?.email || "alex.morgan@example.com"}
                  className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900/50 border border-gray-800 text-gray-400 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="text-gray-400">User ID Scope</label>
                <input
                  type="text"
                  disabled
                  value={user?.id || "usr-uuid-partition-active"}
                  className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900/50 border border-gray-800 text-gray-400 font-mono cursor-not-allowed"
                />
              </div>
            </div>
          </div>

          {/* AI Provider Config */}
          <div className="glass-card p-6 rounded-2xl border-gray-800 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Cpu className="h-4 w-4 text-purple-400" /> AI LLM Provider Abstraction
            </h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-gray-400">Active Provider</label>
                <select
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="w-full mt-1 px-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-purple-500"
                >
                  <option value="gemini">Google Gemini (gemini-1.5-pro & text-embedding-004)</option>
                  <option value="openai">OpenAI Compatible (gpt-4o)</option>
                  <option value="mock">Offline Mock Provider (Deterministic Testing)</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-gray-400">API Key Override (Optional)</label>
                <div className="relative mt-1">
                  <Key className="absolute left-3.5 top-2.5 h-3.5 w-3.5 text-gray-500" />
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="AIzaSy... (Managed safely via server environment variables)"
                    className="w-full pl-9 pr-3.5 py-2.5 rounded-xl bg-gray-900 border border-gray-800 text-white text-xs focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Database & Oracle Readiness */}
          <div className="glass-card p-6 rounded-2xl border-gray-800 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Database className="h-4 w-4 text-emerald-400" /> Vector Database Architecture
            </h3>

            <div className="flex items-center justify-between p-4 rounded-xl bg-gray-900/60 border border-gray-800">
              <div>
                <p className="text-xs font-semibold text-white">Oracle AI Database 23ai Vector Search</p>
                <p className="text-[11px] text-gray-400 mt-0.5">
                  Seamlessly switch between PostgreSQL pgvector and Oracle AI Vector Search via unified VectorStoreProvider.
                </p>
              </div>
              <input
                type="checkbox"
                checked={oracleEnabled}
                onChange={(e) => setOracleEnabled(e.target.checked)}
                className="h-4 w-4 accent-indigo-600 rounded cursor-pointer"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/30 transition-all flex items-center gap-2"
            >
              <Save className="h-4 w-4" /> Save Configuration
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
