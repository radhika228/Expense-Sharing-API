from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator


class ExpenseCreate(BaseModel):
    group_id: int = Field(gt=0)
    paid_by: int = Field(gt=0)

    amount: Decimal = Field(
        ge=Decimal("1.00"),
        max_digits=10,
        decimal_places=2
    )

    description: str = Field(min_length=1, max_length=255)

    category: str = Field(default="Other", min_length=1, max_length=50)

    split_type: Literal["equal", "percentage", "custom"] = "equal"

    @field_validator("description", "category")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value


class ExpenseResponse(BaseModel):
    id: int
    group_id: int
    paid_by: str
    amount: str
    description: str
    category: str
    split_type: str

    model_config = ConfigDict(from_attributes=True)