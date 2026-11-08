
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ai, auth, transactions, users

app = FastAPI()

# Allow our React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(ai.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FinAssist AI"}
