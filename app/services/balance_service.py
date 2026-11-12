from decimal import Decimal, ROUND_HALF_UP
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.group import Group, group_members
from app.models.expense import Expense


class BalanceService:
    """Calculates net balances and converts them into settlement transactions."""

    @staticmethod
    def _to_minor_units(amount: Decimal) -> int:
        return int(
            (Decimal(amount) * 100).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )

    @staticmethod
    def calculate(db: Session, group_id: int):
        group = db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        members = (
            db.query(User)
            .join(group_members, User.id == group_members.c.user_id)
            .filter(group_members.c.group_id == group_id)
            .order_by(User.id)
            .all()
        )
        if not members:
            raise HTTPException(status_code=400, detail="Group has no members")

        expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
        balances = {member.id: 0 for member in members}
        member_count = len(members)

        for expense in expenses:
            if expense.paid_by not in balances:
                raise HTTPException(
                    status_code=400,
                    detail="An expense payer is not a current group member",
                )

            total = BalanceService._to_minor_units(expense.amount)
            share, remainder = divmod(total, member_count)

            for index, member in enumerate(members):
                balances[member.id] -= share + (1 if index < remainder else 0)

            balances[expense.paid_by] += total

        creditors = [[uid, value] for uid, value in balances.items() if value > 0]
        debtors = [[uid, -value] for uid, value in balances.items() if value < 0]
        names = {member.id: member.name for member in members}

        settlements = []
        i = j = 0
        while i < len(debtors) and j < len(creditors):
            debtor_id, debt = debtors[i]
            creditor_id, credit = creditors[j]
            amount = min(debt, credit)

            settlements.append({
                "from": names[debtor_id],
                "to": names[creditor_id],
                "amount": f"{Decimal(amount) / Decimal(100):.2f}",
            })

            debtors[i][1] -= amount
            creditors[j][1] -= amount
            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return {"group": group.name, "settlements": settlements}
