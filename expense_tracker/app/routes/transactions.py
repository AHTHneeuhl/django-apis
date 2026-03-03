# app/routes/transactions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# ➕ Create Transaction
@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_transaction = models.Transaction(
        **transaction.model_dump(),
        user_id=current_user.id
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction.filter(models.Transaction.user_id == current_user.id).first()


# 📄 Get All Transactions
@router.get("/", response_model=List[schemas.TransactionResponse])
def get_transactions(
    type: Optional[schemas.TransactionType] = None,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Always restrict to current user
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    )

    if type:
        query = query.filter(models.Transaction.type == type)

    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)

    if start_date:
        query = query.filter(models.Transaction.created_at >= start_date)

    if end_date:
        query = query.filter(models.Transaction.created_at <= end_date)

    return query.all()


# Update Transaction
@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    updated_data: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update fields
    for key, value in updated_data.model_dump().items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


# Delete Transaction
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}