from decimal import Decimal
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    group_id: int = Field(gt=0)
    paid_by: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    description: str = Field(min_length=1, max_length=255)
