from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import ExpenseCreate
from app.services.expense_service import ExpenseService
from app.services.balance_service import BalanceService

router = APIRouter(tags=["Expenses"])


@router.post("/expenses", status_code=201)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db)
):
    expense, payer = ExpenseService.create_expense(db, payload)

    return {
        "id": expense.id,
        "group_id": expense.group_id,
        "paid_by": payer.name,
        "amount": str(expense.amount),
        "description": expense.description,
        "category": expense.category,
        "split_type": expense.split_type,
    }


@router.get("/groups/{group_id}/expenses")
def get_group_expenses(
    group_id: int,
    search: str = Query(default="", max_length=100),
    db: Session = Depends(get_db),
):
    return ExpenseService.get_group_expenses(db, group_id, search)


@router.get("/groups/{group_id}/expenses/suggestions")
def get_expense_suggestions(
    group_id: int,
    q: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    return ExpenseService.get_expense_suggestions(db, group_id, q)


@router.get("/groups/{group_id}/balances")
def get_balances(
    group_id: int,
    db: Session = Depends(get_db)
):
    return BalanceService.calculate(db, group_id)