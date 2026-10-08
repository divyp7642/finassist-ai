from sqlalchemy.orm import Session

from app.models import Transaction

def get_all_transactions(db: Session):
    return db.query(Transaction).all()

def get_transactions_by_user_id(db: Session, user_id: int):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.get(Transaction, transaction_id)


def create_transaction(
    db: Session,
    description: str,
    amount,
    category: str,
    user_id: int
):
    new_transaction = Transaction(
        description=description,
        amount=amount,
        category=category,
        user_id=user_id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


def update_transaction(
    db: Session,
    transaction: Transaction,
    description: str,
    amount,
    category: str,
    user_id: int
):
    transaction.description = description
    transaction.amount = amount
    transaction.category = category
    transaction.user_id = user_id

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(
    db: Session,
    transaction: Transaction
):
    db.delete(transaction)
    db.commit()