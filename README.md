
# FinAssist AI

**AI-Powered Personal Finance Management Backend**

FinAssist AI is a backend application built with Python, FastAPI, PostgreSQL, and the OpenAI API. It allows users to securely manage financial transactions, track spending, and receive AI-generated financial insights.

The project demonstrates RESTful API development, database management, authentication, authorization, AI integration, automated testing, and continuous integration.

## Features

### User Authentication and Security

- User registration and login
- Secure password hashing using Argon2 and pwdlib
- JWT-based authentication using PyJWT
- JWT access tokens with a 30-minute expiration
- Protected API endpoints
- User-specific access controls
- Prevention of unauthorized access to another user's data

### User Management

- Retrieve authenticated user information
- Retrieve user profiles
- Update user information
- Delete user accounts
- User ownership validation

### Transaction Management

- Create financial transactions
- Retrieve transactions
- Retrieve individual transactions by ID
- Update existing transactions
- Delete transactions
- Associate transactions with individual users
- Restrict access to transactions based on authenticated user identity

### AI-Powered Spending Analysis

- Integration with the OpenAI Responses API
- Spending analysis based on stored financial transactions
- Total spending and category-based calculations
- Identification of the highest spending category
- AI-generated spending summaries
- Spending insights and practical recommendations
- Structured AI responses using Pydantic
- OpenAI API timeout, retry, and error handling
- Instructions to treat transaction data as data rather than executable instructions

### Testing and Continuous Integration

- Automated API tests using Pytest
- 28 passing automated tests
- Manual API testing using Swagger UI
- GitHub Actions continuous integration workflow

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Authentication | JWT, PyJWT |
| Password Security | pwdlib, Argon2 |
| AI Integration | OpenAI API |
| Data Validation | Pydantic |
| Testing | Pytest |
| API Documentation | Swagger UI / OpenAPI |
| CI | GitHub Actions |
| Version Control | Git and GitHub |

## Project Architecture

The application follows a layered backend architecture to separate API routing, business logic, database access, and external AI integration.

```text
Client / Swagger UI
        |
        v
FastAPI Routers
        |
        v
Authentication and Authorization
        |
        v
Service Layer
        |
        v
Repository Layer
        |
        v
PostgreSQL Database
```

AI spending analysis also communicates with the OpenAI API through a dedicated client module.

## Project Structure

```text
FinAssist-AI/
|
|-- .github/
|   |-- workflows/
|
|-- alembic/
|   |-- versions/
|
|-- app/
|   |-- routers/
|   |   |-- auth.py
|   |   |-- users.py
|   |   |-- transactions.py
|   |   |-- ai.py
|   |
|   |-- services/
|   |-- repositories/
|   |
|   |-- main.py
|   |-- database.py
|   |-- models.py
|   |-- schemas.py
|   |-- security.py
|   |-- dependencies.py
|   |-- openai_client.py
|
|-- tests/
|   |-- test_api.py
|   |-- test_basic.py
|
|-- .gitignore
|-- alembic.ini
|-- requirements.txt
|-- README.md
```

## Getting Started

### Prerequisites

Make sure you have installed:

- Python
- PostgreSQL
- Git
- An OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/divyp7642/finassist-ai.git
cd finassist-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add the following variables:

```env
DATABASE_URL=postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/YOUR_DB_NAME
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
JWT_SECRET_KEY=YOUR_SECURE_RANDOM_SECRET
```

Replace the placeholders with your own values.

**Environment variables:**

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | API key for OpenAI services |
| `JWT_SECRET_KEY` | Secret used to sign and validate JWT access tokens |

Use a long, cryptographically random JWT secret.

**Security:** Never commit the `.env` file, API keys, database credentials, or JWT secrets to GitHub.

### 5. Run Database Migrations

Make sure PostgreSQL is running and the configured database exists.

Run:

```bash
python -m alembic upgrade head
```

This applies the available database migrations.

### 6. Start the FastAPI Server

Run:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

