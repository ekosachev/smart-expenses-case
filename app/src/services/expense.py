from src.services.company import CompanyService
from .general_service import BaseService
from fastapi import HTTPException, status

from ..database.db import AsyncSession
from ..database.expense import ExpenseRepository
from .schemas.expense import ExpenseCreate, ExpenseData, ExpenseEdit
from .expense_category import ExpenseCategoryService
from .vehicle import VehicleService


class ExpenseService(BaseService):
    """Сервис для работы с расходами"""

    def __init__(self):
        super().__init__(ExpenseRepository())

    async def create_expense(
        self, session: AsyncSession, data: ExpenseCreate, user_id: int
    ) -> ExpenseData:
        """Создание расхода с автоматической привязкой"""
        # Проверка существования категории
        category_service = ExpenseCategoryService()
        await category_service.get_or_404(
            session, data.category_id, error_message="Категория расходов не найдена"
        )

        # Проверка существования ТС (если указано)
        if data.vehicle_id:
            vehicle_service = VehicleService()
            await vehicle_service.get_or_404(
                session,
                data.vehicle_id,
                error_message="Транспортное средство не найдено",
            )

        company_service = CompanyService()
        await company_service.get_or_404(
            session, data.company_id, "Компания не найдена"
        )

        if data.amount <= 0:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Нельзя создать расход с нулевой или отрицательной суммой",
            )

        return await self.create_entity(session, data, created_by=user_id)

    async def get_expenses_by_vehicle(
        self, session: AsyncSession, vehicle_id: int, offset: int = 0, limit: int = 100
    ) -> list[ExpenseData]:
        """Получение расходов по ТС"""
        vehicle_service = VehicleService()
        await vehicle_service.get_or_404(
            session, vehicle_id, "Транспортное средство не найдено"
        )
        return await self.repository.get_by_vehicle(
            session, vehicle_id, offset=offset, limit=limit
        )

    async def approve_expense(
        self, session: AsyncSession, expense_id: int, approver_id: int
    ) -> ExpenseData | None:
        """Утверждение расхода"""
        await self.get_or_404(session, expense_id)

        # Обновляем статус и утверждающего пользователя
        return await self.update_entity(
            session, expense_id, ExpenseEdit(status="approved", approver_id=approver_id)
        )
