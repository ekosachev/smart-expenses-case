from typing import Optional
from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str


class CompanyData(CompanyCreate):
    id: int


class CompanyEdit(BaseModel):
    name: Optional[str] = None
