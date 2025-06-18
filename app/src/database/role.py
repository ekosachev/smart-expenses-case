from src.database.general_db import BaseRepository
from src.database.models.models import Role
from src.schemas.role import RoleCreate, RoleData, RoleEdit


class RoleRepository(BaseRepository[Role, RoleCreate, RoleEdit, RoleData]):
    def __init__(self):
        super().__init__(Role, RoleData)
