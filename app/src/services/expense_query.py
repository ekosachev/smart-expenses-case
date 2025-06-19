from datetime import timedelta, date
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.expense_category import ExpenseCategoryData
from src.schemas.expense_query import (
    BudgetComparison,
    ExpenseQuery,
    ExpenseQueryResponse,
    ExpensesForCategory,
    ExpensesForTimePeriod,
    ExpensesForVehicle,
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
        expenses = [e for e in expenses if e.category_id in data.category_ids]

    if data.vehicle_ids is not None:
        expenses = [e for e in expenses if e.vehicle_id in data.vehicle_ids]

    if len(expenses) == 0:
        raise ValueError("Нет транзаций за указанный период")

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

    expenses_grouped_by_periods = {
        (start_date, end_date): [
            e
            for e in expenses
            if (e.expense_date >= start_date) and (e.expense_date < end_date)
        ]
        for (start_date, end_date) in periods
    }

    expenses_grouped_by_category = {
        category.name: [e for e in expenses if e.category_id == category.id]
        for category in categories.values()
        if category is not None
    }

    expenses_grouped_by_vehicle = {
        (vehicle.license_plate, vehicle.make, vehicle.model, vehicle.vehicle_type): [
            e for e in expenses if e.vehicle_id == vehicle.id
        ]
        for vehicle in vehicles.values()
        if vehicle is not None
    }

    expense_amounts: list[float] = [e.amount for e in expenses]

    return ExpenseQueryResponse(
        total_expenses=sum(map(lambda e: e.amount, expenses)),
        expenses_by_period=[
            ExpensesForTimePeriod(
                min_expense=min(e.amount for e in expenses) if expenses else 0,
                max_expense=max(e.amount for e in expenses) if expenses else 0,
                average_expense=sum(e.amount for e in expenses) / len(expenses)
                if expenses
                else 0,
                total_expenses=sum(e.amount for e in expenses) if expenses else 0,
                time_period_start=start_date,
                time_period_end=end_date,
            )
            for (
                (start_date, end_date),
                expenses,
            ) in expenses_grouped_by_periods.items()
        ],
        expenses_by_category=[
            ExpensesForCategory(
                min_expense=min(e.amount for e in expenses) if expenses else 0,
                max_expense=max(e.amount for e in expenses) if expenses else 0,
                average_expense=sum(e.amount for e in expenses) / len(expenses)
                if expenses
                else 0,
                total_expenses=sum(e.amount for e in expenses) if expenses else 0,
                category_name=category_name,
            )
            for (category_name, expenses) in expenses_grouped_by_category.items()
        ]
        if data.category_ids
        else None,
        expenses_by_vehicle=[
            ExpensesForVehicle(
                min_expense=min(e.amount for e in expenses) if expenses else 0,
                max_expense=max(e.amount for e in expenses) if expenses else 0,
                average_expense=sum(e.amount for e in expenses) / len(expenses)
                if expenses
                else 0,
                total_expenses=sum(e.amount for e in expenses) if expenses else 0,
                license_plate=license_plate,
                model=model,
                make=make,
                vehicle_type=vehicle_type,
            )
            for (
                (license_plate, make, model, vehicle_type),
                expenses,
            ) in expenses_grouped_by_vehicle.items()
        ]
        if data.vehicle_ids
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
