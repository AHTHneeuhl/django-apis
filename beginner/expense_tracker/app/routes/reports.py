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


@router.get("/monthly-chart")
def monthly_chart(year: int, db: Session = Depends(get_db)):
    # Get month-wise expense totals
    results = (
        db.query(
            extract("month", models.Transaction.created_at).label("month"),
            func.sum(models.Transaction.amount).label("total")
        )
        .filter(models.Transaction.type == "expense")
        .filter(extract("year", models.Transaction.created_at) == year)
        .group_by("month")
        .all()
    )

    # Initialize all months with 0
    monthly_data = {month: 0 for month in range(1, 13)}

    # Fill actual data
    for month, total in results:
        monthly_data[int(month)] = float(total)

    return {
        "year": year,
        "data": monthly_data
    }