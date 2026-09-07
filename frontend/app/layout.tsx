import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";
import { Navbar } from "@/components/Navbar";

export const metadata: Metadata = {
  title: "CareerPilot AI — Agentic Career Intelligence & Job Application Platform",
  description: "Deterministic match calculations, multi-agent resume optimization, adaptive mock interviews, and RAG knowledge search.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0b0f19] text-gray-100 antialiased selection:bg-indigo-500/30 selection:text-indigo-200">
        <AuthProvider>
          {/* Ambient background glows */}
          <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
            <div className="absolute -top-40 left-1/4 h-96 w-96 rounded-full bg-indigo-600/10 blur-[128px]"></div>
            <div className="absolute top-1/3 -right-40 h-96 w-96 rounded-full bg-purple-600/10 blur-[128px]"></div>
            <div className="absolute bottom-10 left-1/3 h-96 w-96 rounded-full bg-emerald-600/5 blur-[128px]"></div>
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
