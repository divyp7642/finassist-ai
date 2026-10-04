from sqlalchemy.orm import Session

from app.repositories import transaction_repository


def get_all_transactions(db: Session):
    return transaction_repository.get_all_transactions(db)


def get_transaction_by_id(
    db: Session,
    transaction_id: int
):
    return transaction_repository.get_transaction_by_id(
        db,
        transaction_id
    )


def create_transaction(
    db: Session,
    description: str,
    amount,
    category: str,
    user_id: int
):
    # Check whether the user exists
    user = transaction_repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return None

    # Create the transaction
    return transaction_repository.create_transaction(
        db=db,
        description=description,
        amount=amount,
        category=category,
        user_id=user_id
    )


def update_transaction(
    db: Session,
    transaction_id: int,
    description: str,
    amount,
    category: str,
    user_id: int
):
    # Check whether the transaction exists
    transaction = transaction_repository.get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:
        return None, "transaction_not_found"

    # Check whether the user exists
    user = transaction_repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return None, "user_not_found"

    # Update the transaction
    updated_transaction = transaction_repository.update_transaction(
        db=db,
        transaction=transaction,
        description=description,
        amount=amount,
        category=category,
        user_id=user_id
    )

    return updated_transaction, None


def delete_transaction(
    db: Session,
    transaction_id: int
):
    # Find the transaction
    transaction = transaction_repository.get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:
        return False

    # Delete the transaction
    transaction_repository.delete_transaction(
        db=db,
        transaction=transaction
    )

    return True