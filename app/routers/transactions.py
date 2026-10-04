from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TransactionCreate
from app.services import transaction_service


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("")
def get_transactions(db: Session = Depends(get_db)):
    return transaction_service.get_all_transactions(db)


@router.post("", status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = transaction_service.create_transaction(
        db=db,
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category,
        user_id=transaction.user_id
    )

    if new_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return new_transaction


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = transaction_service.get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction, error = transaction_service.update_transaction(
        db=db,
        transaction_id=transaction_id,
        description=updated_transaction.description,
        amount=updated_transaction.amount,
        category=updated_transaction.category,
        user_id=updated_transaction.user_id
    )

    if error == "transaction_not_found":
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    if error == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    deleted = transaction_service.delete_transaction(
        db=db,
        transaction_id=transaction_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {"message": "Transaction deleted successfully"}