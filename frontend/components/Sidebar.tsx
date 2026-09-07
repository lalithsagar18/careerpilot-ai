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
  Bot,
  Settings as SettingsIcon,
  Layers,
} from "lucide-react";

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
}

const navItems: NavItem[] = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Resumes", href: "/resumes", icon: FileText },
  { name: "Job Analyzer", href: "/jobs", icon: Briefcase },
  { name: "Job Match & Gaps", href: "/match", icon: GitCompare, badge: "Score" },
  { name: "Learning Roadmap", href: "/learning-plan", icon: GraduationCap },
  { name: "Resume Optimizer", href: "/optimize", icon: Sparkles, badge: "ATS" },
  { name: "Cover Letter Studio", href: "/cover-letter", icon: Mail },
  { name: "Mock Interview AI", href: "/interview", icon: Mic, badge: "Adaptive" },
  { name: "Career Knowledge", href: "/knowledge", icon: FolderSearch, badge: "RAG" },
  { name: "Applications Tracker", href: "/applications", icon: Kanban },
  { name: "Settings & Profile", href: "/settings", icon: SettingsIcon },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-gray-800/80 bg-[#0e1322]/90 backdrop-blur-xl flex flex-col justify-between p-4 min-h-[calc(100vh-4rem)]">
      <div className="space-y-1">
        <div className="px-3 py-2">
          <p className="text-[11px] font-bold uppercase tracking-wider text-gray-400">
            Intelligence Hub
          </p>
        </div>
        <nav className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-indigo-600/15 text-indigo-300 border border-indigo-500/30 font-semibold shadow-sm"
                    : "text-gray-300 hover:text-white hover:bg-gray-800/50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`h-4 w-4 ${isActive ? "text-indigo-400" : "text-gray-400"}`} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[10px] px-1.5 py-0.5 rounded-md font-semibold tracking-wide ${
                      isActive
                        ? "bg-indigo-500/30 text-indigo-200"
                        : "bg-gray-800 text-gray-400 border border-gray-700/50"
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

      {/* Agent & MCP Engine Status Pill */}
      <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-3.5 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-gray-300 flex items-center gap-1.5">
            <Layers className="h-3.5 w-3.5 text-purple-400" />
            Agent Engine
          </span>
          <span className="text-[10px] text-emerald-400 font-mono">10 AGENTS</span>
        </div>
        <p className="text-[11px] text-gray-400 leading-tight">
          Deterministic 6-dim matching + LangGraph orchestrator ready.
        </p>
      </div>
    </aside>
  );
};
