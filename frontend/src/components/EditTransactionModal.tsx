
import { useState, type FormEvent } from "react";
import { X, Save, Loader2 } from "lucide-react";

import {
  updateTransaction,
  type Transaction,
  type TransactionType,
} from "../api/transactions";

interface EditTransactionModalProps {
  accessToken: string;
  transaction: Transaction;
  onClose: () => void;
  onSuccess: () => void;
}

const expenseCategories = [
  "Food & Drinks",
  "Shopping",
  "Transportation",
  "Bills & Utilities",
  "Entertainment",
  "Health",
  "Other",
];

const incomeCategories = [
  "Salary",
  "Freelance",
  "Business",
  "Investments",
  "Gifts",
  "Other",
];

export default function EditTransactionModal({
  accessToken,
  transaction,
  onClose,
  onSuccess,
}: EditTransactionModalProps) {
  const [transactionType, setTransactionType] =
    useState<TransactionType>(
      transaction.transaction_type ?? "expense"
    );

  const [description, setDescription] = useState(
    transaction.description
  );

  const [amount, setAmount] = useState(
    String(transaction.amount)
  );

  const [category, setCategory] = useState(
    transaction.category
  );

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const categories =
    transactionType === "income"
      ? incomeCategories
      : expenseCategories;

  function handleTypeChange(type: TransactionType) {
    setTransactionType(type);

    setCategory(
      type === "income"
        ? incomeCategories[0]
        : expenseCategories[0]
    );

    setError("");
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const numericAmount = Number(amount);

    if (!description.trim()) {
      setError("Please enter a description.");
      return;
    }

    if (
      !Number.isFinite(numericAmount) ||
      numericAmount <= 0
    ) {
      setError("Amount must be greater than zero.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await updateTransaction(
        accessToken,
        transaction.id,
        {
          description: description.trim(),
          amount: numericAmount,
          category,
          transaction_type: transactionType,
          user_id: transaction.user_id,
        }
      );

      onSuccess();
    } catch {
      setError(
        "Could not update transaction. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      role="presentation"
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="edit-transaction-title"
        className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-3xl bg-white p-6 shadow-2xl md:p-8"
      >
        {/* Header */}
        <div className="mb-7 flex items-start justify-between">
          <div>
            <h2
              id="edit-transaction-title"
              className="text-2xl font-bold text-slate-900"
            >
              Edit Transaction
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Update your income or expense details.
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            aria-label="Close"
            className="rounded-xl p-2 text-slate-500 hover:bg-slate-100 disabled:opacity-50"
          >
            <X size={22} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Transaction Type */}
          <div>
            <p className="mb-2 text-sm font-semibold text-slate-700">
              Transaction Type
            </p>

            <div className="grid grid-cols-2 gap-3 rounded-xl bg-slate-100 p-1">
              <button
                type="button"
                onClick={() => handleTypeChange("expense")}
                disabled={loading}
                aria-pressed={transactionType === "expense"}
                className={`rounded-lg px-4 py-3 text-sm font-semibold transition ${
                  transactionType === "expense"
                    ? "bg-white text-rose-600 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                }`}
              >
                Expense
              </button>

              <button
                type="button"
                onClick={() => handleTypeChange("income")}
                disabled={loading}
                aria-pressed={transactionType === "income"}
                className={`rounded-lg px-4 py-3 text-sm font-semibold transition ${
                  transactionType === "income"
                    ? "bg-white text-emerald-600 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                }`}
              >
                Income
              </button>
            </div>
          </div>

          {/* Description */}
          <div>
            <label
              htmlFor="edit-description"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Description
            </label>

            <input
              id="edit-description"
              type="text"
              required
              maxLength={200}
              value={description}
              onChange={(event) =>
                setDescription(event.target.value)
              }
              className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-emerald-500"
            />
          </div>

          {/* Amount */}
          <div>
            <label
              htmlFor="edit-amount"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Amount ($)
            </label>

            <input
              id="edit-amount"
              type="number"
              min="0.01"
              step="0.01"
              required
              value={amount}
              onChange={(event) =>
                setAmount(event.target.value)
              }
              className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-emerald-500"
            />
          </div>

          {/* Category */}
          <div>
            <label
              htmlFor="edit-category"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Category
            </label>

            <select
              id="edit-category"
              value={category}
              onChange={(event) =>
                setCategory(event.target.value)
              }
              disabled={loading}
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-emerald-500"
            >
              {!categories.includes(category) && (
                <option value={category}>
                  {category}
                </option>
              )}

              {categories.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>

          {/* Error Message */}
          {error && (
            <p
              role="alert"
              className="rounded-xl bg-red-50 p-3 text-sm text-red-600"
            >
              {error}
            </p>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-3">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="flex-1 rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-white hover:bg-emerald-600 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2
                    size={18}
                    className="animate-spin"
                  />
                  Saving...
                </>
              ) : (
                <>
                  <Save size={18} />
                  Save Changes
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
