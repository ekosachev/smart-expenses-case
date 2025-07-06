from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.expense import ExpenseCreate, ExpenseData, ExpenseEdit
from .general_db import BaseRepository
from .models.models import Expense


class ExpenseRepository(
    BaseRepository[Expense, ExpenseCreate, ExpenseEdit, ExpenseData]
):
    def __init__(self):
        super().__init__(Expense, ExpenseData)

    async def get_by_vehicle(
        self,
        session: AsyncSession,
        vehicle_id: int,
        offset: int = 0,
        limit: Optional[int] = 100,
    ) -> list[ExpenseData]:
        query = select(Expense).where(Expense.vehicle_id == vehicle_id).offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return [
            ExpenseData.model_validate(expense, from_attributes=True)
            for expense in (await session.execute(query))
        ]
