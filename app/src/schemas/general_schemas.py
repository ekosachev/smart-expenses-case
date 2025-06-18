from typing import List, Optional
from pydantic import BaseModel

from expense import ExpenseData
from expense_category import ExpenseCategoryData
from vehicle import VehicleData


class ExpenseWithRelations(ExpenseData):
    vehicle: Optional[VehicleData] = None
    driver: Optional[dict] = None  # Упрощенная схема водителя
    category: Optional[ExpenseCategoryData] = None


class VehicleWithExpenses(VehicleData):
    last_expenses: List[ExpenseData] = []


class PaginatedResponse(BaseModel):
    items: List[BaseModel]
    total: int
    page: int
    pages: int
    size: int
