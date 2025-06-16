from typing import Optional

from pydantic import BaseModel, Field


class ExpenseCategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)
    code: str = Field(..., max_length=10)


class ExpenseCategoryData(ExpenseCategoryCreate):
    id: int


class ExpenseCategoryEdit(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    code: Optional[str] = Field(None, max_length=10)
