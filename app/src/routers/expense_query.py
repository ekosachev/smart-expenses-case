from fastapi import APIRouter, Depends

from src.database.db import get_session
from src.schemas.expense_query import ExpenseQueryResponse, ExpenseQuery
from src.services.auth_utils import get_current_user
from src.services import expense_query as service

router = APIRouter(prefix="/expense_query", tags=["Query expenses"])


@router.post("", response_model=ExpenseQueryResponse)
async def expense_query(
    data: ExpenseQuery, user=Depends(get_current_user), session=Depends(get_session)
):
    return await service.expense_query(session, data)
