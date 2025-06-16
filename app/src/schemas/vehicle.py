from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.database.models.models import VehicleType


class VehicleCreate(BaseModel):
    company_id: int
    license_plate: str
    make: str
    model: str
    year: int
    vehicle_type: VehicleType
    carrying_capacity: Optional[int] = None
    fuel_consumption_rate: Optional[float] = None
    current_mileage: Optional[int] = None
    initial_cost: Optional[float] = None
    rent_price: Optional[float] = None


class VehicleData(VehicleCreate):
    id: int
    is_active: bool
    created_at: date
    updated_at: date
    created_by: Optional[int] = None


class VehicleEdit(BaseModel):
    license_plate: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vehicle_type: Optional[VehicleType] = None
    carrying_capacity: Optional[int] = None
    fuel_consumption_rate: Optional[float] = None
    current_mileage: Optional[int] = None
    initial_cost: Optional[float] = None
    is_active: Optional[bool] = None
    rent_price: Optional[float] = None
