import csv
from io import BytesIO, StringIO
from typing import List

import pandas as pd
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.models import ExpenseCategory
from src.logs import get_logger
from src.schemas.expense import ExpenseCreate
from src.schemas.import_schemas import ExpenseCSVRow, ImportResult, VehicleCSVRow
from src.schemas.vehicle import VehicleCreate
from src.services.expense import ExpenseService
from src.services.vehicle import VehicleService

logger = get_logger(__name__)


class ImportService:
    @staticmethod
    async def _process_import_data(
        data: List[dict], import_func, *args
    ) -> ImportResult:
        """Общая функция обработки импорта данных"""
        result = ImportResult(success_count=0, error_count=0, errors=[])
        for row_num, row in enumerate(data, 1):
            try:
                await import_func(row, *args)
                result.success_count += 1
                logger.info(f"Success {result.success_count}")
            except Exception as e:
                result.error_count += 1
                result.errors.append({"row": row_num, "error": str(e), "data": row})
                logger.warning(f"Import error: {str(e)}")
        return result

    async def import_vehicles(
        self, session: AsyncSession, data: List[dict], company_id: int, user_id: int
    ) -> ImportResult:
        """Импорт транспортных средств из данных"""
        service = VehicleService()

        async def process_row(row):
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

        return await self._process_import_data(data, process_row)

    async def import_expenses(
        self, session: AsyncSession, data: List[dict], company_id: int, user_id: int
    ) -> ImportResult:
        """Импорт расходов из данных"""
        vehicle_service = VehicleService()
        expense_service = ExpenseService()
        # category_service = ExpenseCategoryService()

        # Кэш для быстрого доступа
        license_plate_cache = {}
        category_name_cache = {}

        async def process_row(row):
            # Валидация строки
            expense_data = ExpenseCSVRow(**row)

            # Поиск ТС по госномеру
            license_plate = expense_data.license_plate
            if license_plate not in license_plate_cache:
                vehicle = await vehicle_service.repository.get_by_license_plate(
                    session, license_plate
                )
                if not vehicle:
                    raise ValueError(f"ТС с госномером {license_plate} не найдено")
                license_plate_cache[license_plate] = vehicle.id
            vehicle_id = license_plate_cache[license_plate]

            # Поиск/создание категории
            category_name = expense_data.category_name
            if category_name not in category_name_cache:
                result = await session.execute(
                    select(ExpenseCategory).where(ExpenseCategory.name == category_name)
                )
                category = result.scalars().first()
                if not category:
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
                ),
                user_id=user_id,
            )

        return await self._process_import_data(data, process_row)

    @staticmethod
    def read_upload_file(file: UploadFile, file_format: str) -> List[dict]:
        """Чтение файла в зависимости от формата"""
        content = file.file.read()

        if file_format == "csv":
            # Декодируем CSV
            try:
                csv_content = content.decode("utf-8")
            except UnicodeDecodeError:
                raise ValueError("Неподдерживаемая кодировка файла. Используйте UTF-8")

            # Читаем CSV в список словарей
            return list(csv.DictReader(StringIO(csv_content)))

        elif file_format == "xlsx":
            # Читаем XLSX с помощью pandas
            try:
                df = pd.read_excel(BytesIO(content))
                return df.replace({pd.NaT: None}).to_dict("records")
            except Exception as e:
                raise ValueError(f"Ошибка чтения XLSX: {str(e)}")

        else:
            raise ValueError("Неподдерживаемый формат файла")

    @staticmethod
    def generate_template(file_format: str, columns: list) -> StreamingResponse:
        """Генерация шаблона для импорта"""
        if file_format == "csv":
            # Создаем CSV с заголовками
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=columns)
            writer.writeheader()
            content = output.getvalue().encode("utf-8")
            media_type = "text/csv"
            filename = f"template_{columns[0]}.csv"

        elif file_format == "xlsx":
            # Создаем пустой XLSX с заголовками
            wb = Workbook()
            ws = wb.active
            ws.title = "Template"
            ws.append(columns)

            # Сохраняем в буфер
            output = BytesIO()
            wb.save(output)
            content = output.getvalue()
            media_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            filename = f"template_{columns[0]}.xlsx"

        else:
            raise ValueError("Неподдерживаемый формат шаблона")

        return StreamingResponse(
            BytesIO(content),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
