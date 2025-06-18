from src.database.role import RoleRepository
from src.services.general_service import BaseService


class RoleService(BaseService):
    def __init__(self):
        super().__init__(RoleRepository())
