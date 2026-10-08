from sqlalchemy.orm import Session

from app.integrations import openai_client
from app.repositories import transaction_repository, user_repository


def analyze_spending(db: Session, user_id: int):
    # Check whether the user exists
    user = user_repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return "user_not_found"

    # Get all transactions for this user
    transactions = transaction_repository.get_transactions_by_user_id(
        db,
        user_id
    )

    # User exists, but has no transactions
    if not transactions:
        return None

    # Calculate total spending
    total_spending = sum(
        transaction.amount
        for transaction in transactions
    )

    # Calculate spending for each category
    category_totals = {}

    for transaction in transactions:
        category = transaction.category
        amount = transaction.amount

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    # Find the category with the highest spending
    top_category = max(
        category_totals,
        key=category_totals.get
    )

    # Get the amount spent in the top category
    top_category_amount = category_totals[top_category]

    # Calculate the percentage spent in the top category
    top_category_percentage = (
        top_category_amount / total_spending
    ) * 100

    # Prepare only the transaction information needed by OpenAI
    transaction_data = [
        {
            "description": transaction.description,
            "amount": str(transaction.amount),
            "category": transaction.category
        }
        for transaction in transactions
    ]

    # Call the OpenAI adapter and return its result
    return openai_client.analyze_spending(
        transaction_data,
        total_spending,
        category_totals,
        top_category,
        top_category_amount,
        top_category_percentage
    )