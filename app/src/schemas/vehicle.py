from datetime import date
from typing import Optional

from pydantic import BaseModel


class VehicleCreate(BaseModel):
    company_id: int
    license_plate: str
    make: str
    model: str
    year: int
    vehicle_type: str
    fuel_type: str
    vin: Optional[str] = None
    registration_certificate: Optional[str] = None
    insurance_policy: Optional[str] = None
    carrying_capacity: Optional[int] = None
    fuel_consumption_rate: Optional[float] = None
    current_mileage: Optional[int] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    initial_cost: Optional[float] = None
    residual_value: Optional[float] = None
    current_driver_id: Optional[int] = None
    department_id: Optional[int] = None


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
    vehicle_type: Optional[str] = None
    fuel_type: Optional[str] = None
    vin: Optional[str] = None
    registration_certificate: Optional[str] = None
    insurance_policy: Optional[str] = None
    carrying_capacity: Optional[int] = None
    fuel_consumption_rate: Optional[float] = None
    current_mileage: Optional[int] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    initial_cost: Optional[float] = None
    residual_value: Optional[float] = None
    current_driver_id: Optional[int] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
