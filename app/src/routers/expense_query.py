from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from src.database.db import get_session
from src.schemas.expense_query import ExpenseQueryResponse, ExpenseQuery
from src.services.auth_utils import get_current_user
from src.services import expense_query as service
from src.services import llm_model as llm_service

router = APIRouter(prefix="/expense_query", tags=["Query expenses"])


@router.post("", response_model=dict)
async def expense_query(
    data: ExpenseQuery, user=Depends(get_current_user), session=Depends(get_session)
):
    try:
        result = (await service.expense_query(session, data)).model_dump()
    except ValueError as e:
        result = {"message": str(e)}
    return result


@router.post("/report")
async def expenses_report(
    data: ExpenseQuery, user=Depends(get_current_user), session=Depends(get_session)
):
    expense_data = await service.expense_query(session, data)
    filepath = await llm_service.get_llm_analysis(expense_data)
    return FileResponse(filepath, media_type="application/pdf")
