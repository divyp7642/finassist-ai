
# FinAssist AI

### AI-Powered Personal Finance Management Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

## Live Application

**Website:** [https://finassist-ai.duckdns.org](https://finassist-ai.duckdns.org)

FinAssist AI is deployed on Amazon EC2 and accessible through a secure HTTPS connection.

The application provides an interactive financial dashboard, transaction management, spending analytics, and personalized AI-generated financial insights.

> This project is an independently developed portfolio application designed to demonstrate full-stack software engineering, backend system design, event-driven architecture, AI integration, containerization, and cloud deployment.

## Overview

FinAssist AI is a full-stack personal finance management platform that helps users record income and expenses, monitor financial activity, analyze spending patterns, and receive personalized financial recommendations.

The application combines a React frontend with a FastAPI backend, PostgreSQL persistence, Redis caching, Apache Kafka event processing, and the OpenAI API.

It follows a layered backend architecture with clearly separated API, service, repository, and integration components.

The project also demonstrates practical DevOps engineering through Docker, Kubernetes, GitHub Actions, and AWS deployment.

## Key Features

### Financial Dashboard

- Interactive financial overview
- Total balance calculated from recorded income and expenses
- Monthly income and expense summaries
- Financial activity visualization
- Historical spending and income charts
- Responsive dashboard interface

### Authentication and Authorization

- User registration and login APIs
- Secure password hashing using Argon2 and pwdlib
- JWT-based authentication using PyJWT
- JWT access tokens with a 30-minute expiration
- Protected API endpoints
- User-specific resource ownership validation
- Authorization checks for financial data access

### Transaction Management

- Create income and expense transactions
- Retrieve recorded transactions
- Retrieve individual transactions by ID
- Edit existing transactions
- Delete transactions
- Categorize financial transactions
- Associate transactions with authenticated users
- Update financial dashboard totals using recorded data

### Financial Analytics

- Monthly income and expense tracking
- Historical financial activity visualization
- Category-based spending analysis
- Identification of spending patterns
- Financial balance calculations based on stored transactions

### AI-Powered Financial Insights

- Integration with the OpenAI Responses API
- Personalized financial analysis based on recorded transactions
- Financial summaries
- Identification of the highest spending category
- AI-generated spending insights
- Practical financial recommendations
- Structured AI responses using Pydantic
- OpenAI timeout, retry, and error handling
- Instructions that treat transaction descriptions as untrusted data

The AI integration uses application-calculated financial values as authoritative inputs to reduce inconsistencies in generated financial summaries.

### Redis Caching

- Cache-aside caching strategy
- Reduced repetitive database queries
- Configurable cache expiration
- Cache invalidation following transaction mutations
- Redis integration with the backend service layer

### Event-Driven Processing

- Apache Kafka integration
- Transaction-created event publishing
- Dedicated Kafka producer
- Independent Kafka consumer
- Asynchronous event processing
- Separation of transaction operations from event consumption

### Cloud Deployment

- Amazon EC2 hosting
- Docker-based application deployment
- Docker Compose service orchestration
- Nginx reverse proxy
- Public DNS configuration using DuckDNS
- HTTPS encryption using Let's Encrypt
- Automatic certificate renewal using Certbot
- HTTP-to-HTTPS redirection

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python, JavaScript |
| Frontend | React, Vite |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Caching | Redis |
| Event Streaming | Apache Kafka |
| Authentication | JWT, PyJWT |
| Password Security | Argon2, pwdlib |
| AI Integration | OpenAI Responses API |
| Data Validation | Pydantic |
| Testing | Pytest |
| API Documentation | Swagger UI, OpenAPI |
| Containerization | Docker |
| Service Orchestration | Docker Compose |
| Container Orchestration | Kubernetes |
| Continuous Integration | GitHub Actions |
| Cloud Infrastructure | Amazon EC2 |
| Reverse Proxy | Nginx |
| DNS | DuckDNS |
| HTTPS | Let's Encrypt, Certbot |
| Version Control | Git, GitHub |

## System Architecture

```mermaid
flowchart TD
    U[User Browser] -->|HTTPS| N[Nginx Reverse Proxy]

    subgraph AWS[Amazon EC2]
        N --> F[React Frontend]
        F -->|REST API Requests| N
        N -->|API Proxy| A[FastAPI Backend]

        A --> AU[Authentication and Authorization]
        AU --> S[Service Layer]

        S --> R[Repository Layer]
        R --> P[(PostgreSQL)]

        S --> C[(Redis Cache)]
        S --> KP[Kafka Producer]
        KP --> K[Apache Kafka]
        K --> KC[Kafka Consumer]

        S --> AI[OpenAI Integration]
    end

    AI --> O[OpenAI Responses API]
```

### Architecture Overview

The application uses a layered architecture to separate responsibilities and improve maintainability.

| Layer | Responsibility |
|---|---|
| Presentation Layer | React dashboard and user interactions |
| API Layer | FastAPI routing and request validation |
| Security Layer | Authentication and resource authorization |
| Service Layer | Business logic, financial calculations, and caching |
| Repository Layer | Database queries and persistence |
| Integration Layer | OpenAI API and Kafka integration |
| Infrastructure Layer | Docker, Kubernetes, AWS, and Nginx |

### Request Flow

1. A user accesses the React application through HTTPS.
2. Nginx serves the frontend and forwards API requests to FastAPI.
3. FastAPI validates the request and authenticates the user.
4. The service layer executes the required business logic.
5. Redis may provide cached data when applicable.
6. The repository layer retrieves or modifies PostgreSQL records.
7. Transaction creation can publish an event to Kafka.
8. AI analysis requests communicate with the OpenAI API.
9. The backend returns a structured response to the frontend.

## Backend Architecture

```text
FastAPI Routers
       |
       v
Authentication and Authorization
       |
       v
Service Layer
       |
       +--------------------+
       |                    |
       v                    v
Repository Layer      External Integrations
       |                    |
       v                    +-- Redis
PostgreSQL                  +-- Kafka
                            +-- OpenAI API
```

### Design Principles

- Separation of concerns
- Layered application architecture
- Dependency injection
- Repository pattern
- Service-oriented business logic
- Cache-aside caching
- Event-driven communication
- Environment-based configuration
- Containerized deployment

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
|   |-- integrations/
|   |
|   |-- main.py
|   |-- database.py
|   |-- models.py
|   |-- schemas.py
|   |-- security.py
|   |-- dependencies.py
|   |-- redis_client.py
|   |-- kafka_producer.py
|   |-- kafka_consumer.py
|
|-- frontend/
|   |-- src/
|   |-- package.json
|
|-- k8s/
|
|-- tests/
|
|-- .dockerignore
|-- .gitignore
|-- alembic.ini
|-- compose.yaml
|-- Dockerfile
|-- requirements.txt
|-- README.md
```

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

### AI Financial Analysis

| Method | Endpoint | Description |
|---|---|---|
| GET | `/ai/spending-analysis/{user_id}` | Generate personalized financial analysis |

Protected endpoints require a valid JWT access token.

The deployed Nginx reverse proxy forwards requests under `/api/` to the corresponding FastAPI routes.

## Authentication Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant F as React Frontend
    participant A as FastAPI
    participant D as PostgreSQL

    U->>F: Submit login credentials
    F->>A: POST /auth/login
    A->>D: Retrieve user
    D-->>A: User and password hash
    A->>A: Verify Argon2 password hash
    A-->>F: Signed JWT access token
    F->>A: Protected request with JWT
    A->>A: Validate token and ownership
    A->>D: Retrieve authorized data
    D-->>A: User-specific data
    A-->>F: API response
    F-->>U: Display financial dashboard
```

JWT configuration:

- Algorithm: HS256
- Access token expiration: 30 minutes
- Signing secret: Loaded from `JWT_SECRET_KEY`

The backend validates authenticated identities and applies resource ownership checks before allowing access to protected financial data.

## Redis Caching Workflow

The backend uses a cache-aside strategy for transaction retrieval.

```mermaid
flowchart TD
    A[Transaction Retrieval Request] --> B[Check Redis Cache]
    B --> C{Cache Hit?}
    C -->|Yes| D[Return Cached Data]
    C -->|No| E[Query PostgreSQL]
    E --> F[Store Result in Redis with TTL]
    F --> G[Return Database Result]

    H[Create Update or Delete Transaction] --> I[Update PostgreSQL]
    I --> J[Invalidate Relevant Cache]
```

### Benefits

- Reduces repetitive database queries
- Improves response times for cacheable operations
- Limits stale data through expiration and invalidation
- Separates caching logic from database persistence

## Kafka Event Processing

Apache Kafka provides an event-driven communication mechanism within the application.

When a transaction is created, the backend publishes a transaction-created event.

```mermaid
flowchart LR
    A[Create Transaction] --> B[FastAPI Service]
    B --> C[(PostgreSQL)]
    B --> D[Kafka Producer]
    D --> E[transactions.created Topic]
    E --> F[Kafka Consumer]
    F --> G[Event Processing]
```

Example event structure:

```json
{
  "event": "transaction.created",
  "data": {
    "id": 1,
    "description": "Grocery shopping",
    "amount": 75.50,
    "category": "Food",
    "user_id": 1
  }
}
```

The producer publishes events to the `transactions.created` topic, while the consumer runs independently to process those events.

This architecture provides a foundation for future notification services, financial reporting, auditing, and asynchronous processing.

## AI Financial Analysis Workflow

The AI analysis feature combines deterministic financial calculations with natural-language explanations generated by OpenAI.

```mermaid
flowchart TD
    A[User Requests AI Insights] --> B[Validate Authentication]
    B --> C[Retrieve User Transactions]
    C --> D[Calculate Financial Totals]
    D --> E[Prepare Structured AI Input]
    E --> F[OpenAI Responses API]
    F --> G[Validate Structured Response]
    G --> H[Display Financial Insights]
```

The backend calculates financial totals and category summaries before sending the relevant information to the AI integration.

The AI-generated response includes:

- Financial summary
- Highest spending category
- Key financial insights
- Practical recommendations

Transaction descriptions are treated as untrusted data rather than executable instructions, helping reduce prompt-injection risk.

AI-generated recommendations are informational and should not be considered professional financial advice.

## Getting Started

### Prerequisites

For local development, install:

- Python
- Node.js and npm
- PostgreSQL
- Redis
- Apache Kafka
- Git
- Docker and Docker Compose, if using containerized services

An OpenAI API key is required for AI-generated financial insights.

### 1. Clone the Repository

```bash
git clone https://github.com/divyp7642/finassist-ai.git
cd finassist-ai
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/YOUR_DB_NAME

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=gpt-4.1-mini

JWT_SECRET_KEY=YOUR_SECURE_RANDOM_SECRET

REDIS_HOST=localhost
REDIS_PORT=6379

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

Replace all placeholders with your own configuration.

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API credential |
| `OPENAI_MODEL` | AI model used for financial analysis |
| `JWT_SECRET_KEY` | Secret used to sign JWT tokens |
| `REDIS_HOST` | Redis server hostname |
| `REDIS_PORT` | Redis server port |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker connection address |

Use a long, cryptographically random JWT signing secret.

Never commit `.env` files, API credentials, database passwords, or signing secrets to version control.

### 5. Apply Database Migrations

Ensure PostgreSQL is running and the configured database exists.

```bash
python -m alembic upgrade head
```

### 6. Start the Backend

Ensure the required PostgreSQL, Redis, and Kafka services are available.

```bash
python -m uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 7. Start the Kafka Consumer

Open a separate terminal with the Python virtual environment activated.

```bash
python -m app.kafka_consumer
```

### 8. Start the React Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Configure the frontend API base URL to match the running backend or local reverse proxy.

The Vite development server typically runs at:

```text
http://localhost:5173
```

## Docker

The backend includes a Dockerfile for building a containerized application image.

Build the image:

```bash
docker build -t finassist-ai:latest .
```

The repository also includes Docker Compose configuration for local development.

```bash
docker compose config
```

Review the Compose configuration and provide the required environment variables, networks, and supporting services before starting the application.

Docker is used to package the backend and its dependencies into a consistent runtime environment.

## Kubernetes

The project includes Kubernetes manifests for running the backend and supporting infrastructure in a container-orchestrated environment.

The Kubernetes configuration includes:

- FastAPI application deployment
- Kafka consumer deployment
- PostgreSQL deployment
- Redis deployment
- Kafka deployment
- Service configuration
- Environment and secret configuration

Inspect the local Kubernetes environment:

```bash
kubectl get nodes
kubectl get deployments
kubectl get pods
kubectl get services
```

The Kubernetes configuration was developed and tested in a local Kubernetes environment.

The public AWS deployment uses Docker Compose rather than a managed Kubernetes cluster.

## AWS Cloud Deployment

FinAssist AI is deployed on an Amazon EC2 instance running Amazon Linux.

### Deployment Architecture

```mermaid
flowchart TD
    U[Internet User] --> DNS[DuckDNS Domain]
    DNS --> SG[AWS Security Group]

    SG -->|HTTPS 443| N[Nginx]
    SG -->|HTTP 80| N

    subgraph EC2[Amazon EC2 Instance]
        N --> F[React Static Build]
        N -->|Internal API Proxy| A[FastAPI Container]

        subgraph Docker[Docker Compose Network]
            A --> P[(PostgreSQL)]
            A --> R[(Redis)]
            A --> K[Kafka Broker]
            K --> C[Kafka Consumer]
        end

        CERT[Certbot] --> N
    end

    A --> O[OpenAI API]
```

### Deployment Components

| Component | Configuration |
|---|---|
| Cloud Provider | Amazon Web Services |
| Compute | Amazon EC2 |
| Operating System | Amazon Linux 2023 |
| Container Runtime | Docker |
| Service Management | Docker Compose |
| Frontend Hosting | Nginx static file serving |
| API Routing | Nginx reverse proxy |
| Database | PostgreSQL container |
| Cache | Redis container |
| Event Streaming | Apache Kafka container |
| DNS | DuckDNS |
| TLS Certificate | Let's Encrypt |
| Certificate Management | Certbot |

### Deployment Security

- Public HTTP and HTTPS access through Nginx
- Restricted SSH access using AWS security groups
- Backend API bound to the local host interface
- Database, Redis, and Kafka kept on the internal Docker network
- Environment-based application credentials
- HTTPS encryption
- HTTP-to-HTTPS redirection
- Automatic TLS certificate renewal

### HTTPS Configuration

The application uses a Let's Encrypt certificate installed through Certbot.

Public application URL:

```text
https://finassist-ai.duckdns.org
```

HTTP requests are redirected to HTTPS.

Certificate renewal has been validated using:

```bash
sudo certbot renew --dry-run
```

The deployment uses a single EC2 instance and is intended for portfolio demonstration and development purposes rather than high-availability financial production workloads.

## Automated Testing

The project uses Pytest for automated backend testing.

Run the test suite:

```bash
python -m pytest -v
```

### Latest Verified Test Result

**28 automated tests passing.**

Testing includes backend functionality such as:

- API request and response validation
- Transaction creation
- Transaction retrieval
- Transaction deletion
- Missing-resource handling
- Service-layer mocking
- Kafka event publishing assertions

The application has also undergone manual testing using Swagger UI and the React frontend.

### Manual Deployment Verification

| Functionality | Status |
|---|---|
| Public website access | Passed |
| User login | Passed |
| Financial dashboard | Passed |
| Income transaction creation | Passed |
| Expense transaction creation | Passed |
| Transaction retrieval | Passed |
| Financial balance calculation | Passed |
| Financial charts | Passed |
| AI-generated financial insights | Passed |
| HTTPS connection | Passed |
| HTTP-to-HTTPS redirect | Passed |
| TLS certificate renewal simulation | Passed |

## Continuous Integration

The repository includes GitHub Actions workflows for automated testing and Docker image build validation.

The CI workflow helps identify regressions and dependency issues introduced by code changes.

Typical CI stages include:

1. Repository checkout
2. Python environment setup
3. Dependency installation
4. Automated test execution
5. Docker image build validation

The public AWS deployment is managed separately from the CI workflow.

## Security Considerations

FinAssist AI implements security controls across the application and infrastructure layers.

### Application Security

- Argon2 password hashing
- JWT-based authentication
- Access token expiration validation
- Protected API endpoints
- Resource ownership checks
- Pydantic request validation
- Environment-based secret management
- Error handling for invalid authentication tokens
- Untrusted-data handling for AI prompts

### Infrastructure Security

- AWS security group restrictions
- HTTPS encryption
- Nginx reverse proxy
- Internal Docker networking
- Restricted backend service exposure
- TLS certificate renewal

Additional security hardening, rate limiting, cross-user cache isolation testing, monitoring, and backup validation are recommended before handling real financial information at scale.

## Engineering Highlights

This project demonstrates practical experience in:

- Designing RESTful APIs with FastAPI
- Implementing layered backend architecture
- Managing relational databases with PostgreSQL
- Applying schema migrations with Alembic
- Implementing authentication and authorization
- Integrating Redis caching and invalidation
- Publishing and consuming Kafka events
- Integrating structured AI-generated responses
- Building interactive React dashboards
- Containerizing application services
- Working with Kubernetes deployments
- Implementing automated testing and CI
- Deploying full-stack applications to AWS
- Configuring Nginx and HTTPS certificates

## Project Status

FinAssist AI has progressed from a local backend application to a publicly accessible full-stack cloud deployment.

| Milestone | Status |
|---|---|
| Backend API development | Completed |
| PostgreSQL integration | Completed |
| Database migrations | Completed |
| JWT authentication | Completed |
| Transaction management | Completed |
| OpenAI integration | Completed |
| Redis caching | Completed |
| Kafka event processing | Completed |
| Automated backend testing | Completed |
| GitHub Actions CI | Implemented |
| React frontend | Completed |
| Docker containerization | Completed |
| Local Kubernetes configuration | Completed |
| AWS EC2 deployment | Completed |
| Nginx reverse proxy | Completed |
| Public DNS configuration | Completed |
| HTTPS configuration | Completed |

## Future Improvements

- Automated deployment pipeline to AWS
- Infrastructure as Code using Terraform
- Managed PostgreSQL using Amazon RDS
- Managed Redis using Amazon ElastiCache
- Improved event delivery guarantees
- Idempotent Kafka event processing
- Expanded integration and security testing
- API rate limiting
- Application monitoring and alerting
- Centralized logging
- Database backup and recovery automation
- Advanced financial analytics
- Budget planning and savings goals
- Enhanced mobile responsiveness
- Horizontal scaling and high-availability deployment

## Author

**Divykumar Patel**

M.S. in Computer Science  
Loyola Marymount University

Software Engineering | Backend Development | AI Integration | Cloud Engineering

- GitHub: [divyp7642](https://github.com/divyp7642)
- Live Project: [FinAssist AI](https://finassist-ai.duckdns.org)

## Disclaimer

FinAssist AI is a personal software engineering portfolio project.

It is intended for educational and demonstration purposes. AI-generated financial insights are informational and do not constitute professional financial advice.

Users should avoid entering sensitive or real financial information into the demonstration environment.

## License

No license has been specified for this repository.
