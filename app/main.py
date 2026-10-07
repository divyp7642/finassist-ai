from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import transactions, users


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transactions.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FinAssist AI"}