from decimal import Decimal

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import User
from app.models.group import Group, group_members
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate
from app.services.expense_service import ExpenseService
from app.services.balance_service import BalanceService


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = TestingSession()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def create_group_with_members(db):
    user1 = User(name="Rahul")
    user2 = User(name="Aman")
    group = Group(name="Trip")

    db.add_all([user1, user2, group])
    db.commit()

    db.execute(
        group_members.insert(),
        [
            {"group_id": group.id, "user_id": user1.id},
            {"group_id": group.id, "user_id": user2.id},
        ],
    )
    db.commit()

    return user1, user2, group


# 1. Existing amount conversion tests

def test_amount_to_minor_units():
    assert BalanceService._to_minor_units(Decimal("12.34")) == 1234


def test_amount_rounds_to_minor_unit():
    assert BalanceService._to_minor_units(Decimal("10.999")) == 1100


# 2. Expense creation test

def test_expense_creation(db):
    user1, user2, group = create_group_with_members(db)

    payload = ExpenseCreate(
        group_id=group.id,
        paid_by=user1.id,
        amount=Decimal("100.00"),
        description="Dinner",
        category="Food",
        split_type="equal",
    )

    expense, payer = ExpenseService.create_expense(db, payload)

    assert expense.id is not None
    assert expense.amount == Decimal("100.00")
    assert expense.description == "Dinner"
    assert payer.name == "Rahul"


# 3. Balance calculation test

def test_balance_calculation(db):
    user1, user2, group = create_group_with_members(db)

    expense = Expense(
        group_id=group.id,
        paid_by=user1.id,
        amount=Decimal("100.00"),
        description="Dinner",
        category="Food",
        split_type="equal",
    )

    db.add(expense)
    db.commit()

    result = BalanceService.calculate(db, group.id)

    assert result["group"] == "Trip"
    assert result["settlements"] == [
        {
            "from": "Aman",
            "to": "Rahul",
            "amount": "50.00",
        }
    ]


# 4. Validation logic test

def test_expense_validation():
    with pytest.raises(ValidationError):
        ExpenseCreate(
            group_id=1,
            paid_by=1,
            amount=Decimal("0.50"),
            description="Dinner",
        )

    with pytest.raises(ValidationError):
        ExpenseCreate(
            group_id=1,
            paid_by=1,
            amount=Decimal("100.00"),
            description="   ",
        )

    with pytest.raises(ValidationError):
        ExpenseCreate(
            group_id=1,
            paid_by=1,
            amount=Decimal("100.00"),
            description="Dinner",
            split_type="invalid",
        )