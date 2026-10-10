
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis.exceptions import RedisError
from sqlalchemy.orm import Session

from app.database import get_db
from app.redis_client import redis_client
from app.schemas import TransactionCreate
from app.services import transaction_service


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


# GET ALL TRANSACTIONS
@router.get("")
def get_transactions(db: Session = Depends(get_db)):

    # Step 1: Try fetching transactions from Redis
    try:
        cached_data = redis_client.get("transactions:all")

        if cached_data is not None:
            return json.loads(cached_data)

    except (RedisError, ValueError):
        print("Redis cache unavailable. Using PostgreSQL.")

    # Step 2: Fetch transactions from PostgreSQL
    transactions = transaction_service.get_all_transactions(db)

    # Step 3: Convert transactions to JSON-compatible data
    transaction_data = jsonable_encoder(transactions)

    # Step 4: Try caching the result for 60 seconds
    try:
        redis_client.setex(
            "transactions:all",
            60,
            json.dumps(transaction_data)
        )

    except RedisError:
        print("Redis cache write failed. Continuing without cache.")

    return transaction_data


# CREATE TRANSACTION
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

    # Invalidate cache after successful creation
    try:
        redis_client.delete("transactions:all")

    except RedisError:
        print("Redis cache invalidation failed after creation.")

    return new_transaction


# GET TRANSACTION BY ID
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


# UPDATE TRANSACTION
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

    # Invalidate cache after successful update
    try:
        redis_client.delete("transactions:all")

    except RedisError:
        print("Redis cache invalidation failed after update.")

    return transaction


# DELETE TRANSACTION
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

    # Invalidate cache after successful deletion
    try:
        redis_client.delete("transactions:all")

    except RedisError:
        print("Redis cache invalidation failed after deletion.")

    return {"message": "Transaction deleted successfully"}
