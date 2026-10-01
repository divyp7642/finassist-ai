from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="FinAssist AI",
    description="AI-powered financial application platform",
    version="1.0.0"
)

class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)

transactions = []

@app.get("/")
def root():
    return {
        "message": "Welcome to FinAssist AI",
        "status": "running"
    }

@app.post("/transactions", status_code=201)
def create_transaction(transaction: TransactionCreate):
    new_transaction = {
        "id": len(transactions) + 1,
        "description": transaction.description,
        "amount": transaction.amount,
        "category": transaction.category
    }

    transactions.append(new_transaction)
    return new_transaction

@app.get("/transactions")
def get_transactions():
    return transactions

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return transaction

    raise HTTPException(
    status_code=404,
    detail="Transaction not found"
)

@app.put("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate
):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transaction["description"] = updated_transaction.description
            transaction["amount"] = updated_transaction.amount
            transaction["category"] = updated_transaction.category

            return transaction

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)

            return {
                "message": "Transaction deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )
