from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from ..schemas.expense import ExpenseCreate, ExpenseData, ExpenseEdit
from ..services.expense import ExpenseService

from src.services.auth_utils import get_current_user

from ..database.db import get_session

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseData, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseService()
    return await service.create_expense(
        session, expense_data, user_id=current_user["id"]
    )


@router.get("/{expense_id}", response_model=ExpenseData)
async def get_expense(
    expense_id: int = Path(..., title="ID расхода"),
    session=Depends(get_session),
):
    service = ExpenseService()
    return await service.get_or_404(
        session, expense_id, error_message="Расход не найден"
    )


@router.get("/", response_model=list[ExpenseData])
async def list_expenses(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[int] = Query(None, title="Фильтр по ТС"),
    category_id: Optional[int] = Query(None, title="Фильтр по категории"),
    session=Depends(get_session),
):
    service = ExpenseService()
    filters = {}
    if vehicle_id:
        filters["vehicle_id"] = vehicle_id
    if category_id:
        filters["category_id"] = category_id

    return await service.get_entities(session, skip=skip, limit=limit, **filters)


@router.put("/{expense_id}", response_model=ExpenseData)
async def update_expense(
    expense_data: ExpenseEdit,
    expense_id: int = Path(..., title="ID расхода"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseService()
    return await service.update_entity(session, expense_id, expense_data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int = Path(..., title="ID расхода"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseService()
    success = await service.delete_entity(session, expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Расход не найден"
        )


@router.post("/{expense_id}/approve", response_model=ExpenseData)
async def approve_expense(
    expense_id: int = Path(..., title="ID расхода"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = ExpenseService()
    return await service.approve_expense(
        session, expense_id, approver_id=current_user["id"]
    )


@router.get("/by-vehicle/{vehicle_id}", response_model=list[ExpenseData])
async def get_expenses_by_vehicle(
    vehicle_id: int = Path(..., title="ID транспортного средства"),
    skip: int = 0,
    limit: int = 100,
    session=Depends(get_session),
):
    service = ExpenseService()
    return await service.get_expenses_by_vehicle(
        session, vehicle_id, offset=skip, limit=limit
    )
