# app/routes/reports.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..database import get_db
from .. import models

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly")
def monthly_summary(
    month: int,
    year: int,
    db: Session = Depends(get_db)
):
    # Query total income
    total_income = (
        db.query(func.sum(models.Transaction.amount))
        .filter(models.Transaction.type == "income")
        .filter(extract("month", models.Transaction.created_at) == month)
        .filter(extract("year", models.Transaction.created_at) == year)
        .scalar()
    ) or 0

    # Query total expense
    total_expense = (
        db.query(func.sum(models.Transaction.amount))
        .filter(models.Transaction.type == "expense")
        .filter(extract("month", models.Transaction.created_at) == month)
        .filter(extract("year", models.Transaction.created_at) == year)
        .scalar()
    ) or 0

    return {
        "month": month,
        "year": year,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": total_income - total_expense
    }