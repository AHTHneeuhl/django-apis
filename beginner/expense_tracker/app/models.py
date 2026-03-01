# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Short description of transaction
    title = Column(String, nullable=False)

    # Amount of money
    amount = Column(Float, nullable=False)

    # income or expense
    type = Column(String, nullable=False)

    # Optional category (we’ll normalize later)
    category = Column(String, nullable=True)

    # When transaction happened
    created_at = Column(DateTime, default=datetime.utcnow)