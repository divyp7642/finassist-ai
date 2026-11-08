
import { useState } from "react";
import { Trash2, X, Loader2, AlertTriangle } from "lucide-react";

import {
  deleteTransaction,
  type Transaction,
} from "../api/transactions";

interface DeleteTransactionModalProps {
  accessToken: string;
  transaction: Transaction;
  onClose: () => void;
  onSuccess: () => void;
}

export default function DeleteTransactionModal({
  accessToken,
  transaction,
  onClose,
  onSuccess,
}: DeleteTransactionModalProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleDelete() {
    if (loading) return;

    setLoading(true);
    setError("");

    try {
      await deleteTransaction(accessToken, transaction.id);

      onSuccess();
    } catch {
      setError(
        "Could not delete transaction. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4">
      <div
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="delete-transaction-title"
        aria-describedby="delete-transaction-description"
        className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl md:p-8"
      >
        {/* Header */}
        <div className="mb-6 flex items-start justify-between">
          <div className="rounded-2xl bg-red-50 p-4">
            <AlertTriangle
              size={28}
              className="text-red-600"
            />
          </div>

          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            aria-label="Close"
            className="rounded-xl p-2 text-slate-500 transition hover:bg-slate-100 disabled:opacity-50"
          >
            <X size={22} />
          </button>
        </div>

        {/* Confirmation Message */}
        <h2
          id="delete-transaction-title"
          className="text-2xl font-bold text-slate-900"
        >
          Delete Transaction?
        </h2>

        <p
          id="delete-transaction-description"
          className="mt-3 text-sm leading-6 text-slate-500"
        >
          Are you sure you want to delete{" "}
          <span className="font-semibold text-slate-800">
            {transaction.description}
          </span>
          ? This action cannot be undone.
        </p>

        {/* Transaction Details */}
        <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <p className="text-sm font-semibold text-slate-800">
            {transaction.description}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {transaction.category}
          </p>

          <p className="mt-3 text-lg font-bold text-slate-900">
            ${Number(transaction.amount).toFixed(2)}
          </p>
        </div>

        {/* Error */}
        {error && (
          <p
            role="alert"
            className="mt-5 rounded-xl bg-red-50 p-3 text-sm text-red-600"
          >
            {error}
          </p>
        )}

        {/* Actions */}
        <div className="mt-7 flex gap-3">
          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            className="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:opacity-50"
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={handleDelete}
            disabled={loading}
            className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-red-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2
                  size={18}
                  className="animate-spin"
                />
                Deleting...
              </>
            ) : (
              <>
                <Trash2 size={18} />
                Delete
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
