import Link from "next/link";
import { Pill, Activity, Heart, ArrowRight, ShieldCheck } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#050505] text-white overflow-hidden selection:bg-indigo-500/30">
      {/* Animated Background Gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[25%] -left-[10%] w-[70%] h-[70%] rounded-full bg-indigo-500/10 blur-[120px] animate-pulse" />
        <div className="absolute -bottom-[25%] -right-[10%] w-[60%] h-[60%] rounded-full bg-violet-600/10 blur-[120px] animate-pulse delay-700" />
      </div>

      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-8 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-10 h-10 bg-gradient-to-tr from-indigo-500 to-violet-500 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform">
            <Pill className="text-white w-6 h-6" />
          </div>
          <span className="text-2xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
            CARA
          </span>
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-400">
          <a href="#features" className="hover:text-white transition-colors">Features</a>
          <a href="#mascot" className="hover:text-white transition-colors">Dosi</a>
          <a href="#security" className="hover:text-white transition-colors">Security</a>
        </div>

        <Link 
          href="/dashboard"
          className="px-6 py-2.5 bg-white text-black text-sm font-semibold rounded-full hover:bg-zinc-200 transition-colors shadow-xl shadow-white/10"
        >
          Open App
        </Link>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 pt-20 pb-32 px-8 max-w-7xl mx-auto flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-xs font-medium text-zinc-400 mb-8 animate-fade-in">
          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
          Powered by Llama 4 Scout
        </div>

        <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-8 leading-[0.9] max-w-4xl">
          Medication adherence,{" "}
          <span className="bg-clip-text text-transparent bg-gradient-to-b from-indigo-400 to-violet-600">
            reimagined.
          </span>
        </h1>

        <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mb-12 leading-relaxed">
          The first context-aware adherence ecosystem that understands your routine, 
          detects recovery patterns, and keeps you healthy through empathetic AI.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 items-center">
          <Link 
            href="/dashboard"
            className="group px-8 py-4 bg-indigo-600 text-white font-semibold rounded-2xl flex items-center gap-2 hover:bg-indigo-500 transition-all shadow-2xl shadow-indigo-500/25 active:scale-95"
          >
            Go to Dashboard
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <button className="px-8 py-4 bg-transparent border border-zinc-800 text-zinc-300 font-semibold rounded-2xl hover:bg-zinc-900 transition-all">
            How it works
          </button>
        </div>

        {/* Feature Grid */}
        <div id="features" className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-32 w-full text-left">
          <div className="p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-sm hover:border-indigo-500/50 transition-colors group">
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Activity className="text-indigo-400 w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-3">Recovery Analytics</h3>
            <p className="text-zinc-500 leading-relaxed text-sm">
              Advanced tracking that correlates medication adherence with your actual recovery milestones.
            </p>
          </div>

          <div className="p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-sm hover:border-violet-500/50 transition-colors group">
            <div className="w-12 h-12 rounded-2xl bg-violet-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Heart className="text-violet-400 w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-3">Dosi Companion</h3>
            <p className="text-zinc-500 leading-relaxed text-sm">
              An empathetic AI coach powered by Groq Llama 4 for lightning-fast, privacy-first conversations.
            </p>
          </div>

          <div className="p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-sm hover:border-emerald-500/50 transition-colors group">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <ShieldCheck className="text-emerald-400 w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-3">HIPAA Ready</h3>
            <p className="text-zinc-500 leading-relaxed text-sm">
              End-to-end encryption and contextual privacy rules that never name your medications in plain text.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-zinc-900 py-12 px-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="text-zinc-500 text-sm font-medium">
            © 2026 CARA Health. Built for the future of care.
          </div>
          <div className="flex gap-8 text-zinc-500 text-sm font-medium">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
