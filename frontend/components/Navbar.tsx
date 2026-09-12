"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import {
  Sparkles,
  LogOut,
  User as UserIcon,
  ShieldCheck,
  Cpu,
  Layers,
  Menu,
  X,
  ArrowRight,
} from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/[0.07] bg-[#070913]/85 backdrop-blur-2xl transition-all">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 max-w-7xl mx-auto">
        {/* Brand */}
        <Link href={user ? "/dashboard" : "/"} className="flex items-center gap-3 group">
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 shadow-lg shadow-indigo-500/25 group-hover:scale-105 group-hover:shadow-indigo-500/40 transition-all duration-300">
            <Sparkles className="h-5 w-5 text-white" />
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-400"></span>
            </span>
          </div>
          <div>
            <span className="text-xl font-extrabold tracking-tight text-white flex items-center gap-2">
              CareerPilot{" "}
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-bold tracking-wider">
                AI Agentic
              </span>
            </span>
          </div>
        </Link>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              {/* Agent Engine Status Indicator */}
              <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-indigo-950/40 border border-indigo-500/20 text-xs text-indigo-200">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="font-medium">10 Agents Orchestrated</span>
                <span className="text-indigo-400/60 font-mono text-[11px]">• LangGraph</span>
              </div>

              {/* User Profile Pill */}
              <div className="flex items-center gap-3 pl-2 sm:border-l sm:border-white/[0.08]">
                <div className="text-right hidden sm:block">
                  <p className="text-xs font-semibold text-white leading-none">
                    {user.full_name || user.email.split("@")[0]}
                  </p>
                  <p className="text-[11px] text-gray-400 font-mono mt-0.5">{user.email}</p>
                </div>

                <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-300 text-xs font-bold">
                  {(user.full_name || user.email)[0].toUpperCase()}
                </div>

                <button
                  onClick={logout}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-xl bg-white/[0.05] hover:bg-rose-500/20 hover:text-rose-300 text-gray-300 transition-all border border-white/[0.08] hover:border-rose-500/30"
                  title="Sign out of workspace"
                >
                  <LogOut className="h-3.5 w-3.5" />
                  <span className="hidden md:inline">Logout</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                href="/login"
                className="px-4 py-2 text-xs sm:text-sm font-semibold text-gray-300 hover:text-white transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-4 sm:px-5 py-2 sm:py-2.5 text-xs sm:text-sm font-semibold rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-lg shadow-indigo-600/30 transition-all hover:scale-[1.02] flex items-center gap-1.5"
              >
                Launch Pilot <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
