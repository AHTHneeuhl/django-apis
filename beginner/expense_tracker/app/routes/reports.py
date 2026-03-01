# app/routes/reports.py

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from io import StringIO
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
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


@router.get("/export-csv")
def export_csv(
    type: str = None,
    category: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Transaction)

    # Apply filters if provided
    if type:
        query = query.filter(models.Transaction.type == type)

    if category:
        query = query.filter(models.Transaction.category == category)

    if start_date:
        query = query.filter(models.Transaction.created_at >= start_date)

    if end_date:
        query = query.filter(models.Transaction.created_at <= end_date)

    transactions = query.all()

    # Convert to list of dicts
    data = [
        {
            "id": t.id,
            "title": t.title,
            "amount": t.amount,
            "type": t.type,
            "category": t.category,
            "created_at": t.created_at
        }
        for t in transactions
    ]

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Write to CSV in memory
    stream = StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    # Return as downloadable file
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )