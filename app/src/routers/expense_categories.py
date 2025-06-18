from fastapi import APIRouter, status, Depends, Path, HTTPException
from ..schemas.expense_category import (
    ExpenseCategoryCreate,
    ExpenseCategoryData,
    ExpenseCategoryEdit,
)
from ..services.expense_category import ExpenseCategoryService
from src.database.db import get_session
from src.services.auth_utils import get_current_user

router = APIRouter(prefix="/expense-categories", tags=["Expense Categories"])


@router.post(
    "/", response_model=ExpenseCategoryData, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_data: ExpenseCategoryCreate,
    session=Depends(get_current_user),
    current_user=Depends(get_session),
):
    service = ExpenseCategoryService()
    return await service.create_entity(session, category_data)


@router.get("/{category_id}", response_model=ExpenseCategoryData)
async def get_category(
    category_id: int = Path(..., title="ID категории расходов"),
    session=Depends(get_session),
):
    service = ExpenseCategoryService()
    return await service.get_or_404(
        session, category_id, error_message="Категория расходов не найдена"
    )


@router.get("/", response_model=list[ExpenseCategoryData])
async def list_categories(
    skip: int = 0, limit: int = 100, session=Depends(get_session)
):
    service = ExpenseCategoryService()
    return await service.get_entities(session, skip=skip, limit=limit)


@router.put("/{category_id}", response_model=ExpenseCategoryData)
async def update_category(
    category_data: ExpenseCategoryEdit,
    category_id: int = Path(..., title="ID категории расходов"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseCategoryService()
    return await service.update_entity(session, category_id, category_data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., title="ID категории расходов"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseCategoryService()
    success = await service.delete_entity(session, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория расходов не найдена",
        )


@router.post("/{category_id}/restore", response_model=ExpenseCategoryData)
async def restore_category(
    category_id: int = Path(..., title="ID категории расходов"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseCategoryService()
    success = await service.restore_entity(session, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория расходов не найдена или уже активна",
        )
    return await service.get_or_404(
        session, category_id, error_message="Категория расходов не найдена"
    )
