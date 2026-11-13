from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    group_id = Column(
        Integer,
        ForeignKey("groups.id"),
        nullable=False,
        index=True
    )

    paid_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    amount = Column(Numeric(10, 2), nullable=False)

    description = Column(String(255), nullable=False)

    category = Column(
        String(50),
        nullable=False,
        default="Other"
    )

    split_type = Column(
        String(20),
        nullable=False,
        default="equal"
    )