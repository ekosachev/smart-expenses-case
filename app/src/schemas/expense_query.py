import datetime
from typing import Optional
from pydantic import BaseModel
from enum import StrEnum
from datetime import date, datetime

from src.database.models.models import VehicleType


class QueryGroupPeriod(StrEnum):
    day = "day"
    month = "month"
    year = "year"


class ExpenseQuery(BaseModel):
    company_id: int
    start_date: date
    end_date: date
    vehicle_ids: Optional[list[int]] = None
    category_ids: Optional[list[int]] = None
    group_by: QueryGroupPeriod
    planned_budget: float


class BudgetComparison(BaseModel):
    planned_budget: float
    actual_expenses: float
    budget_utilization: float


class ExpenseInfo(BaseModel):
    max_expense: float
    min_expense: float
    average_expense: float
    total_expenses: float


class ExpensesForTimePeriod(ExpenseInfo):
    time_period_start: date
    time_period_end: date


class ExpensesForCategory(ExpenseInfo):
    category_name: str


class ExpensesForVehicle(ExpenseInfo):
    license_plate: str
    model: str
    make: str
    vehicle_type: VehicleType


class ExpenseQueryResponse(BaseModel):
    total_expenses: float
    expenses_by_period: list[ExpensesForTimePeriod]
    expenses_by_category: Optional[list[ExpensesForCategory]]
    expenses_by_vehicle: Optional[list[ExpensesForVehicle]]
    max_expense: float
    min_expense: float
    average_expense: float
    budget_comparison: BudgetComparison
