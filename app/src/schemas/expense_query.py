import datetime
from typing import Optional
from pydantic import BaseModel
from enum import StrEnum
from datetime import date, datetime


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


class ExpenseQueryResponse(BaseModel):
    total_expenses: float
    expenses_by_period: dict[tuple[date, date], float]
    expenses_by_category: Optional[dict[str, float]]
    expenses_by_vehicle: Optional[dict[str, float]]
    max_expense: float
    min_expense: float
    average_expense: float
    budget_comparison: BudgetComparison
