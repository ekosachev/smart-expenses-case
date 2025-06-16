from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status

from src.database.db import get_session
from src.services.auth_utils import get_current_user
from src.services.import_service import ImportService
from src.schemas.import_schemas import ImportResult

router = APIRouter(prefix="/import", tags=["Data Import"])


@router.post("/vehicles/{company_id}/csv", response_model=ImportResult)
async def import_vehicles_csv(
    company_id: int,
    file: UploadFile = File(..., description="CSV файл с данными ТС"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Проверка типа файла
    if file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректное имя файла"
        )
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только CSV файлы",
        )

    # Чтение содержимого файла
    content = await file.read()
    try:
        csv_content = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неподдерживаемая кодировка файла. Используйте UTF-8",
        )

    # Импорт данных
    return await ImportService.import_vehicles_from_csv(
        session, csv_content, company_id, current_user["id"]
    )


@router.post("/expenses/{company_id}/csv", response_model=ImportResult)
async def import_expenses_csv(
    company_id: int,
    file: UploadFile = File(..., description="CSV файл с данными расходов"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Проверка типа файла
    if file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректное имя файла"
        )
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поддерживаются только CSV файлы",
        )

    # Чтение содержимого файла
    content = await file.read()
    try:
        csv_content = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неподдерживаемая кодировка файла. Используйте UTF-8",
        )

    # Импорт данных
    return await ImportService.import_expenses_from_csv(
        session, csv_content, company_id, current_user["id"]
    )
