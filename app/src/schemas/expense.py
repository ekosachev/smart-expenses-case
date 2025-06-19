from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    company_id: int
    amount: float
    expense_date: date
    category_id: int
    vehicle_id: int
    description: Optional[str] = Field(None, max_length=255)


class ExpenseData(ExpenseCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    approver_id: Optional[int] = None


class ExpenseEdit(BaseModel):
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    category_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    description: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = None
    approver_id: Optional[int] = None
