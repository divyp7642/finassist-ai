from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from app.database import Base, engine, get_db
from app import models
from sqlalchemy.orm import Session
from app.models import Transaction
from decimal import Decimal

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinAssist AI",
    description="AI-powered financial application platform",
    version="1.0.0"
)

class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)

@app.get("/")
def root():
    return {
        "message": "Welcome to FinAssist AI",
        "status": "running"
    }

@app.post("/transactions", status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = Transaction(
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@app.get("/transactions/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction

    raise HTTPException(
    status_code=404,
    detail="Transaction not found"
)

@app.put("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.description = updated_transaction.description
    transaction.amount = updated_transaction.amount
    transaction.category = updated_transaction.category

    db.commit()
    db.refresh(transaction)

    return transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.get(Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}