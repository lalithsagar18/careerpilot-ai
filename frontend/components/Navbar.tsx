"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { Sparkles, LogOut, User as UserIcon, Bell, ChevronRight, Shield } from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-800/80 bg-[#0b0f19]/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-6">
        {/* Brand */}
        <Link href={user ? "/dashboard" : "/"} className="flex items-center gap-3 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform duration-200">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
              CareerPilot <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold">AI</span>
            </span>
          </div>
        </Link>

        {/* Action Controls */}
        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-3">
              <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gray-900/60 border border-gray-800 text-xs text-gray-300">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Oracle & LangGraph Active</span>
              </div>
              <div className="flex items-center gap-3 pl-2 border-l border-gray-800">
                <div className="text-right hidden sm:block">
                  <p className="text-sm font-medium text-white leading-none">{user.full_name || user.email.split("@")[0]}</p>
                  <p className="text-xs text-gray-400 mt-0.5">{user.email}</p>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-gray-800/80 hover:bg-red-500/20 hover:text-red-300 text-gray-300 transition-colors border border-gray-700/60"
                  title="Log out"
                >
                  <LogOut className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                href="/login"
                className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-colors"
              >
                Log In
              </Link>
              <Link
                href="/register"
                className="px-4 py-2 text-sm font-medium rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-md shadow-indigo-600/30 transition-all hover:scale-[1.02]"
              >
                Get Started Free
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