### 7. Open Swagger UI

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Swagger UI allows you to test the application's endpoints directly from your browser.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate a user and generate a JWT |
| GET | `/auth/me` | Retrieve the authenticated user ID |

### User Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | Retrieve the authenticated user's profile |
| GET | `/users/{user_id}` | Retrieve a user by ID |
| PUT | `/users/{user_id}` | Update user information |
| DELETE | `/users/{user_id}` | Delete a user |

### Transaction Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/transactions` | Retrieve transactions |
| POST | `/transactions` | Create a transaction |
| GET | `/transactions/{transaction_id}` | Retrieve a transaction by ID |
| PUT | `/transactions/{transaction_id}` | Update a transaction |
| DELETE | `/transactions/{transaction_id}` | Delete a transaction |

### AI Spending Analysis

| Method | Endpoint | Description |
|---|---|---|
| GET | `/ai/spending-analysis/{user_id}` | Generate AI-powered spending analysis |

Protected endpoints require a valid JWT access token.

## Authentication Workflow

The application uses JWT-based authentication.

1. A user registers using `/auth/register`.
2. The user's password is hashed using Argon2.
3. The user logs in using `/auth/login`.
4. The backend validates the submitted credentials.
5. The backend generates a signed JWT access token.
6. The client sends the token when accessing protected endpoints.
7. The backend validates the token and identifies the authenticated user.
8. Authorization checks restrict access to the user's own resources.

JWT configuration:

- Algorithm: HS256
- Access token expiration: 30 minutes
- Secret: Loaded from `JWT_SECRET_KEY`

## AI Spending Analysis Workflow

The AI spending analysis feature combines deterministic financial calculations with AI-generated explanations.

1. An authenticated user requests spending analysis.
2. The backend validates the user's identity.
3. The application retrieves the user's transactions from PostgreSQL.
4. The service layer calculates spending totals and category summaries.
5. The calculated information is passed to the OpenAI client.
6. The OpenAI Responses API generates a structured analysis.
7. The backend returns the analysis to the client.

The AI model is instructed to use the application's financial calculations as authoritative rather than recalculating them.

Transaction descriptions are treated as untrusted data, reducing the risk of prompt injection.

## Automated Testing

The project uses Pytest for automated backend testing.

Run all tests:

```bash
python -m pytest -v
```

Current test status:

**28 automated tests passing.**

The project also underwent manual testing through Swagger UI, including:

- User registration and login
- JWT authentication
- User profile access
- Transaction creation, retrieval, updating, and deletion
- Transaction ownership validation
- AI spending analysis
- Unauthorized access prevention

## Continuous Integration

The project includes a GitHub Actions workflow that runs automated tests.

The workflow helps identify problems introduced by code changes and verifies that the application remains compatible with its declared dependencies.

Latest verified CI status during development: **Passing**.

## Security Features

The backend implements several security controls:

- Argon2 password hashing
- JWT token authentication
- Token expiration validation
- Protected API routes
- User ownership checks
- Authorization restrictions for financial transactions
- Environment-based secret configuration
- Error handling for invalid or expired tokens
- Separation of application logic and database access

These controls provide a foundation for application security. Additional security testing and production hardening are recommended before deployment.

## Project Status

The following backend capabilities have been implemented and tested locally:

- RESTful API development
- PostgreSQL database integration
- SQLAlchemy models and repositories
- Alembic database migrations
- User authentication and authorization
- JWT-based endpoint protection
- Transaction CRUD operations
- AI-powered spending analysis
- Automated testing
- GitHub Actions continuous integration

The application currently runs in a local development environment.

Production deployment has not yet been completed.

## Future Improvements

Planned improvements include:

- Docker containerization
- Cloud deployment
- Frontend financial dashboard
- Expanded financial analytics
- Additional automated integration and security tests
- Application monitoring and logging
- Performance optimization
- Improved production configuration and deployment automation

## Author

**Divykumar Patel**

M.S. Computer Science  
Loyola Marymount University

GitHub: https://github.com/divyp7642

## License

No license has been specified for this repository.
