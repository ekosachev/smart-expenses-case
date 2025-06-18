from src.database.general_db import BaseRepository
from src.database.models.models import Company
from src.schemas.company import CompanyCreate, CompanyData, CompanyEdit


class CompanyRepository(
    BaseRepository[Company, CompanyCreate, CompanyEdit, CompanyData]
):
    def __init__(self):
        super().__init__(Company, CompanyData)
