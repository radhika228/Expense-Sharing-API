from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.group import Group, group_members
from app.models.expense import Expense


class ExpenseService:

    @staticmethod
    def create_expense(db: Session, payload):

        group = db.query(Group).filter(
            Group.id == payload.group_id
        ).first()

        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        payer = db.query(User).filter(
            User.id == payload.paid_by
        ).first()

        if payer is None:
            raise HTTPException(status_code=404, detail="User not found")

        membership = db.execute(
            group_members.select().where(
                group_members.c.group_id == payload.group_id,
                group_members.c.user_id == payload.paid_by,
            )
        ).first()

        if membership is None:
            raise HTTPException(
                status_code=400,
                detail="Payer is not a member of this group"
            )

        # Percentage and custom splits will be enabled
        # after their allocation logic is implemented.
        if payload.split_type != "equal":
            raise HTTPException(
                status_code=400,
                detail="Only equal split is currently supported"
            )

        expense = Expense(
            group_id=payload.group_id,
            paid_by=payload.paid_by,
            amount=payload.amount,
            description=payload.description,
            category=payload.category,
            split_type=payload.split_type,
        )

        db.add(expense)
        db.commit()
        db.refresh(expense)

        return expense, payer

    @staticmethod
    def get_group_expenses(db: Session, group_id: int, search: str = ""):

        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        query = db.query(Expense, User.name).join(
            User, User.id == Expense.paid_by
        ).filter(
            Expense.group_id == group_id
        )

        if search.strip():
            query = query.filter(
                Expense.description.ilike(f"%{search.strip()}%")
            )

        rows = query.order_by(Expense.id.desc()).all()

        return [
            {
                "id": expense.id,
                "description": expense.description,
                "amount": str(expense.amount),
                "paid_by": payer_name,
                "category": expense.category,
                "split_type": expense.split_type,
            }
            for expense, payer_name in rows
        ]

    @staticmethod
    def get_expense_suggestions(db: Session, group_id: int, search: str):

        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        if not search.strip():
            return []

        suggestions = (
            db.query(Expense.description)
            .filter(
                Expense.group_id == group_id,
                Expense.description.ilike(f"%{search.strip()}%")
            )
            .distinct()
            .limit(10)
            .all()
        )

        return [item[0] for item in suggestions]