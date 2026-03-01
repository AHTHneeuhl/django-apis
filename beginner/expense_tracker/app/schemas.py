# app/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    category_id: int


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: TransactionType
    created_at: datetime
    CategoryResponse

    class Config:
        from_attributes = True  # For SQLAlchemy (Pydantic v2)