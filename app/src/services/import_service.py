import csv
from io import StringIO
from sqlalchemy import select

# from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.models import ExpenseCategory

# from src.database.models.models import Vehicle, Expense
from src.database.user_db import get_user_by_id
from src.schemas.import_schemas import VehicleCSVRow, ExpenseCSVRow, ImportResult
from src.schemas.vehicle import VehicleCreate
from src.schemas.expense import ExpenseCreate
from src.services.vehicle import VehicleService
from src.services.expense import ExpenseService
from src.services.expense_category import ExpenseCategoryService
# from datetime import datetime


class ImportService:
    @staticmethod
    async def import_vehicles_from_csv(
        session: AsyncSession, csv_content: str, company_id: int, user_id: int
    ) -> ImportResult:
        """Импорт транспортных средств из CSV"""
        reader = csv.DictReader(StringIO(csv_content))
        result = ImportResult(success_count=0, error_count=0, errors=[])
        service = VehicleService()

        for row_num, row in enumerate(reader, 1):
            try:
                # Валидация строки
                vehicle_data = VehicleCSVRow(**row)

                # Проверка уникальности госномера
                existing = await service.repository.get_by_license_plate(
                    session, vehicle_data.license_plate, include_inactive=True
                )
                if existing:
                    raise ValueError(
                        f"ТС с госномером {vehicle_data.license_plate} уже существует"
                    )

                # Создание ТС
                await service.create_vehicle(
                    session,
                    VehicleCreate(
                        license_plate=vehicle_data.license_plate,
                        make=vehicle_data.make,
                        model=vehicle_data.model,
                        year=vehicle_data.year,
                        vehicle_type=vehicle_data.vehicle_type,
                        current_mileage=vehicle_data.current_mileage,
                        carrying_capacity=vehicle_data.carrying_capacity,
                        fuel_consumption_rate=vehicle_data.fuel_consumption_rate,
                        company_id=company_id,
                    ),
                    user_id=user_id,
                )
                result.success_count += 1
            except Exception as e:
                result.error_count += 1
                result.errors.append({"row": row_num, "error": str(e), "data": row})

        return result

    @staticmethod
    async def import_expenses_from_csv(
        session: AsyncSession, csv_content: str, company_id: int, user_id: int
    ) -> ImportResult:
        """Импорт расходов из CSV"""
        reader = csv.DictReader(StringIO(csv_content))
        result = ImportResult(success_count=0, error_count=0, errors=[])
        vehicle_service = VehicleService()
        expense_service = ExpenseService()
        category_service = ExpenseCategoryService()

        # Кэш для быстрого доступа
        license_plate_cache = {}
        category_name_cache = {}
        driver_cache = {}

        for row_num, row in enumerate(reader, 1):
            try:
                # Валидация строки
                expense_data = ExpenseCSVRow(**row)

                # Поиск ТС по госномеру (с кэшированием)
                license_plate = expense_data.license_plate
                if license_plate not in license_plate_cache:
                    vehicle = await vehicle_service.repository.get_by_license_plate(
                        session, license_plate
                    )
                    if not vehicle:
                        raise ValueError(f"ТС с госномером {license_plate} не найдено")
                    license_plate_cache[license_plate] = vehicle.id
                vehicle_id = license_plate_cache[license_plate]

                if expense_data.driver_id not in driver_cache:
                    driver = await get_user_by_id(expense_data.driver_id)
                    if not driver:
                        raise ValueError(
                            f"Пользователь с id {expense_data.driver_id} не найден"
                        )
                    driver_cache[expense_data.driver_id] = driver.id

                # Поиск категории по имени (с кэшированием)
                category_name = expense_data.category_name
                if category_name not in category_name_cache:
                    # Ищем категорию по имени
                    categories = await session.execute(
                        select(ExpenseCategory).where(
                            ExpenseCategory.name == category_name
                        )
                    )
                    category = categories.scalars().first()
                    if not category:
                        # Создаем новую категорию, если не найдена
                        category = ExpenseCategory(
                            name=category_name, code=category_name.upper()[:10]
                        )
                        session.add(category)
                        await session.commit()
                        await session.refresh(category)
                    category_name_cache[category_name] = category.id
                category_id = category_name_cache[category_name]

                # Создание расхода
                await expense_service.create_expense(
                    session,
                    ExpenseCreate(
                        amount=expense_data.amount,
                        expense_date=expense_data.expense_date,
                        category_id=category_id,
                        vehicle_id=vehicle_id,
                        description=expense_data.description,
                        company_id=company_id,
                        driver_id=expense_data.driver_id,
                    ),
                    user_id=user_id,
                )
                result.success_count += 1
            except Exception as e:
                result.error_count += 1
                result.errors.append({"row": row_num, "error": str(e), "data": row})

        return result
