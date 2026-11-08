
from decimal import Decimal

from sqlalchemy.orm import Session

from app.integrations import openai_client
from app.repositories import transaction_repository, user_repository


def analyze_spending(db: Session, user_id: int):
    # Step 1: Verify that the user exists.
    user = user_repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return "user_not_found"

    # Step 2: Retrieve the user's transactions.
    transactions = transaction_repository.get_transactions_by_user_id(
        db,
        user_id
    )

    if not transactions:
        return None

    # Step 3: Separate income from expenses.
    income_transactions = [
        transaction
        for transaction in transactions
        if transaction.transaction_type == "income"
    ]

    expense_transactions = [
        transaction
        for transaction in transactions
        if transaction.transaction_type == "expense"
    ]

    # Step 4: Calculate income and spending independently.
    total_income = sum(
        (
            transaction.amount
            for transaction in income_transactions
        ),
        Decimal("0.00")
    )

    total_spending = sum(
        (
            transaction.amount
            for transaction in expense_transactions
        ),
        Decimal("0.00")
    )

    net_balance = total_income - total_spending

    # Step 5: Calculate spending by expense category.
    category_totals = {}

    for transaction in expense_transactions:
        category = transaction.category
        amount = transaction.amount

        category_totals[category] = (
            category_totals.get(
                category,
                Decimal("0.00")
            ) + amount
        )

    # Step 6: Find the highest expense category.
    if category_totals:
        top_category = max(
            category_totals,
            key=category_totals.get
        )

        top_category_amount = category_totals[
            top_category
        ]
    else:
        top_category = "No expenses"
        top_category_amount = Decimal("0.00")

    # Step 7: Avoid division by zero.
    if total_spending > 0:
        top_category_percentage = (
            top_category_amount / total_spending
        ) * Decimal("100")
    else:
        top_category_percentage = Decimal("0.00")

    # Step 8: Prepare real transaction data for OpenAI.
    transaction_data = [
        {
            "description": transaction.description,
            "amount": str(transaction.amount),
            "category": transaction.category,
            "transaction_type": transaction.transaction_type,
            "created_at": (
                transaction.created_at.isoformat()
                if transaction.created_at is not None
                else None
            )
        }
        for transaction in transactions
    ]

    # Step 9: Preserve the existing OpenAI adapter interface.
    # Income and expenses are now correctly classified in
    # transaction_data. The adapter will be reviewed next
    # to ensure it interprets these fields correctly.
    return openai_client.analyze_spending(
        transaction_data,
        total_spending,
        category_totals,
        top_category,
        top_category_amount,
        top_category_percentage
    )
