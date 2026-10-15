from fastapi.testclient import TestClient
from app.main import app

from unittest.mock import patch
from unittest.mock import ANY
from types import SimpleNamespace

from app.integrations.openai_client import OpenAIServiceError
from redis.exceptions import RedisError

client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to FinAssist AI"
    }



def test_transaction_not_found():
    with patch(
        "app.routers.transactions.transaction_service.get_transaction_by_id",
        return_value=None
    ) as mock_get_transaction:

        response = client.get("/transactions/999999")

        mock_get_transaction.assert_called_once_with(
            ANY, 999999
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found"
    }


def test_transaction_found():
    fake_transaction = {
        "id": 10,
        "description": "Groceries",
        "amount": 50.0,
        "category": "Food",
        "user_id": 1
    }

    with patch(
        "app.routers.transactions.transaction_service.get_transaction_by_id",
        return_value=fake_transaction
    ) as mock_get_transaction:

        response = client.get("/transactions/10")

        mock_get_transaction.assert_called_once_with(ANY, 10)

    assert response.status_code == 200
    assert response.json() == fake_transaction


def test_invalid_transaction_id():
    with patch(
        "app.routers.transactions.transaction_service.get_transaction_by_id"
    ) as mock_get_transaction:

        response = client.get("/transactions/abc")

        assert response.status_code == 422

        mock_get_transaction.assert_not_called()


def test_create_transaction_invalid_amount():
    transaction_data = {
        "description": "Groceries",
        "amount": -50,
        "category": "Food",
        "user_id": 1
    }

    response = client.post(
        "/transactions",
        json=transaction_data
    )

    assert response.status_code == 422


def test_create_transaction_success():
    transaction_data = {
        "description": "Groceries",
        "amount": 50,
        "category": "Food",
        "user_id": 1
    }
    
    fake_transaction = SimpleNamespace(
    id=20,
    description="Groceries",
    amount=50,
    category="Food",
    user_id=1
    )

    with patch(
        "app.routers.transactions.transaction_service.create_transaction",
        return_value=fake_transaction
    ), patch(
    "app.routers.transactions.redis_client.delete"
    ) as mock_redis_delete, patch(
    "app.routers.transactions.publish_transaction_created"
    ) as mock_kafka_publish:
        response = client.post(
            "/transactions",
            json=transaction_data
        ) 

        mock_redis_delete.assert_called_once_with(
        "transactions:all"
        )

        mock_kafka_publish.assert_called_once_with({
        "transaction_id": 20,
        "user_id": 1,
        "description": "Groceries",
        "amount": 50.0,
        "category": "Food"
        })

    assert response.status_code == 201
    assert response.json() == vars(fake_transaction)


def test_create_transaction_user_not_found():
    transaction_data = {
        "description": "Groceries",
        "amount": 50,
        "category": "Food",
        "user_id": 999999
    }

    with patch(
        "app.routers.transactions.transaction_service.create_transaction",
        return_value=None
    ) as mock_create:

        response = client.post(
            "/transactions",
            json=transaction_data
        )

        mock_create.assert_called_once()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_delete_transaction_not_found():
    with patch(
        "app.routers.transactions.transaction_service.delete_transaction",
        return_value=False
    ) as mock_delete:

        response = client.delete("/transactions/999999")

        mock_delete.assert_called_once_with(
        db=ANY,
        transaction_id=999999
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found"
    }



def test_delete_transaction_success():
    with patch(
        "app.routers.transactions.transaction_service.delete_transaction",
        return_value=True
    ) as mock_delete, patch(
        "app.routers.transactions.redis_client.delete"
    ) as mock_redis_delete:

        response = client.delete("/transactions/10")

        mock_delete.assert_called_once_with(
            db=ANY,
            transaction_id=10
        )

        mock_redis_delete.assert_called_once_with(
            "transactions:all"
        )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Transaction deleted successfully"
    }


def test_update_transaction_not_found():
    transaction_data = {
        "description": "Groceries",
        "amount": 75,
        "category": "Food",
        "user_id": 1
    }

    with patch(
        "app.routers.transactions.transaction_service.update_transaction",
        return_value=(None, "transaction_not_found")
    ) as mock_update:

        response = client.put(
            "/transactions/999999",
            json=transaction_data
        )

        mock_update.assert_called_once_with(
            db=ANY,
            transaction_id=999999,
            description="Groceries",
            amount=75,
            category="Food",
            user_id=1
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found"
    }


