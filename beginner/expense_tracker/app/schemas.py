# app/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    category: Optional[str] = None


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: TransactionType
    category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy (Pydantic v2)