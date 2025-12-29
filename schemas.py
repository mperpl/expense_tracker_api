from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional, Literal

CATEGORY = Literal[
        'housing',
        'transportation',
        'shopping',
        'health_fitness',
        'taxes_fees',
        'entertainment',
        'other'
    ]

class ExpenseBase(BaseModel):
    amount: Decimal = Field(ge=0.01)
    category: CATEGORY
    description: Optional[str] = None
    expense_date: date
    model_config = ConfigDict(from_attributes=True)


class Expense(ExpenseBase):
    id: int
