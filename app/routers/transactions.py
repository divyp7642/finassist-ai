
import json
import logging

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

logger = logging.getLogger(__name__)


def serialize_transaction(transaction):
    """Convert a transaction into JSON-compatible data."""
    return jsonable_encoder(transaction)


def invalidate_transaction_cache(user_id: int):
    """Invalidate the cached transaction list for a user."""
    try:
        redis_client.delete(
            f"transactions:user:{user_id}"
        )
    except RedisError:
        logger.warning(
            "Redis cache invalidation failed for user %s",
            user_id
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

    except (RedisError, ValueError, TypeError):
        logger.warning(
            "Redis cache unavailable or invalid. Using PostgreSQL."
        )

    transactions = transaction_service.get_transactions_by_user(
        db=db,
        user_id=user_id
    )

    transaction_data = [
        serialize_transaction(transaction)
        for transaction in transactions
    ]

    try:
        redis_client.setex(
            cache_key,
            60,
            json.dumps(transaction_data)
        )

    except RedisError:
        logger.warning(
            "Redis cache write failed. Continuing without cache."
        )

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
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type
    )

    if new_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    invalidate_transaction_cache(new_transaction.user_id)

    # Publish transaction event to Kafka.
    try:
        publish_transaction_created({
            "transaction_id": new_transaction.id,
            "user_id": new_transaction.user_id,
            "description": new_transaction.description,
            "amount": float(new_transaction.amount),
            "category": new_transaction.category,
            "transaction_type": new_transaction.transaction_type,
            "created_at": (
                new_transaction.created_at.isoformat()
                if new_transaction.created_at is not None
                else None
            )
        })

    except Exception:
        logger.exception(
            "Kafka publishing failed for transaction %s",
            new_transaction.id
        )

    return serialize_transaction(new_transaction)


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

    return serialize_transaction(transaction)


# UPDATE TRANSACTION
@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    existing_transaction = transaction_service.get_transaction_by_id(
        db,
        transaction_id
    )

    if existing_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    if existing_transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update another user's transaction"
        )

    if updated_transaction.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot change transaction ownership"
        )

    old_user_id = existing_transaction.user_id

    transaction, error = transaction_service.update_transaction(
        db=db,
        transaction_id=transaction_id,
        description=updated_transaction.description,
        amount=updated_transaction.amount,
        category=updated_transaction.category,
        user_id=updated_transaction.user_id,
        transaction_type=updated_transaction.transaction_type
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

    invalidate_transaction_cache(old_user_id)

    if transaction.user_id != old_user_id:
        invalidate_transaction_cache(transaction.user_id)

    return serialize_transaction(transaction)


# DELETE TRANSACTION
@router.delete("/{transaction_id}")
def delete_transaction(
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
            detail="You cannot delete another user's transaction"
        )

    deleted = transaction_service.delete_transaction(
        db=db,
        transaction_id=transaction_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    invalidate_transaction_cache(user_id)

    return {
        "message": "Transaction deleted successfully"
    }
