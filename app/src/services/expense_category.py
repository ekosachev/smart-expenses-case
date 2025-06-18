from .general_service import BaseService
from ..database.expense_category import ExpenseCategoryRepository


class ExpenseCategoryService(BaseService):
    def __init__(self):
        super().__init__(ExpenseCategoryRepository())
