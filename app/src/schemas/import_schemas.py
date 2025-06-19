from pydantic import BaseModel
from typing import Optional
from datetime import date
from src.database.models.models import VehicleType


class VehicleCSVRow(BaseModel):
    license_plate: str
    make: str
    model: str
    year: int
    vehicle_type: VehicleType
    current_mileage: Optional[int]
    carrying_capacity: Optional[int]
    fuel_consumption_rate: Optional[float]


class ExpenseCSVRow(BaseModel):
    amount: float
    expense_date: date
    license_plate: str
    category_name: str
    description: str


class ImportResult(BaseModel):
    success_count: int
    error_count: int
    errors: list[dict] = []
