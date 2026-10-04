from decimal import Decimal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    user_id: int = Field(gt=0)