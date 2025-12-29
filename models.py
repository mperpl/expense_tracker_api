from decimal import Decimal
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, Date, func
from typing import Optional
from datetime import date

class Expense(Base):
    __tablename__ = 'expenses'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(24), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    expense_date: Mapped[date] = mapped_column(Date, server_default=func.current_date())