from typing import Optional
from pydantic import BaseModel


class RoleCreate(BaseModel):
    # Data control
    can_view_data: bool
    can_edit_vehicles: bool
    can_edit_employees: bool
    can_edit_expense_categories: bool

    # Integrations and data sourses
    can_view_data_sourses: bool
    can_create_data_sourses: bool
    can_import_from_files: bool
    can_edit_sync_settings: bool

    # Finansial ops
    can_create_expenses: bool
    can_approve_expenses: bool
    can_correct_expense_amounts: bool
    can_remove_expenses: bool

    # Moderation
    can_add_employees: bool
    can_create_roles: bool
    can_assign_roles: bool
    can_edit_roles: bool

    id_company: int


class RoleData(RoleCreate):
    id: int


class RoleEdit(BaseModel):
    # Data control
    can_view_data: Optional[bool] = None
    can_edit_vehicles: Optional[bool] = None
    can_edit_employees: Optional[bool] = None
    can_edit_expense_categories: Optional[bool] = None

    # Integrations and data sourses
    can_view_data_sourses: Optional[bool] = None
    can_create_data_sourses: Optional[bool] = None
    can_import_from_files: Optional[bool] = None
    can_edit_sync_settings: Optional[bool] = None

    # Finansial ops
    can_create_expenses: Optional[bool] = None
    can_approve_expenses: Optional[bool] = None
    can_correct_expense_amounts: Optional[bool] = None
    can_remove_expenses: Optional[bool] = None

    # Moderation
    can_add_employees: Optional[bool] = None
    can_create_roles: Optional[bool] = None
    can_assign_roles: Optional[bool] = None
    can_edit_roles: Optional[bool] = None
