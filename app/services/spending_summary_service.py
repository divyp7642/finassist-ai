
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from app.database import SessionLocal
from app.models import Transaction, SpendingSummary


def process_transaction_spending(event):
    """
    Update the spending summary when a Kafka
    transaction.created event is received.
    """

    # Step 1: Extract transaction data from the event
    transaction_data = event.get("data", event)
    transaction_id = transaction_data.get("transaction_id")

    if transaction_id is None:
        raise ValueError("Transaction ID is missing from Kafka event")

    # Step 2: Create a PostgreSQL database session
    with SessionLocal() as db:

        # Step 3: Find the transaction in PostgreSQL
        transaction = db.get(Transaction, transaction_id)

        if transaction is None:
            raise ValueError(
                f"Transaction {transaction_id} does not exist"
            )

        user_id = transaction.user_id
        category = transaction.category

        # Step 4: Calculate the current spending total
        # directly from saved transactions
        statement = select(
            func.sum(Transaction.amount),
            func.count(Transaction.id)
        ).where(
            Transaction.user_id == user_id,
            Transaction.category == category
        )

        total_amount, transaction_count = db.execute(
            statement
        ).one()

        # Step 5: Insert or update the spending summary
        insert_statement = insert(SpendingSummary).values(
            user_id=user_id,
            category=category,
            total_amount=total_amount,
            transaction_count=transaction_count
        )

        update_statement = insert_statement.on_conflict_do_update(
            constraint="uq_spending_summary_user_category",
            set_={
                "total_amount": insert_statement.excluded.total_amount,
                "transaction_count": insert_statement.excluded.transaction_count
            }
        )

        db.execute(update_statement)

        # Step 6: Save the changes
        db.commit()

        print(
            f"Spending summary updated: "
            f"user={user_id}, "
            f"category={category}, "
            f"total={total_amount}, "
            f"transactions={transaction_count}",
            flush=True
        )
