
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis.exceptions import RedisError
from sqlalchemy.orm import Session

from app.database import get_db
from app.redis_client import redis_client
from app.schemas import TransactionCreate
from app.services import transaction_service
from app.kafka_producer import publish_transaction_created
from app.dependencies import get_current_user_id


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


# GET ALL TRANSACTIONS
@router.get("")
def get_transactions(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    cache_key = f"transactions:user:{user_id}"

    try:
        cached_data = redis_client.get(cache_key)

        if cached_data is not None:
            return json.loads(cached_data)

    except (RedisError, ValueError):
        print("Redis cache unavailable. Using PostgreSQL.")

    transactions = transaction_service.get_transactions_by_user(
        db=db,
        user_id=user_id
    )

    transaction_data = jsonable_encoder(transactions)

    try:
        redis_client.setex(
            cache_key,
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
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    if transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot create transactions for another user"
        )

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

    # Invalidate Redis cache
    try:
        redis_client.delete(
            f"transactions:user:{new_transaction.user_id}"
        )

    except RedisError:
        print("Redis cache invalidation failed after creation.")

    # Publish transaction event to Kafka
    try:
        publish_transaction_created({
            "transaction_id": new_transaction.id,
            "user_id": new_transaction.user_id,
            "description": new_transaction.description,
            "amount": float(new_transaction.amount),
            "category": new_transaction.category
        })

    except Exception as e:
        print(f"Kafka publishing failed: {e}")

    return new_transaction


# GET TRANSACTION BY ID
@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
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

    if transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's transaction"
        )

    return transaction


# UPDATE TRANSACTION
@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Find existing transaction
    existing_transaction = transaction_service.get_transaction_by_id(
        db,
        transaction_id
    )

    if existing_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    # Verify transaction ownership
    if existing_transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update another user's transaction"
        )

    # Prevent ownership changes
    if updated_transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot change transaction ownership"
        )

    old_user_id = existing_transaction.user_id

    # Update transaction
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

    if transaction is None:
        raise HTTPException(
            status_code=500,
            detail="Transaction update failed"
        )

    # Invalidate Redis cache
    try:
        redis_client.delete(
            f"transactions:user:{old_user_id}"
        )

        if transaction.user_id != old_user_id:
            redis_client.delete(
                f"transactions:user:{transaction.user_id}"
            )

    except RedisError:
        print("Redis cache invalidation failed after update.")

    return transaction


# DELETE TRANSACTION
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Find transaction
    transaction = transaction_service.get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    # Verify ownership
    if transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete another user's transaction"
        )

    # Delete transaction
    deleted = transaction_service.delete_transaction(
        db=db,
        transaction_id=transaction_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    # Invalidate Redis cache
    try:
        redis_client.delete(
            f"transactions:user:{user_id}"
        )

    except RedisError:
        print("Redis cache invalidation failed after deletion.")

    return {
        "message": "Transaction deleted successfully"
    }
