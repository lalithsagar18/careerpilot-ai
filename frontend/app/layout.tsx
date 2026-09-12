import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";
import { Navbar } from "@/components/Navbar";

export const metadata: Metadata = {
  title: "CareerPilot AI — Agentic Career Intelligence & Job Application Platform",
  description:
    "Deterministic match calculations, multi-agent resume optimization, adaptive mock interviews, and RAG knowledge search.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#070913] text-gray-100 antialiased selection:bg-indigo-500/30 selection:text-indigo-200">
        <AuthProvider>
          {/* Ambient cosmic background glow meshes */}
          <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
            <div className="absolute -top-40 left-1/4 h-[500px] w-[500px] rounded-full bg-gradient-to-br from-indigo-600/15 to-purple-600/10 blur-[140px] animate-pulse-slow"></div>
            <div className="absolute top-1/3 -right-40 h-[600px] w-[600px] rounded-full bg-gradient-to-tr from-purple-600/15 via-pink-600/10 to-transparent blur-[160px] animate-pulse-glow"></div>
            <div className="absolute bottom-10 left-1/3 h-[500px] w-[500px] rounded-full bg-gradient-to-r from-emerald-600/10 via-cyan-600/10 to-transparent blur-[140px]"></div>
            <div className="absolute inset-0 bg-[radial-gradient(#ffffff08_1px,transparent_1px)] [background-size:24px_24px] opacity-40"></div>
          </div>

          <div className="relative z-10 flex min-h-screen flex-col">
            <Navbar />
            <main className="flex-1">{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