def test_update_transaction_user_not_found():
    transaction_data = {
        "description": "Groceries",
        "amount": 75,
        "category": "Food",
        "user_id": 999999
    }

    with patch(
        "app.routers.transactions.transaction_service.update_transaction",
        return_value=(None, "user_not_found")
    ) as mock_update:

        response = client.put(
            "/transactions/10",
            json=transaction_data
        )

        mock_update.assert_called_once_with(
            db=ANY,
            transaction_id=10,
            description="Groceries",
            amount=75,
            category="Food",
            user_id=999999
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_update_transaction_success():
    transaction_data = {
        "description": "Groceries",
        "amount": 75,
        "category": "Food",
        "user_id": 1
    }

    fake_transaction = SimpleNamespace(
        id=10,
        description="Groceries",
        amount=75,
        category="Food",
        user_id=1
    )

    with patch(
        "app.routers.transactions.transaction_service.update_transaction",
        return_value=(fake_transaction, None)
    ) as mock_update, patch(
        "app.routers.transactions.redis_client.delete"
    ) as mock_redis_delete:

        response = client.put(
            "/transactions/10",
            json=transaction_data
        )

        mock_update.assert_called_once_with(
            db=ANY,
            transaction_id=10,
            description="Groceries",
            amount=75,
            category="Food",
            user_id=1
        )

        mock_redis_delete.assert_called_once_with(
            "transactions:all"
        )

    assert response.status_code == 200
    assert response.json() == vars(fake_transaction)


def test_user_not_found():
    with patch(
        "app.routers.users.user_service.get_user_by_id",
        return_value=None
    ) as mock_get_user:

        response = client.get("/users/999999")

        mock_get_user.assert_called_once_with(
            ANY, 999999
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_get_user_success():
    fake_user = {
        "id": 1,
        "name": "John",
        "email": "john@example.com"
    }

    with patch(
        "app.routers.users.user_service.get_user_by_id",
        return_value=fake_user
    ) as mock_get_user:

        response = client.get("/users/1")

        mock_get_user.assert_called_once_with(
            ANY, 1
        )

    assert response.status_code == 200
    assert response.json() == fake_user


def test_create_user_duplicate_email():
    user_data = {
        "name": "John",
        "email": "john@example.com"
    }

    with patch(
        "app.routers.users.user_service.create_user",
        return_value=None
    ) as mock_create_user:

        response = client.post(
            "/users",
            json=user_data
        )

        mock_create_user.assert_called_once_with(
            db=ANY,
            name="John",
            email="john@example.com"
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Email already exists"
    }


def test_create_user_success():
    user_data = {
        "name": "John",
        "email": "john@example.com"
    }

    fake_user = {
        "id": 5,
        "name": "John",
        "email": "john@example.com"
    }

    with patch(
        "app.routers.users.user_service.create_user",
        return_value=fake_user
    ) as mock_create_user:

        response = client.post(
            "/users",
            json=user_data
        )

        mock_create_user.assert_called_once_with(
            db=ANY,
            name="John",
            email="john@example.com"
        )

    assert response.status_code == 201
    assert response.json() == fake_user


def test_update_user_not_found():
    user_data = {
        "name": "John Updated",
        "email": "john@example.com"
    }

    with patch(
        "app.routers.users.user_service.update_user",
        return_value=(None, "user_not_found")
    ) as mock_update_user:

        response = client.put(
            "/users/999999",
            json=user_data
        )

        mock_update_user.assert_called_once_with(
            db=ANY,
            user_id=999999,
            name="John Updated",
            email="john@example.com"
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_update_user_duplicate_email():
    user_data = {
        "name": "John Updated",
        "email": "existing@example.com"
    }

    with patch(
        "app.routers.users.user_service.update_user",
        return_value=(None, "email_exists")
    ) as mock_update_user:

        response = client.put(
            "/users/5",
            json=user_data
        )

        mock_update_user.assert_called_once_with(
            db=ANY,
            user_id=5,
            name="John Updated",
            email="existing@example.com"
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Email already exists"
    }


def test_update_user_success():
    user_data = {
        "name": "John Updated",
        "email": "johnupdated@example.com"
    }

    fake_user = {
        "id": 5,
        "name": "John Updated",
        "email": "johnupdated@example.com"
    }

    with patch(
        "app.routers.users.user_service.update_user",
        return_value=(fake_user, None)
    ) as mock_update_user:

        response = client.put(
            "/users/5",
            json=user_data
        )

        mock_update_user.assert_called_once_with(
            db=ANY,
            user_id=5,
            name="John Updated",
            email="johnupdated@example.com"
        )

    assert response.status_code == 200
    assert response.json() == fake_user


def test_delete_user_not_found():
    with patch(
        "app.routers.users.user_service.delete_user",
        return_value=False
    ) as mock_delete_user:

        response = client.delete("/users/999999")

        mock_delete_user.assert_called_once_with(
            db=ANY,
            user_id=999999
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_delete_user_success():
    with patch(
        "app.routers.users.user_service.delete_user",
        return_value=True
    ) as mock_delete_user:

        response = client.delete("/users/5")

        mock_delete_user.assert_called_once_with(
            db=ANY,
            user_id=5
        )

    assert response.status_code == 200
    assert response.json() == {
        "message": "User deleted successfully"
    }


def test_ai_spending_analysis_success():
    fake_analysis = {
        "summary": "You spent $150 this month.",
        "top_category": "Food",
        "insights": [
            "Food is your highest spending category."
        ],
        "recommendation": "Reduce unnecessary food expenses."
    }

    with patch(
        "app.routers.ai.ai_service.analyze_spending",
        return_value=fake_analysis
    ) as mock_analyze:

        response = client.get(
            "/ai/spending-analysis/1"
        )

        mock_analyze.assert_called_once_with(
            db=ANY,
            user_id=1
        )

    assert response.status_code == 200
    assert response.json() == fake_analysis


def test_ai_user_not_found():
    with patch(
        "app.routers.ai.ai_service.analyze_spending",
        return_value="user_not_found"
    ) as mock_analyze:

        response = client.get(
            "/ai/spending-analysis/999999"
        )

        mock_analyze.assert_called_once_with(
            db=ANY,
            user_id=999999
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_ai_no_transactions():
    with patch(
        "app.routers.ai.ai_service.analyze_spending",
        return_value=None
    ) as mock_analyze:

        response = client.get(
            "/ai/spending-analysis/1"
        )

        mock_analyze.assert_called_once_with(
            db=ANY,
            user_id=1
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No transactions found for this user"
    }


def test_ai_service_unavailable():
    with patch(
        "app.routers.ai.ai_service.analyze_spending",
        side_effect=OpenAIServiceError("OpenAI unavailable")
    ) as mock_analyze:

        response = client.get(
            "/ai/spending-analysis/1"
        )

        mock_analyze.assert_called_once_with(
            db=ANY,
            user_id=1
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "AI service is temporarily unavailable"
    }


def test_create_transaction_redis_failure():
    transaction_data = {
        "description": "Groceries",
        "amount": 50,
        "category": "Food",
        "user_id": 1
    }

    fake_transaction = SimpleNamespace(
        id=30,
        description="Groceries",
        amount=50,
        category="Food",
        user_id=1
    )

    with patch(
        "app.routers.transactions.transaction_service.create_transaction",
        return_value=fake_transaction
    ), patch(
        "app.routers.transactions.redis_client.delete",
        side_effect=RedisError("Redis unavailable")
    ), patch(
        "app.routers.transactions.publish_transaction_created"
    ):
        response = client.post(
            "/transactions",
            json=transaction_data
        )

    assert response.status_code == 201
    assert response.json() == vars(fake_transaction)


def test_create_transaction_kafka_failure():
    transaction_data = {
        "description": "Groceries",
        "amount": 50,
        "category": "Food",
        "user_id": 1
    }

    fake_transaction = SimpleNamespace(
        id=40,
        description="Groceries",
        amount=50,
        category="Food",
        user_id=1
    )

    with patch(
        "app.routers.transactions.transaction_service.create_transaction",
        return_value=fake_transaction
    ), patch(
        "app.routers.transactions.redis_client.delete"
    ), patch(
        "app.routers.transactions.publish_transaction_created",
        side_effect=Exception("Kafka unavailable")
    ) as mock_kafka:

        response = client.post(
            "/transactions",
            json=transaction_data
        )

        mock_kafka.assert_called_once()

    assert response.status_code == 201
    assert response.json() == vars(fake_transaction)
