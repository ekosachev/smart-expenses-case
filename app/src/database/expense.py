from ..schemas.expense import ExpenseCreate, ExpenseData, ExpenseEdit
from .general_db import BaseRepository
from .models.models import Expense


class ExpenseRepository(
    BaseRepository[Expense, ExpenseCreate, ExpenseEdit, ExpenseData]
):
    def __init__(self):
        super().__init__(Expense, ExpenseData)
