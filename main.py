from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import (
    create_engine, Column, Integer, String,
    ForeignKey, Table, UniqueConstraint, Numeric
)
from sqlalchemy.orm import sessionmaker, declarative_base
from decimal import Decimal, ROUND_HALF_UP


# DATABASE SETUP

app = FastAPI(title="Expense Sharing API")

DATABASE_URL = "sqlite:///./expense.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# DATABASE TABLES

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


group_members = Table(
    "group_members",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    UniqueConstraint("group_id", "user_id")
)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    paid_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


# REQUEST MODELS

class UserCreate(BaseModel):
    name: str


class GroupCreate(BaseModel):
    name: str


class MemberCreate(BaseModel):
    user_id: int


class ExpenseCreate(BaseModel):
    group_id: int
    paid_by: int
    amount: Decimal = Field(gt=0)
    description: str


# HOME API

@app.get("/")
def home():
    return {"message": "Welcome to Expense Sharing API"}


# CREATE USER

@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()

    try:
        new_user = User(name=user.name)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "name": new_user.name
        }

    finally:
        db.close()


# GET ALL USERS

@app.get("/users")
def get_users():
    db = SessionLocal()

    try:
        users = db.query(User).all()

        return [
            {"id": user.id, "name": user.name}
            for user in users
        ]

    finally:
        db.close()


# CREATE GROUP

@app.post("/groups")
def create_group(group: GroupCreate):
    db = SessionLocal()

    try:
        new_group = Group(name=group.name)

        db.add(new_group)
        db.commit()
        db.refresh(new_group)

        return {
            "id": new_group.id,
            "name": new_group.name
        }

    finally:
        db.close()


# ADD MEMBER TO GROUP

@app.post("/groups/{group_id}/members")
def add_member(group_id: int, member: MemberCreate):
    db = SessionLocal()

    try:
        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        user = db.query(User).filter(
            User.id == member.user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        existing = db.execute(
            group_members.select().where(
                group_members.c.group_id == group_id,
                group_members.c.user_id == member.user_id
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="User is already a member"
            )

        db.execute(
            group_members.insert().values(
                group_id=group_id,
                user_id=member.user_id
            )
        )

        db.commit()

        return {"message": "Member added successfully"}

    finally:
        db.close()


# GET GROUP MEMBERS

@app.get("/groups/{group_id}/members")
def get_group_members(group_id: int):
    db = SessionLocal()

    try:
        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        results = db.query(User).join(
            group_members,
            User.id == group_members.c.user_id
        ).filter(
            group_members.c.group_id == group_id
        ).all()

        return [
            {"id": user.id, "name": user.name}
            for user in results
        ]

    finally:
        db.close()


# CREATE EXPENSE

@app.post("/expenses")
def create_expense(expense: ExpenseCreate):
    db = SessionLocal()

    try:
        group = db.query(Group).filter(
            Group.id == expense.group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        user = db.query(User).filter(
            User.id == expense.paid_by
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        membership = db.execute(
            group_members.select().where(
                group_members.c.group_id == expense.group_id,
                group_members.c.user_id == expense.paid_by
            )
        ).first()

        if not membership:
            raise HTTPException(
                status_code=400,
                detail="Payer is not a member of this group"
            )

        new_expense = Expense(
            group_id=expense.group_id,
            paid_by=expense.paid_by,
            amount=expense.amount,
            description=expense.description
        )

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return {
            "id": new_expense.id,
            "group_id": new_expense.group_id,
            "paid_by": user.name,
            "amount": str(new_expense.amount),
            "description": new_expense.description
        }

    finally:
        db.close()


# GET GROUP EXPENSES

@app.get("/groups/{group_id}/expenses")
def get_group_expenses(group_id: int, search: str = ""):
    db = SessionLocal()

    try:
        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        query = db.query(Expense).filter(
            Expense.group_id == group_id
        )

        if search:
            query = query.filter(
                Expense.description.ilike(f"%{search}%")
            )

        expenses = query.all()
        result = []

        for expense in expenses:
            payer = db.query(User).filter(
                User.id == expense.paid_by
            ).first()

            result.append({
                "id": expense.id,
                "description": expense.description,
                "amount": str(expense.amount),
                "paid_by": payer.name
            })

        return result

    finally:
        db.close()


# CALCULATE BALANCES

@app.get("/groups/{group_id}/balances")
def get_balances(group_id: int):
    db = SessionLocal()

    try:
        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        members = db.query(User).join(
            group_members,
            User.id == group_members.c.user_id
        ).filter(
            group_members.c.group_id == group_id
        ).order_by(User.id).all()

        if not members:
            raise HTTPException(
                status_code=400,
                detail="Group has no members"
            )

        expenses = db.query(Expense).filter(
            Expense.group_id == group_id
        ).all()

        balances = {
            member.id: 0 for member in members
        }

        for expense in expenses:

            total_cents = int(
                (Decimal(expense.amount) * 100).quantize(
                    Decimal("1"),
                    rounding=ROUND_HALF_UP
                )
            )

            member_count = len(members)

            share, remainder = divmod(
                total_cents,
                member_count
            )

            for index, member in enumerate(members):

                member_share = share

                if index < remainder:
                    member_share += 1

                balances[member.id] -= member_share

            balances[expense.paid_by] += total_cents

        creditors = []
        debtors = []

        for member in members:

            balance = balances[member.id]

            if balance > 0:
                creditors.append([member.id, balance])

            elif balance < 0:
                debtors.append([member.id, -balance])

        transactions = []

        i = 0
        j = 0

        while i < len(debtors) and j < len(creditors):

            debtor_id, debt = debtors[i]
            creditor_id, credit = creditors[j]

            amount = min(debt, credit)

            debtor_name = next(
                m.name for m in members
                if m.id == debtor_id
            )

            creditor_name = next(
                m.name for m in members
                if m.id == creditor_id
            )

            transactions.append({
                "from": debtor_name,
                "to": creditor_name,
                "amount": f"{amount / 100:.2f}"
            })

            debtors[i][1] -= amount
            creditors[j][1] -= amount

            if debtors[i][1] == 0:
                i += 1

            if creditors[j][1] == 0:
                j += 1

        return {
            "group": group.name,
            "settlements": transactions
        }

    finally:
        db.close()