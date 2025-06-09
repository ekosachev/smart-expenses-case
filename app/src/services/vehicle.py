from .general_service import BaseService
from ..database.vehicle import VehicleRepository
from ..database.db import AsyncSession
from ..schemas.vehicle import VehicleCreate, VehicleEdit, VehicleData
from fastapi import HTTPException
from fastapi import status


class VehicleService(BaseService):
    """Сервис для работы с транспортными средствами"""

    def __init__(self):
        super().__init__(VehicleRepository())

    async def create_vehicle(
        self, session: AsyncSession, data: VehicleCreate, user_id: int
    ) -> VehicleData:
        """Создание ТС с проверкой уникальности госномера"""
        # Проверка уникальности госномера среди активных ТС
        existing = await self.repository.get_by_license_plate(
            session, data.license_plate
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Транспортное средство с таким госномером уже существует",
            )

        return await self.create_entity(session, data, created_by=user_id)

    async def update_vehicle(
        self, session: AsyncSession, vehicle_id: int, data: VehicleEdit, user_id: int
    ) -> VehicleData | None:
        if data.license_plate:
            existing = await self.repository.get_by_license_plate(
                session, data.license_plate, include_inactive=True
            )
            if existing and existing.id != vehicle_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Транспортное средство с таким госномером уже существует",
                )

        return await self.update_entity(session, vehicle_id, data)
