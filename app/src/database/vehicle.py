from typing import Optional

from .general_db import BaseRepository

from ..schemas.vehicle import VehicleCreate, VehicleData, VehicleEdit
from .models.models import Vehicle
from .db import AsyncSession
from sqlalchemy import select


# Репозиторий для Vehicle
class VehicleRepository(
    BaseRepository[Vehicle, VehicleCreate, VehicleEdit, VehicleData]
):
    def __init__(self):
        super().__init__(Vehicle, VehicleData)

    async def get_by_license_plate(
        self, session: AsyncSession, plate: str, include_inactive: bool = False
    ) -> Optional[VehicleData]:
        """Поиск ТС по госномеру с учетом активности"""
        query = select(Vehicle).where(Vehicle.license_plate == plate)

        if not include_inactive:
            query = query.where(Vehicle.is_active == True)

        result = await session.execute(query)
        db_obj = result.scalars().first()
        return (
            self.data_schema.model_validate(db_obj, from_attributes=True)
            if db_obj
            else None
        )
