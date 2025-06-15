from typing import TypeVar, Optional, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

# Generic типы для схем
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
EditSchemaType = TypeVar("EditSchemaType", bound=BaseModel)
DataSchemaType = TypeVar("DataSchemaType", bound=BaseModel)


class BaseService:
    def __init__(self, repository):
        self.repository = repository

    async def create_entity(
        self, session: AsyncSession, data: CreateSchemaType, **kwargs: Any
    ) -> DataSchemaType:
        """Создание сущности"""
        return await self.repository.create(session, data, **kwargs)

    async def get_entity(
        self, session: AsyncSession, entity_id: int
    ) -> Optional[DataSchemaType]:
        """Получение сущности по ID"""
        return await self.repository.get(session, entity_id)

    async def get_entities(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: Optional[int] = 100,
        **filters: Any,
    ) -> list[DataSchemaType]:
        """Получение списка сущностей с фильтрацией"""
        return await self.repository.get_all(session, skip=skip, limit=limit, **filters)

    async def update_entity(
        self, session: AsyncSession, entity_id: int, data: EditSchemaType
    ) -> Optional[DataSchemaType]:
        """Обновление сущности"""
        return await self.repository.update(session, entity_id, data)

    async def delete_entity(self, session: AsyncSession, entity_id: int) -> bool:
        """Удаление сущности"""
        return await self.repository.delete(session, entity_id)

    async def restore_entity(self, session: AsyncSession, entity_id: int) -> bool:
        """Восстановление сущности (если поддерживается)"""
        if hasattr(self.repository, "restore"):
            return await self.repository.restore(session, entity_id)
        return False

    async def get_or_404(
        self,
        session: AsyncSession,
        entity_id: int,
        error_message: str = "Entity not found",
    ) -> DataSchemaType:
        """Получение сущности с обработкой ошибки 404"""
        entity = await self.get_entity(session, entity_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        return entity

    async def create_with_relation_check(
        self,
        session: AsyncSession,
        data: CreateSchemaType,
        relation_service: "BaseService",
        relation_id: int,
        relation_field: str,
        relation_error: str = "Related entity not found",
        **kwargs: Any,
    ) -> DataSchemaType:
        """Создание сущности с проверкой связанной сущности"""
        # Проверяем существование связанной сущности
        _ = await relation_service.get_or_404(
            session, relation_id, error_message=relation_error
        )

        # Создаем новую сущность
        return await self.create_entity(
            session, data, **{relation_field: relation_id}, **kwargs
        )
