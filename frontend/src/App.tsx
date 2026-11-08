
import {
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  LayoutDashboard,
  ArrowLeftRight,
  ChartNoAxesCombined,
  BrainCircuit,
  Wallet,
  ArrowUpRight,
  ArrowDownRight,
  Plus,
  Bell,
  Search,
  CreditCard,
  ChevronRight,
  LogOut,
  RefreshCw,
  Pencil,
  Trash2,
  Loader2,
} from "lucide-react";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

import Login from "./pages/Login";

import AddTransactionModal from "./components/AddTransactionModal";
import EditTransactionModal from "./components/EditTransactionModal";
import DeleteTransactionModal from "./components/DeleteTransactionModal";

import { getMyProfile } from "./api/auth";

import {
  getTransactions,
  type Transaction,
} from "./api/transactions";

const SESSION_TOKEN_KEY = "finassist_access_token";

interface SpendingAnalysis {
  summary: string;
  top_category: string;
  insights: string[];
  recommendation: string;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8003";

const moneyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

type ActivePage = "Dashboard" | "Transactions" | "Analytics" | "AI Insights";

const pageHeaders: Record<ActivePage, { title: string; subtitle: string }> = {
  Dashboard: {
    title: "Financial Overview",
    subtitle: "Welcome back! Here's your financial snapshot.",
  },
  Transactions: {
    title: "My Transactions",
    subtitle: "View, add, edit, and manage your recorded transactions.",
  },
  Analytics: {
    title: "Financial Analytics",
    subtitle: "Explore your recorded income and expenses over time.",
  },
  "AI Insights": {
    title: "AI Financial Insights",
    subtitle: "Understand your spending with personalized AI analysis.",
  },
};

const navigation = [
  { label: "Dashboard" as const, icon: LayoutDashboard },
  { label: "Transactions" as const, icon: ArrowLeftRight },
  { label: "Analytics" as const, icon: ChartNoAxesCombined },
  { label: "AI Insights" as const, icon: BrainCircuit },
];

// Calculate financial totals using real transactions.
// Records without dates count toward the recorded net balance,
// but are excluded from monthly statistics.
function buildFinancialSummary(transactions: Transaction[]) {
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth();

  const monthlyData = Array.from({ length: 6 }, (_, index) => {
    const date = new Date(
      currentYear,
      currentMonth - (5 - index),
      1
    );

    return {
      key: `${date.getFullYear()}-${date.getMonth()}`,
      month: date.toLocaleString("en-US", {
        month: "short",
      }),
      income: 0,
      expenses: 0,
    };
  });

  let totalIncome = 0;
  let totalExpenses = 0;
  let monthlyIncome = 0;
  let monthlyExpenses = 0;
  let undatedCount = 0;

  for (const transaction of transactions) {
    const amount = Number(transaction.amount);

    if (!Number.isFinite(amount) || amount < 0) {
      continue;
    }

    const isIncome =
      transaction.transaction_type === "income";

    if (isIncome) {
      totalIncome += amount;
    } else {
      totalExpenses += amount;
    }

    if (!transaction.created_at) {
      undatedCount += 1;
      continue;
    }

    const date = new Date(transaction.created_at);

    if (Number.isNaN(date.getTime())) {
      undatedCount += 1;
      continue;
    }

    const year = date.getFullYear();
    const month = date.getMonth();

    if (
      year === currentYear &&
      month === currentMonth
    ) {
      if (isIncome) {
        monthlyIncome += amount;
      } else {
        monthlyExpenses += amount;
      }
    }

    const bucket = monthlyData.find(
      (item) => item.key === `${year}-${month}`
    );

    if (bucket) {
      if (isIncome) {
        bucket.income += amount;
      } else {
        bucket.expenses += amount;
      }
    }
  }

  return {
    totalBalance: totalIncome - totalExpenses,
    monthlyIncome,
    monthlyExpenses,
    monthlyData,
    undatedCount,
  };
}

function App() {
  const [activePage, setActivePage] = useState<ActivePage>("Dashboard");
  const [accessToken, setAccessToken] = useState<
    string | null
  >(() => sessionStorage.getItem(SESSION_TOKEN_KEY));

  const [userId, setUserId] = useState<number | null>(
    null
  );

  const [sessionChecking, setSessionChecking] = useState(
    () => Boolean(sessionStorage.getItem(SESSION_TOKEN_KEY))
  );

  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");

  const [transactions, setTransactions] = useState<
    Transaction[]
  >([]);

  const [transactionsLoading, setTransactionsLoading] =
    useState(false);

  const [transactionsError, setTransactionsError] =
    useState("");

  const [refreshKey, setRefreshKey] = useState(0);

  const [aiAnalysis, setAiAnalysis] = useState<SpendingAnalysis | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  const [showAddTransaction, setShowAddTransaction] =
    useState(false);

  const [editingTransaction, setEditingTransaction] =
    useState<Transaction | null>(null);

  const [deletingTransaction, setDeletingTransaction] =
    useState<Transaction | null>(null);

  const financialSummary = useMemo(
    () => buildFinancialSummary(transactions),
    [transactions]
  );

  // Restore and verify the authenticated session.
  useEffect(() => {
    if (!accessToken) {
      setSessionChecking(false);
      return;
    }

    let cancelled = false;

    async function restoreSession() {
      setSessionChecking(true);

      try {
        const profile = await getMyProfile(accessToken!);

        if (!cancelled) {
          setUserId(profile.user_id);
          setAuthError("");
        }
      } catch {
        if (!cancelled) {
          sessionStorage.removeItem(SESSION_TOKEN_KEY);
          setAccessToken(null);
          setUserId(null);
          setTransactions([]);
          setAuthError(
            "Your session could not be verified. Please sign in again."
          );
        }
      } finally {
        if (!cancelled) {
          setSessionChecking(false);
        }
      }
    }

    restoreSession();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  // Login.
  async function handleLogin(token: string) {
    if (authLoading) return;

    setAuthLoading(true);
    setAuthError("");

    try {
      const profile = await getMyProfile(token);

      sessionStorage.setItem(SESSION_TOKEN_KEY, token);

      setUserId(profile.user_id);
      setAccessToken(token);
    } catch {
      setAuthError(
        "Could not verify your session. Please sign in again."
      );

      sessionStorage.removeItem(SESSION_TOKEN_KEY);
      setAccessToken(null);
      setUserId(null);
    } finally {
      setAuthLoading(false);
    }
  }

  // Logout.
  function handleLogout() {
    sessionStorage.removeItem(SESSION_TOKEN_KEY);

    setShowAddTransaction(false);
    setEditingTransaction(null);
    setDeletingTransaction(null);

    setAccessToken(null);
    setUserId(null);
    setSessionChecking(false);

    setAuthError("");
    setTransactions([]);
    setTransactionsError("");
    setAiAnalysis(null);
    setAiError("");
    setActivePage("Dashboard");
  }

  // Fetch real transactions from FastAPI.
  useEffect(() => {
    if (
      !accessToken ||
      userId === null ||
      sessionChecking
    ) {
      return;
    }

    let cancelled = false;

    async function loadTransactions() {
      setTransactionsLoading(true);
      setTransactionsError("");

      try {
        const data = await getTransactions(accessToken!);

        if (!cancelled) {
          setTransactions(data);
        }
      } catch {
        if (!cancelled) {
          setTransactionsError(
            "Unable to load transactions. Please try again."
          );
        }
      } finally {
        if (!cancelled) {
          setTransactionsLoading(false);
        }
      }
    }

    loadTransactions();

    return () => {
      cancelled = true;
    };
  }, [accessToken, userId, sessionChecking, refreshKey]);

  function refreshTransactions() {
    setAiAnalysis(null);
    setAiError("");
    setRefreshKey((previous) => previous + 1);
  }

  async function handleAnalyzeSpending() {
    if (!accessToken || userId === null || aiLoading) return;

    const requestedToken = accessToken;
    const requestedUserId = userId;
    setAiLoading(true);
    setAiError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/ai/spending-analysis/${requestedUserId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${requestedToken}`,
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("Add a transaction before requesting AI insights.");
        }
        if (response.status === 401 || response.status === 403) {
          throw new Error("Your session is not authorized. Please sign in again.");
        }
        if (response.status === 503) {
          throw new Error("The AI service is temporarily unavailable. Please retry.");
        }
        throw new Error(`Unable to generate AI insights (HTTP ${response.status}).`);
      }

      const result: SpendingAnalysis = await response.json();
      // Do not show an earlier user's analysis after a session change.
      if (sessionStorage.getItem(SESSION_TOKEN_KEY) === requestedToken) {
        setAiAnalysis(result);
      }
    } catch (error) {
      if (sessionStorage.getItem(SESSION_TOKEN_KEY) === requestedToken) {
        setAiError(
          error instanceof Error ? error.message : "Unable to generate AI insights."
        );
      }
    } finally {
      setAiLoading(false);
    }
  }

  function handleTransactionCreated() {
    setShowAddTransaction(false);
    refreshTransactions();
  }

  function handleTransactionUpdated() {
    setEditingTransaction(null);
    refreshTransactions();
  }

  function handleTransactionDeleted() {
    setDeletingTransaction(null);
    refreshTransactions();
  }

  // Loading screen.
  if (sessionChecking) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-slate-50">
        <div className="rounded-2xl bg-emerald-50 p-4">
          <Wallet size={32} className="text-emerald-600" />
        </div>

        <Loader2
          size={24}
          className="animate-spin text-emerald-600"
        />

        <p className="text-sm font-medium text-slate-600">
          Restoring your FinAssist session...
        </p>
      </div>
    );
  }

  // Login screen.
  if (!accessToken || userId === null) {
    return (
      <>
        <Login onLogin={handleLogin} />

        {(authLoading || authError) && (
          <div
            role="status"
            className="fixed bottom-5 right-5 z-50 max-w-sm rounded-xl border border-slate-200 bg-white p-4 text-sm shadow-lg"
          >
            {authLoading
              ? "Verifying your account..."
              : authError}
          </div>
        )}
      </>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 lg:flex">
      {/* Sidebar */}
      <aside className="bg-[#101d32] text-white lg:min-h-screen lg:w-64 lg:shrink-0">
        <div className="flex items-center gap-3 border-b border-white/10 px-6 py-7">
          <div className="rounded-xl bg-emerald-500 p-2">
            <Wallet size={23} />
          </div>

          <div>
            <h1 className="text-xl font-bold">
              FinAssist
            </h1>

            <p className="text-xs text-slate-400">
              AI Financial Platform
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex gap-1 overflow-x-auto px-3 py-4 lg:mt-5 lg:flex-col">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.label}
                type="button"
                onClick={() => setActivePage(item.label)}
                aria-current={activePage === item.label ? "page" : undefined}
                className={`flex shrink-0 items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  activePage === item.label
                    ? "bg-emerald-500 text-white"
                    : "text-slate-300 hover:bg-white/10"
                }`}
              >
                <Icon size={19} />
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Sidebar AI Information */}
        <div className="mx-5 mt-10 hidden rounded-2xl bg-white/10 p-5 lg:block">
          <BrainCircuit
            className="mb-3 text-emerald-400"
            size={28}
          />

          <h3 className="font-semibold">
            Smarter finances
          </h3>

          <p className="mt-2 text-xs leading-5 text-slate-300">
            Get personalized insights powered by artificial
            intelligence.
          </p>
        </div>

        {/* Logout */}
        <div className="px-5 pb-6 lg:mt-10">
          <button
            type="button"
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-300 transition hover:bg-white/10 hover:text-white"
          >
            <LogOut size={19} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="min-w-0 flex-1">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-slate-200 bg-white px-5 py-5 md:px-9">
          <div>
            <h2 className="text-xl font-bold text-slate-900 md:text-2xl">
              {pageHeaders[activePage].title}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              {pageHeaders[activePage].subtitle}
            </p>
          </div>

          <div className="flex items-center gap-4">
            <Search
              className="hidden text-slate-500 sm:block"
              size={20}
            />

            <Bell
              className="text-slate-500"
              size={20}
            />

            <div
              title={`User ID: ${userId}`}
              className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100 font-bold text-emerald-700"
            >
              FA
            </div>
          </div>
        </header>

        <div className="mx-auto max-w-7xl space-y-8 p-5 md:p-9">
          {/* Welcome Section */}
          {(activePage === "Dashboard" || activePage === "Transactions") && (
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm font-medium text-emerald-600">
                YOUR FINANCIAL DASHBOARD
              </p>

              <h2 className="mt-1 text-2xl font-bold text-slate-900">
                Take control of your money
              </h2>
            </div>

            <button
              type="button"
              onClick={() => setShowAddTransaction(true)}
              className="flex items-center gap-2 rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-emerald-600"
            >
              <Plus size={18} />
              Add Transaction
            </button>
          </div>

          )}

          {/* Real Financial Summary Cards */}
          {activePage === "Dashboard" && (
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            <SummaryCard
              title="Total Balance"
              amount={
                transactionsError
                  ? "Unavailable"
                  : transactionsLoading
                  ? "Loading..."
                  : moneyFormatter.format(
                      financialSummary.totalBalance
                    )
              }
              icon={<Wallet size={22} />}
              change="Recorded income minus recorded expenses"
              positive={
                financialSummary.totalBalance >= 0
              }
            />

            <SummaryCard
              title="Monthly Income"
              amount={
                transactionsError
                  ? "Unavailable"
                  : transactionsLoading
                  ? "Loading..."
                  : moneyFormatter.format(
                      financialSummary.monthlyIncome
                    )
              }
              icon={<ArrowDownRight size={22} />}
              change="Income recorded this month"
              positive
            />

            <SummaryCard
              title="Monthly Expenses"
              amount={
                transactionsError
                  ? "Unavailable"
                  : transactionsLoading
                  ? "Loading..."
                  : moneyFormatter.format(
                      financialSummary.monthlyExpenses
                    )
              }
              icon={<ArrowUpRight size={22} />}
              change="Expenses recorded this month"
              positive={false}
            />
          </div>

          )}

          {activePage === "Dashboard" && financialSummary.undatedCount > 0 &&
            !transactionsError &&
            !transactionsLoading && (
              <p className="text-xs text-slate-500">
                {financialSummary.undatedCount} older
                transaction(s) have no recorded date.
                They are included in your total balance,
                but excluded from monthly calculations.
              </p>
            )}

          {/* Analytics and AI Insights: full-width, stacked sections */}
          <div className="space-y-6">
            {/* Spending Analytics Chart */}
            {(activePage === "Dashboard" || activePage === "Analytics") && (
            <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Spending Analytics
                  </h3>

                  <p className="text-sm text-slate-500">
                    Your monthly financial activity
                  </p>
                </div>

                <ChartNoAxesCombined
                  className="text-emerald-500"
                  size={23}
                />
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >
                  <AreaChart
                    data={financialSummary.monthlyData}
                    margin={{
                      top: 10,
                      right: 10,
                      left: -15,
                      bottom: 0,
                    }}
                  >
                    <defs>
                      <linearGradient
                        id="incomeGradient"
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1"
                      >
                        <stop
                          offset="5%"
                          stopColor="#10b981"
                          stopOpacity={0.25}
                        />

                        <stop
                          offset="95%"
                          stopColor="#10b981"
                          stopOpacity={0}
                        />
                      </linearGradient>

                      <linearGradient
                        id="expensesGradient"
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1"
                      >
                        <stop
                          offset="5%"
                          stopColor="#64748b"
                          stopOpacity={0.15}
                        />

                        <stop
                          offset="95%"
                          stopColor="#64748b"
                          stopOpacity={0}
                        />
                      </linearGradient>
                    </defs>

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="#e2e8f0"
                    />

                    <XAxis
                      dataKey="month"
                      tick={{
                        fill: "#64748b",
                        fontSize: 12,
                      }}
                      axisLine={false}
                      tickLine={false}
                    />

                    <YAxis
                      tickFormatter={(value: number) =>
                        `$${value}`
                      }
                      tick={{
                        fill: "#64748b",
                        fontSize: 12,
                      }}
                      axisLine={false}
                      tickLine={false}
                    />

                    <Tooltip
                      formatter={(value) =>
                        moneyFormatter.format(Number(value))
                      }
                    />

                    <Legend />

                    <Area
                      type="monotone"
                      dataKey="income"
                      name="Income"
                      stroke="#10b981"
                      strokeWidth={3}
                      fill="url(#incomeGradient)"
                      activeDot={{ r: 6 }}
                    />

                    <Area
                      type="monotone"
                      dataKey="expenses"
                      name="Expenses"
                      stroke="#64748b"
                      strokeWidth={3}
                      fill="url(#expensesGradient)"
                      activeDot={{ r: 6 }}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <p className="mt-3 text-center text-xs text-slate-400">
                Actual recorded transactions over the last six months
              </p>
            </section>

            )}

            {/* AI Insights Panel */}
            {(activePage === "Dashboard" || activePage === "AI Insights") && (
            <section className="rounded-2xl bg-[#101d32] p-5 text-white shadow-sm sm:p-7">
              <div className="mb-4 flex items-center gap-3">
                <div className="rounded-xl bg-emerald-500/20 p-3">
                  <BrainCircuit
                    className="text-emerald-400"
                    size={24}
                  />
                </div>

                <h3 className="text-lg font-bold">
                  AI Insights
                </h3>
              </div>

              <p className="max-w-3xl text-sm leading-6 text-slate-300">
                Get personalized insights from your recorded income and expenses.
              </p>

              {aiAnalysis ? (
                <div className="mt-5 grid items-start gap-4 md:grid-cols-2" aria-live="polite">
                  <div className="min-w-0 rounded-xl border border-white/10 bg-white/5 p-4 sm:p-5">
                    <p className="text-sm font-semibold text-emerald-300">Financial Summary</p>
                    <p className="mt-2 text-sm leading-6 text-slate-200">{aiAnalysis.summary}</p>
                  </div>
                  <div className="min-w-0 rounded-xl border border-white/10 bg-white/5 p-4 sm:p-5">
                    <p className="text-sm font-semibold text-emerald-300">Top Spending Category</p>
                    <p className="mt-2 text-sm text-white">{aiAnalysis.top_category}</p>
                  </div>
                  <div className="min-w-0 rounded-xl border border-white/10 bg-white/5 p-4 sm:p-5">
                    <p className="text-sm font-semibold text-emerald-300">Key Insights</p>
                    <ul className="mt-2 list-disc space-y-2 pl-5 text-sm leading-6 text-slate-200">
                      {aiAnalysis.insights.map((insight, index) => (
                        <li key={index}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="min-w-0 rounded-xl border border-white/10 bg-white/5 p-4 sm:p-5">
                    <p className="text-sm font-semibold text-emerald-300">Recommendation</p>
                    <p className="mt-2 text-sm leading-6 text-slate-200">{aiAnalysis.recommendation}</p>
                  </div>
                </div>
              ) : (
                <div className="mt-5 max-w-2xl rounded-xl border border-white/10 bg-white/5 p-5">
                  <p className="text-sm font-semibold">Your financial assistant</p>
                  <p className="mt-2 text-xs leading-6 text-slate-300">
                    Analyze transactions, discover spending patterns, and receive actionable recommendations.
                  </p>
                </div>
              )}

              {aiError && (
                <p role="alert" className="mt-4 rounded-lg bg-rose-500/15 p-3 text-sm text-rose-200">
                  {aiError}
                </p>
              )}

              <button
                type="button"
                onClick={handleAnalyzeSpending}
                disabled={aiLoading || transactionsLoading || Boolean(transactionsError) || transactions.length === 0}
                className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 px-6 py-3 text-sm font-semibold transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
              >
                {aiLoading ? (
                  <><Loader2 size={17} className="animate-spin" /> Analyzing...</>
                ) : (
                  <>{aiAnalysis ? "Refresh AI Insights" : "Analyze My Spending"}<ChevronRight size={17} /></>
                )}
              </button>
            </section>
            )}
          </div>

          {/* Recent Transactions: responsive, dated, and clearly labeled */}
          {(activePage === "Dashboard" || activePage === "Transactions") && (
          <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 p-5 sm:p-6">
              <div>
                <h3 className="text-lg font-bold text-slate-900">
                  Recent Transactions
                </h3>
                <p className="mt-1 text-sm text-slate-500">
                  Your recorded income and expenses
                </p>
              </div>

              <button
                type="button"
                onClick={refreshTransactions}
                disabled={transactionsLoading}
                className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold text-emerald-600 transition hover:bg-emerald-50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <RefreshCw
                  size={16}
                  className={transactionsLoading ? "animate-spin" : ""}
                />
                Refresh
              </button>
            </div>

            {transactionsLoading ? (
              <div className="p-10 text-center text-sm text-slate-500">
                Loading your transactions...
              </div>
            ) : transactionsError ? (
              <div role="alert" className="p-10 text-center text-sm text-red-600">
                {transactionsError}
              </div>
            ) : transactions.length === 0 ? (
              <div className="p-10 text-center">
                <CreditCard size={36} className="mx-auto mb-3 text-slate-300" />
                <p className="font-semibold text-slate-700">No transactions yet</p>
                <p className="mt-2 text-sm text-slate-500">
                  Your transactions will appear here once you add them.
                </p>
              </div>
            ) : (
              <div className="divide-y divide-slate-100">
                {transactions.map((transaction) => {
                  const amount = Math.abs(Number(transaction.amount));
                  const isIncome = transaction.transaction_type === "income";
                  const date = transaction.created_at
                    ? new Date(transaction.created_at)
                    : null;
                  const dateLabel = date && !Number.isNaN(date.getTime())
                    ? date.toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                      })
                    : "Date unavailable";

                  return (
                    <div
                      key={transaction.id}
                      className="flex flex-col gap-3 px-4 py-4 transition-colors hover:bg-slate-50/80 sm:flex-row sm:items-center sm:justify-between sm:gap-4 sm:px-6"
                    >
                      <div className="flex min-w-0 items-start gap-3 sm:items-center sm:gap-4">
                        <div
                          className={`shrink-0 rounded-xl p-3 ${
                            isIncome
                              ? "bg-emerald-50 text-emerald-600"
                              : "bg-rose-50 text-rose-600"
                          }`}
                        >
                          {isIncome ? (
                            <ArrowDownRight size={20} />
                          ) : (
                            <ArrowUpRight size={20} />
                          )}
                        </div>

                        <div className="min-w-0">
                          <p className="break-words font-semibold text-slate-800">
                            {transaction.description}
                          </p>
                          <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-slate-500">
                            <span>{transaction.category}</span>
                            <span aria-hidden="true">·</span>
                            <span>{dateLabel}</span>
                            <span
                              className={`rounded-full px-2 py-0.5 font-semibold ${
                                isIncome
                                  ? "bg-emerald-50 text-emerald-700"
                                  : "bg-rose-50 text-rose-700"
                              }`}
                            >
                              {isIncome ? "Income" : "Expense"}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between gap-3 pl-0 sm:shrink-0 sm:justify-end">
                        <p
                          className={`whitespace-nowrap text-base font-bold tabular-nums ${
                            isIncome ? "text-emerald-600" : "text-rose-600"
                          }`}
                        >
                          {isIncome ? "+" : "−"}
                          {moneyFormatter.format(amount)}
                        </p>
                        <div className="flex items-center gap-1">
                          <button
                            type="button"
                            onClick={() => setEditingTransaction(transaction)}
                            aria-label={`Edit ${transaction.description}`}
                            title="Edit transaction"
                            className="rounded-lg p-2.5 text-slate-500 transition hover:bg-emerald-50 hover:text-emerald-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-500"
                          >
                            <Pencil size={17} />
                          </button>
                          <button
                            type="button"
                            onClick={() => setDeletingTransaction(transaction)}
                            aria-label={`Delete ${transaction.description}`}
                            title="Delete transaction"
                            className="rounded-lg p-2.5 text-slate-500 transition hover:bg-rose-50 hover:text-rose-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-rose-500"
                          >
                            <Trash2 size={17} />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          )}

          {/* Add Transaction Modal */}
          {showAddTransaction && (
            <AddTransactionModal
              accessToken={accessToken}
              userId={userId}
              onClose={() =>
                setShowAddTransaction(false)
              }
              onSuccess={handleTransactionCreated}
            />
          )}

          {/* Edit Transaction Modal */}
          {editingTransaction && (
            <EditTransactionModal
              accessToken={accessToken}
              transaction={editingTransaction}
              onClose={() =>
                setEditingTransaction(null)
              }
              onSuccess={handleTransactionUpdated}
            />
          )}

          {/* Delete Transaction Modal */}
          {deletingTransaction && (
            <DeleteTransactionModal
              accessToken={accessToken}
              transaction={deletingTransaction}
              onClose={() =>
                setDeletingTransaction(null)
              }
              onSuccess={handleTransactionDeleted}
            />
          )}

          {/* Footer */}
          <p className="pb-4 text-center text-xs text-slate-400">
            FinAssist-AI · Premium Financial Intelligence Platform
          </p>
        </div>
      </main>
    </div>
  );
}

// Reusable financial summary card.
function SummaryCard({
  title,
  amount,
  icon,
  change,
  positive,
}: {
  title: string;
  amount: string;
  icon: ReactNode;
  change: string;
  positive: boolean;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">
          {title}
        </p>

        <div className="rounded-xl bg-emerald-50 p-3 text-emerald-600">
          {icon}
        </div>
      </div>

      <h3 className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
        {amount}
      </h3>

      <p
        className={`mt-3 text-xs font-medium ${
          positive
            ? "text-emerald-600"
            : "text-rose-500"
        }`}
      >
        {change}
      </p>
    </div>
  );
}

export default App;
