from src.database.company import CompanyRepository
from src.services.general_service import BaseService


class CompanyService(BaseService):
    def __init__(self):
        super().__init__(CompanyRepository())
