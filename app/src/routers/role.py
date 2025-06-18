from fastapi import APIRouter, status, Depends, Path, HTTPException

from src.database.db import get_session
from src.schemas.role import RoleCreate, RoleData, RoleEdit
from src.services.auth_utils import get_current_user
from src.services.role import RoleService

router = APIRouter(prefix="/role", tags=["Access Roles"])


@router.post("/", response_model=RoleData, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    session=Depends(get_current_user),
    current_user=Depends(get_session),
):
    service = RoleService()
    return await service.create_entity(session, role_data)


@router.get("/{role_id}", response_model=RoleData)
async def get_role(
    role_id: int = Path(..., title="ID роли"),
    session=Depends(get_session),
):
    service = RoleService()
    return await service.get_or_404(session, role_id, error_message="Роль не найдена")


@router.get("/", response_model=list[RoleData])
async def list_roles(skip: int = 0, limit: int = 100, session=Depends(get_session)):
    service = RoleService()
    return await service.get_entities(session, skip=skip, limit=limit)


@router.put("/{role_id}", response_model=RoleData)
async def update_role(
    role_data: RoleEdit,
    role_id: int = Path(..., title="ID роли"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = RoleService()
    return await service.update_entity(session, role_id, role_data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    role_id: int = Path(..., title="ID роли"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = RoleService()
    success = await service.delete_entity(session, role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Роль не найдена",
        )


@router.post("/{role_id}/restore", response_model=RoleData)
async def restore_category(
    role_id: int = Path(..., title="ID категории расходов"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = RoleService()
    success = await service.restore_entity(session, role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Роль не найдена или уже активна",
        )
    return await service.get_or_404(session, role_id, error_message="Роль не найдена")
