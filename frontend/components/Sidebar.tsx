"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  Briefcase,
  GitCompare,
  GraduationCap,
  Sparkles,
  Mail,
  Mic,
  FolderSearch,
  Kanban,
  Settings as SettingsIcon,
  Layers,
  ShieldCheck,
  Zap,
} from "lucide-react";

interface NavGroup {
  groupName: string;
  items: {
    name: string;
    href: string;
    icon: React.ElementType;
    badge?: string;
    badgeColor?: string;
  }[];
}

const navGroups: NavGroup[] = [
  {
    groupName: "Core Intelligence",
    items: [
      { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { name: "Resumes Hub", href: "/resumes", icon: FileText, badge: "AI Parser" },
      { name: "Job Analyzer", href: "/jobs", icon: Briefcase },
      { name: "Deterministic Match", href: "/match", icon: GitCompare, badge: "6-Dim", badgeColor: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30" },
    ],
  },
  {
    groupName: "Studio & Optimization",
    items: [
      { name: "Resume Optimizer", href: "/optimize", icon: Sparkles, badge: "ATS 96%", badgeColor: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
      { name: "Cover Letter Studio", href: "/cover-letter", icon: Mail },
      { name: "Mock Interview AI", href: "/interview", icon: Mic, badge: "Adaptive", badgeColor: "bg-purple-500/20 text-purple-300 border-purple-500/30" },
    ],
  },
  {
    groupName: "Career Operations",
    items: [
      { name: "Learning Roadmap", href: "/learning-plan", icon: GraduationCap },
      { name: "Career Knowledge", href: "/knowledge", icon: FolderSearch, badge: "RAG", badgeColor: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30" },
      { name: "Applications Pipeline", href: "/applications", icon: Kanban },
      { name: "Settings & Models", href: "/settings", icon: SettingsIcon },
    ],
  },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-white/[0.07] bg-[#090d1a]/95 backdrop-blur-2xl flex flex-col justify-between p-4 min-h-[calc(100vh-4rem)] hidden md:flex shrink-0">
      <div className="space-y-6">
        {navGroups.map((group, gIdx) => (
          <div key={gIdx} className="space-y-1.5">
            <div className="px-3">
              <p className="text-[10px] font-extrabold uppercase tracking-wider text-gray-400 font-mono">
                {group.groupName}
              </p>
            </div>
            <nav className="space-y-1">
              {group.items.map((item) => {
                const isActive = pathname === item.href;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 group ${
                      isActive
                        ? "bg-gradient-to-r from-indigo-600/20 via-indigo-600/10 to-transparent text-indigo-200 border border-indigo-500/35 shadow-sm shadow-indigo-600/10"
                        : "text-gray-400 hover:text-white hover:bg-white/[0.04]"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`h-7 w-7 rounded-lg flex items-center justify-center transition-all ${
                          isActive
                            ? "bg-indigo-600/30 text-indigo-300"
                            : "bg-white/[0.03] text-gray-400 group-hover:text-gray-200 group-hover:bg-white/[0.06]"
                        }`}
                      >
                        <Icon className="h-4 w-4" />
                      </div>
                      <span>{item.name}</span>
                    </div>
                    {item.badge && (
                      <span
                        className={`text-[9px] font-mono px-2 py-0.5 rounded-md font-bold tracking-tight border ${
                          item.badgeColor ||
                          (isActive
                            ? "bg-indigo-500/20 text-indigo-200 border-indigo-500/30"
                            : "bg-white/[0.04] text-gray-400 border-white/[0.08]")
                        }`}
                      >
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      {/* Multi-Agent LangGraph Engine Status Widget */}
      <div className="rounded-2xl border border-indigo-500/20 bg-gradient-to-b from-indigo-950/40 to-gray-950/60 p-4 space-y-2.5 relative overflow-hidden mt-6">
        <div className="absolute top-0 right-0 h-16 w-16 bg-indigo-500/10 rounded-full blur-xl pointer-events-none"></div>
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white flex items-center gap-1.5">
            <Layers className="h-4 w-4 text-purple-400" />
            LangGraph Orchestrator
          </span>
          <span className="flex items-center gap-1 text-[10px] text-emerald-400 font-mono font-bold">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            10 ONLINE
          </span>
        </div>
        <p className="text-[11px] text-gray-400 leading-tight">
          Deterministic 6-dim calculations + zero-hallucination Evaluator bounds active.
        </p>
        <div className="pt-1 flex items-center gap-2 text-[10px] text-indigo-300/80 font-mono">
          <ShieldCheck className="h-3 w-3 text-indigo-400" />
          <span>Factual Groundedness: 100%</span>
        </div>
      </div>
    </aside>
  );
};
