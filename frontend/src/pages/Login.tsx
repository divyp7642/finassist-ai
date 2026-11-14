
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
  UserRound,
} from "lucide-react";

import { loginUser, registerUser } from "../api/auth";

interface LoginProps {
  onLogin: (token: string) => void;
}

export default function Login({ onLogin }: LoginProps) {
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function switchMode() {
    setIsRegister(!isRegister);
    setError("");
    setSuccess("");
    setPassword("");
    setConfirmPassword("");
    setShowPassword(false);
    setShowConfirmPassword(false);
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (isRegister) {
      if (!name.trim()) {
        setError("Please enter your full name.");
        return;
      }

      if (password.length < 8) {
        setError(
          "Password must contain at least 8 characters."
        );
        return;
      }

      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }
    }

    setLoading(true);

    try {
      if (isRegister) {
        await registerUser({
          name: name.trim(),
          email: email.trim(),
          password,
        });

        try {
          const result = await loginUser({
            email: email.trim(),
            password,
          });

          onLogin(result.access_token);
        } catch {
          setIsRegister(false);
          setPassword("");
          setConfirmPassword("");
          setSuccess(
            "Account created successfully! Please sign in."
          );
        }
      } else {
        const result = await loginUser({
          email: email.trim(),
          password,
        });

        onLogin(result.access_token);
      }
    } catch (err: unknown) {
      const apiError = err as {
        response?: {
          status?: number;
          data?: {
            detail?: unknown;
          };
        };
      };

      const detail = apiError.response?.data?.detail;
      const status = apiError.response?.status;

      if (status === 429) {
        setError(
          "Too many requests. Please wait and try again."
        );
      } else if (typeof detail === "string") {
        setError(detail);
      } else if (isRegister) {
        setError(
          "Registration failed. Please check your details and try again."
        );
      } else {
        setError(
          "Login failed. Please check your email and password."
        );
      }
    } finally {
      setLoading(false);
    }
  }

  const inputClass =
    "w-full rounded-xl border border-slate-200 bg-white py-3.5 pr-4 pl-12 text-sm text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100";

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Authentication form */}
      <main className="flex min-h-screen flex-col bg-white px-6 py-8 sm:px-12 lg:px-20">
        {/* Logo */}
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
            {isRegister
              ? "Get started"
              : "Welcome back"}
          </p>

          <h2 className="text-4xl font-bold tracking-tight text-slate-900">
            {isRegister
              ? "Create your account"
              : "Sign in to your account"}
          </h2>

          <p className="mt-4 text-sm leading-6 text-slate-500">
            {isRegister
              ? "Start managing your finances with smart analytics and AI-powered insights."
              : "Access your financial dashboard and AI-powered spending insights."}
          </p>

          <form
            onSubmit={handleSubmit}
            className="mt-8 space-y-5"
          >
            {/* Full name — registration only */}
            {isRegister && (
              <div>
                <label
                  htmlFor="name"
                  className="mb-2 block text-sm font-semibold text-slate-700"
                >
                  Full name
                </label>

                <div className="relative">
                  <UserRound
                    size={19}
                    className="absolute top-1/2 left-4 -translate-y-1/2 text-slate-400"
                  />

                  <input
                    id="name"
                    type="text"
                    autoComplete="name"
                    required
                    maxLength={100}
                    value={name}
                    onChange={(event) =>
                      setName(event.target.value)
                    }
                    placeholder="Enter your full name"
                    className={inputClass}
                  />
                </div>
              </div>
            )}

            {/* Email */}
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
                  maxLength={255}
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  placeholder="you@example.com"
                  className={inputClass}
                />
              </div>
            </div>

            {/* Password */}
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
                  type={
                    showPassword ? "text" : "password"
                  }
                  autoComplete={
                    isRegister
                      ? "new-password"
                      : "current-password"
                  }
                  required
                  minLength={isRegister ? 8 : undefined}
                  maxLength={128}
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  placeholder={
                    isRegister
                      ? "At least 8 characters"
                      : "Enter your password"
                  }
                  className={`${inputClass} pr-12`}
                />

                <button
                  type="button"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
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

            {/* Confirm password — registration only */}
            {isRegister && (
              <div>
                <label
                  htmlFor="confirmPassword"
                  className="mb-2 block text-sm font-semibold text-slate-700"
                >
                  Confirm password
                </label>

                <div className="relative">
                  <LockKeyhole
                    size={19}
                    className="absolute top-1/2 left-4 -translate-y-1/2 text-slate-400"
                  />

                  <input
                    id="confirmPassword"
                    type={
                      showConfirmPassword
                        ? "text"
                        : "password"
                    }
                    autoComplete="new-password"
                    required
                    minLength={8}
                    maxLength={128}
                    value={confirmPassword}
                    onChange={(event) =>
                      setConfirmPassword(
                        event.target.value
                      )
                    }
                    placeholder="Confirm your password"
                    className={`${inputClass} pr-12`}
                  />

                  <button
                    type="button"
                    onClick={() =>
                      setShowConfirmPassword(
                        !showConfirmPassword
                      )
                    }
                    aria-label={
                      showConfirmPassword
                        ? "Hide confirm password"
                        : "Show confirm password"
                    }
                    className="absolute top-1/2 right-4 -translate-y-1/2 text-slate-400 hover:text-slate-700"
                  >
                    {showConfirmPassword ? (
                      <EyeOff size={19} />
                    ) : (
                      <Eye size={19} />
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* Error message */}
            {error && (
              <p
                role="alert"
                className="rounded-xl bg-red-50 p-4 text-sm text-red-600"
              >
                {error}
              </p>
            )}

            {/* Success message */}
            {success && (
              <p
                role="status"
                className="rounded-xl bg-emerald-50 p-4 text-sm text-emerald-700"
              >
                {success}
              </p>
            )}

            {/* Submit button */}
            <button
              type="submit"
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 py-4 text-sm font-bold text-white transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading
                ? isRegister
                  ? "Creating account..."
                  : "Signing in..."
                : isRegister
                  ? "Create Account"
                  : "Sign In"}

              {!loading && <ArrowRight size={18} />}
            </button>
          </form>

          {/* Switch between login and registration */}
          <div className="mt-6 text-center text-sm text-slate-500">
            {isRegister
              ? "Already have an account?"
              : "Don't have an account?"}{" "}

            <button
              type="button"
              disabled={loading}
              onClick={switchMode}
              className="font-semibold text-emerald-600 hover:text-emerald-700 hover:underline disabled:opacity-60"
            >
              {isRegister ? "Sign In" : "Sign Up"}
            </button>
          </div>

          <p className="mt-8 text-center text-xs text-slate-400">
            Your financial data deserves a smarter
            experience.
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
            Track transactions, understand spending
            patterns, and discover personalized
            financial insights powered by artificial
            intelligence.
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
