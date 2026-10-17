from decimal import Decimal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)

class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: str
    password: str

class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    user_id: int = Field(gt=0)

class SpendingAnalysis(BaseModel):
    summary: str
    top_category: str
    insights: list[str]
    recommendation: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
