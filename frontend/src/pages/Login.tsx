
import { useState, type FormEvent } from "react";
import {
  Wallet,
  Mail,
  LockKeyhole,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldCheck,
  ChartNoAxesCombined,
  BrainCircuit,
} from "lucide-react";

import { loginUser } from "../api/auth";

interface LoginProps {
  onLogin: (token: string) => void;
}

export default function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await loginUser({
        email: email.trim(),
        password,
      });

      onLogin(result.access_token);
    } catch {
      setError(
        "Login failed. Please check your email and password."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Login form */}
      <main className="flex min-h-screen flex-col bg-white px-6 py-8 sm:px-12 lg:px-20">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-emerald-500 p-2.5 text-white">
            <Wallet size={25} />
          </div>

          <div>
            <h1 className="text-xl font-bold text-slate-900">
              FinAssist
            </h1>
            <p className="text-xs text-slate-500">
              AI Financial Platform
            </p>
          </div>
        </div>

        <div className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center py-12">
          <p className="mb-3 text-sm font-semibold tracking-wider text-emerald-600 uppercase">
            Welcome back
          </p>

          <h2 className="text-4xl font-bold tracking-tight text-slate-900">
            Sign in to your account
          </h2>

          <p className="mt-4 text-sm leading-6 text-slate-500">
            Access your financial dashboard and AI-powered
            spending insights.
          </p>

          <form onSubmit={handleSubmit} className="mt-10 space-y-6">
            <div>
              <label
                htmlFor="email"
                className="mb-2 block text-sm font-semibold text-slate-700"
              >
                Email address
              </label>

              <div className="relative">
                <Mail
                  size={19}
                  className="absolute top-1/2 left-4 -translate-y-1/2 text-slate-400"
                />

                <input
                  id="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                  className="w-full rounded-xl border border-slate-200 bg-white py-3.5 pr-4 pl-12 text-sm text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-2 block text-sm font-semibold text-slate-700"
              >
                Password
              </label>

              <div className="relative">
                <LockKeyhole
                  size={19}
                  className="absolute top-1/2 left-4 -translate-y-1/2 text-slate-400"
                />

                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  className="w-full rounded-xl border border-slate-200 bg-white py-3.5 pr-12 pl-12 text-sm text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                  className="absolute top-1/2 right-4 -translate-y-1/2 text-slate-400 hover:text-slate-700"
                >
                  {showPassword ? (
                    <EyeOff size={19} />
                  ) : (
                    <Eye size={19} />
                  )}
                </button>
              </div>
            </div>

            {error && (
              <p
                role="alert"
                className="rounded-xl bg-red-50 p-4 text-sm text-red-600"
              >
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 py-4 text-sm font-bold text-white transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Signing in..." : "Sign In"}
              {!loading && <ArrowRight size={18} />}
            </button>
          </form>

          <p className="mt-8 text-center text-xs text-slate-400">
            Your financial data deserves a smarter experience.
          </p>
        </div>

        <p className="text-center text-xs text-slate-400">
          © 2026 FinAssist-AI
        </p>
      </main>

      {/* Decorative information panel */}
      <aside className="relative hidden overflow-hidden bg-[#101d32] px-14 py-16 text-white lg:flex lg:flex-col lg:justify-center">
        <div className="absolute -top-28 -right-28 h-80 w-80 rounded-full bg-emerald-500/15 blur-3xl" />
        <div className="absolute -bottom-28 -left-28 h-80 w-80 rounded-full bg-emerald-500/10 blur-3xl" />

        <div className="relative z-10 mx-auto max-w-lg">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-500/10 px-4 py-2 text-xs font-semibold text-emerald-300">
            <ShieldCheck size={16} />
            Intelligent Financial Management
          </div>

          <h2 className="text-5xl leading-tight font-bold">
            Your money.
            <br />
            <span className="text-emerald-400">
              Smarter decisions.
            </span>
          </h2>

          <p className="mt-6 text-base leading-8 text-slate-300">
            Track transactions, understand spending patterns,
            and discover personalized financial insights
            powered by artificial intelligence.
          </p>

          <div className="mt-12 grid grid-cols-2 gap-4">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <ChartNoAxesCombined
                size={29}
                className="mb-5 text-emerald-400"
              />
              <h3 className="font-semibold">
                Smart Analytics
              </h3>
              <p className="mt-2 text-xs leading-6 text-slate-400">
                Visualize your financial activity.
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <BrainCircuit
                size={29}
                className="mb-5 text-emerald-400"
              />
              <h3 className="font-semibold">
                AI-Powered Insights
              </h3>
              <p className="mt-2 text-xs leading-6 text-slate-400">
                Discover actionable recommendations.
              </p>
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
}
