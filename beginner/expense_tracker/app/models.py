# app/models.py

from sqlalchemy import ForeignKey, Column, Integer, String, Float, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from .database import Base


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # Relationship
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Short description of transaction
    title = Column(String, nullable=False)

    # Amount of money
    amount = Column(Float, nullable=False)

    # income or expense
    type = Column(SqlEnum(TransactionType), nullable=False)

    # When transaction happened
    created_at = Column(DateTime, default=datetime.utcnow)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="transactions")