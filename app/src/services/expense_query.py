from datetime import timedelta, date
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.expense_category import ExpenseCategoryData
from src.schemas.expense_query import (
    BudgetComparison,
    ExpenseQuery,
    ExpenseQueryResponse,
    QueryGroupPeriod,
)
from src.schemas.vehicle import VehicleData
from src.services.expense import ExpenseService
from src.schemas.expense import ExpenseData
from src.services.expense_category import ExpenseCategoryService
from src.services.vehicle import VehicleService


async def expense_query(
    session: AsyncSession, data: ExpenseQuery
) -> ExpenseQueryResponse:
    expense_service = ExpenseService()
    expenses: list[ExpenseData] = await expense_service.get_entities(session, 0, None)
    expenses = list(filter(lambda e: e.company_id == data.company_id, expenses))
    expenses = list(
        filter(
            lambda e: (e.expense_date < data.end_date)
            and (e.expense_date >= data.start_date),
            expenses,
        )
    )

    if data.category_ids is not None:
        expenses = list(filter(lambda e: e.category_id in data.category_ids, expenses))

    if data.vehicle_ids is not None:
        expenses = list(filter(lambda e: e.vehicle_id in data.vehicle_ids, expenses))

    period_length: timedelta
    if data.group_by == QueryGroupPeriod.day:
        period_length = timedelta(days=1)
    elif data.group_by == QueryGroupPeriod.month:
        period_length = timedelta(days=30)
    else:
        period_length = timedelta(days=365)

    periods: list[tuple[date, date]] = [
        (data.start_date, data.start_date + period_length)
    ]

    while True:
        if periods[-1][1] >= data.end_date:
            break
        periods.append((periods[-1][1], periods[-1][1] + period_length))

    vehicle_service = VehicleService()
    vehicles: dict[int, VehicleData | None] = {}
    if data.vehicle_ids is not None:
        vehicles = {
            id: await vehicle_service.get_entity(session, id) for id in data.vehicle_ids
        }

    category_service = ExpenseCategoryService()
    categories: dict[int, ExpenseCategoryData | None] = {}
    if data.category_ids is not None:
        categories = {
            id: await category_service.get_entity(session, id)
            for id in data.category_ids
        }

    expense_amounts: list[float] = [e.amount for e in expenses]

    return ExpenseQueryResponse(
        total_expenses=sum(map(lambda e: e.amount, expenses)),
        expenses_by_period={
            (start_date, end_date): sum(
                [
                    e.amount
                    for e in expenses
                    if (e.expense_date >= start_date) and (e.expense_date < end_date)
                ]
            )
            for (start_date, end_date) in periods
        },
        expenses_by_category={
            category_obj.name: sum(
                [e.amount for e in expenses if e.category_id == category_id]
            )
            for (category_id, category_obj) in categories.items()
            if category_obj is not None
        }
        if categories
        else None,
        expenses_by_vehicle={
            vehicle_obj.license_plate: sum(
                [e.amount for e in expenses if e.vehicle_id == vehicle_id]
            )
            for (vehicle_id, vehicle_obj) in vehicles.items()
            if vehicle_obj is not None
        }
        if vehicles
        else None,
        max_expense=max(expense_amounts),
        min_expense=min(expense_amounts),
        average_expense=sum(expense_amounts) / len(expense_amounts),
        budget_comparison=BudgetComparison(
            planned_budget=data.planned_budget,
            actual_expenses=sum(expense_amounts),
            budget_utilization=sum(expense_amounts) / data.planned_budget * 100,
        ),
    )
