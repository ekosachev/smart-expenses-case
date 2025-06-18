from ..schemas.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryData,
    ExpenseCategoryEdit,
)
from .general_db import BaseRepository
from .models.models import ExpenseCategory


class ExpenseCategoryRepository(
    BaseRepository[
        ExpenseCategory, ExpenseCategoryCreate, ExpenseCategoryEdit, ExpenseCategoryData
    ]
):
    def __init__(self):
        super().__init__(ExpenseCategory, ExpenseCategoryData)
