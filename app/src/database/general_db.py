from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models.base import Base

# Generic типы для моделей и схем
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
EditSchemaType = TypeVar("EditSchemaType", bound=BaseModel)
DataSchemaType = TypeVar("DataSchemaType", bound=BaseModel)


class BaseRepository(
    Generic[ModelType, CreateSchemaType, EditSchemaType, DataSchemaType]
):
    def __init__(self, model: Type[ModelType], data_schema: Type[DataSchemaType]):
        self.model = model
        self.data_schema = data_schema
        self.supports_soft_delete = hasattr(model, "is_active")

    async def create(
        self, session: AsyncSession, data: CreateSchemaType, **kwargs: Any
    ) -> DataSchemaType:
        """Создание новой сущности"""
        create_data = data.model_dump()
        create_data["is_active"] = True

        db_obj = self.model(**create_data, **kwargs)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return self.data_schema.model_validate(db_obj, from_attributes=True)

    async def get(self, session: AsyncSession, id: int) -> Optional[DataSchemaType]:
        """Получение активной сущности по ID"""
        query = (
            select(self.model).where(self.model.id == id).where(self.model.is_active)
        )

        result = await session.execute(query)
        db_obj = result.scalars().first()
        return (
            self.data_schema.model_validate(db_obj, from_attributes=True)
            if db_obj
            else None
        )

    async def get_all(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: Optional[int] = 100,
        include_inactive: bool = False,
    ) -> List[DataSchemaType]:
        """Получение списка сущностей с пагинацией"""
        query = select(self.model).offset(skip)

        if limit is not None:
            query.limit(limit)

        if not include_inactive:
            query = query.where(self.model.is_active)

        result = await session.execute(query)
        return [
            self.data_schema.model_validate(obj, from_attributes=True)
            for obj in result.scalars()
        ]

    async def update(
        self, session: AsyncSession, id: int, data: EditSchemaType
    ) -> Optional[DataSchemaType]:
        """Обновление активной сущности"""
        # Получаем существующий активный объект
        existing = await self.get(session, id)
        if not existing:
            return None

        # Обновляем только переданные поля
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return existing  # Ничего не обновляем

        # Условия для обновления
        where_conditions = [self.model.id == id]
        where_conditions.append(self.model.is_active == True)

        # Выполняем обновление
        await session.execute(
            update(self.model).where(and_(*where_conditions)).values(**update_data)
        )
        await session.commit()

        # Получаем обновленный объект
        return await self.get(session, id)

    async def delete(self, session: AsyncSession, id: int) -> bool:
        where_conditions = [self.model.id == id]
        where_conditions.append(self.model.is_active == True)

        result = await session.execute(
            update(self.model).where(and_(*where_conditions)).values(is_active=False)
        )
        await session.commit()
        return result.rowcount > 0

    async def restore(self, session: AsyncSession, id: int) -> bool:
        result = await session.execute(
            update(self.model).where(self.model.id == id).values(is_active=True)
        )
        await session.commit()
        return result.rowcount > 0
