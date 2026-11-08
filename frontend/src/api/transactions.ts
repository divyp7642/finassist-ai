
import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8001";

// Supported transaction types
export type TransactionType = "income" | "expense";

// Transaction returned by FastAPI
export interface Transaction {
  id: number;
  description: string;
  amount: number;
  category: string;
  transaction_type: TransactionType;

  // ISO 8601 timestamp returned by FastAPI.
  // Older transactions may not have a recorded date.
  created_at: string | null;

  user_id: number;
}

// Data required to create a transaction
export interface CreateTransactionData {
  description: string;
  amount: number;
  category: string;
  user_id: number;
  transaction_type?: TransactionType;
}

// Data required to update a transaction
export interface UpdateTransactionData {
  description: string;
  amount: number;
  category: string;
  user_id: number;
  transaction_type?: TransactionType;
}

// GET /transactions
// Fetch transactions belonging to the logged-in user.
export async function getTransactions(
  accessToken: string
): Promise<Transaction[]> {
  const response = await axios.get<Transaction[]>(
    `${API_BASE_URL}/transactions`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  return response.data;
}

// POST /transactions
// Create a new transaction.
export async function createTransaction(
  accessToken: string,
  transaction: CreateTransactionData
): Promise<Transaction> {
  const response = await axios.post<Transaction>(
    `${API_BASE_URL}/transactions`,
    transaction,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  return response.data;
}

// PUT /transactions/{transaction_id}
// Update an existing transaction.
export async function updateTransaction(
  accessToken: string,
  transactionId: number,
  transaction: UpdateTransactionData
): Promise<Transaction> {
  const response = await axios.put<Transaction>(
    `${API_BASE_URL}/transactions/${transactionId}`,
    transaction,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  return response.data;
}

// DELETE /transactions/{transaction_id}
// Delete an existing transaction.
export async function deleteTransaction(
  accessToken: string,
  transactionId: number
): Promise<void> {
  await axios.delete(
    `${API_BASE_URL}/transactions/${transactionId}`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );
}
