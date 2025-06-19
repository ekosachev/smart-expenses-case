from fastapi import APIRouter, status, Depends, Path, HTTPException

from src.database.db import get_session
from src.schemas.company import CompanyCreate, CompanyData, CompanyEdit
from src.services.auth_utils import get_current_user
from src.services.company import CompanyService

router = APIRouter(prefix="/company", tags=["Companies"])


@router.post("/", response_model=CompanyData, status_code=status.HTTP_201_CREATED)
async def company_create(
    company_data: CompanyCreate,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = CompanyService()
    return await service.create_entity(session, company_data)


@router.get("/{company_id}", response_model=CompanyData)
async def get_company(
    company_id: int = Path(..., title="ID компании"),
    session=Depends(get_session),
):
    service = CompanyService()
    return await service.get_or_404(
        session, company_id, error_message="Компания не найдена"
    )


@router.get("/", response_model=list[CompanyData])
async def list_companies(skip: int = 0, limit: int = 100, session=Depends(get_session)):
    service = CompanyService()
    return await service.get_entities(session, skip=skip, limit=limit)


@router.put("/{company_id}", response_model=CompanyData)
async def update_company(
    company_data: CompanyEdit,
    company_id: int = Path(..., title="ID компании"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = CompanyService()
    return await service.update_entity(session, company_id, company_data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int = Path(..., title="ID компании"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = CompanyService()
    success = await service.delete_entity(session, company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Роль не найдена",
        )


@router.post("/{company_id}/restore", response_model=CompanyData)
async def restore_company(
    company_id: int = Path(..., title="ID компании"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = CompanyService()
    success = await service.restore_entity(session, company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена или уже активна",
        )
    return await service.get_or_404(
        session, company_id, error_message="Компания не найдена"
    )
