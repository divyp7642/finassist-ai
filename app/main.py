
from fastapi import FastAPI
from app.routers import ai, auth, transactions, users

app = FastAPI()

app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(ai.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FinAssist AI"}
