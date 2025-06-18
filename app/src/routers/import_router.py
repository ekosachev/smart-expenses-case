from fastapi import APIRouter, UploadFile, File, Form, Depends, Query
from src.services.import_service import ImportService
from src.schemas.import_schemas import VehicleCSVRow, ExpenseCSVRow, ImportResult

from src.database.db import get_session
from src.services.auth_utils import get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/import", tags=["Data Import"])
import_service = ImportService()


# Общие параметры для импорта
async def common_import_params(
    file: UploadFile = File(...),
    company_id: int = Form(...),
    file_format: str = Query("csv", description="Формат файла: csv или xlsx"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Определяем формат по расширению файла, если не указан
    if file_format == "auto":
        if file.filename is None:
            raise HTTPException(status_code=400, detail="Некорректное имя файла")
        if file.filename.endswith(".xlsx"):
            file_format = "xlsx"
        else:
            file_format = "csv"

    try:
        # Читаем данные из файла
        data = import_service.read_upload_file(file, file_format)
        return {
            "data": data,
            "company_id": company_id,
            "user_id": current_user["id"],
            "session": session,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vehicles", response_model=ImportResult)
async def import_vehicles(params: dict = Depends(common_import_params)):
    return await import_service.import_vehicles(
        params["session"], params["data"], params["company_id"], params["user_id"]
    )


@router.post("/expenses", response_model=ImportResult)
async def import_expenses(params: dict = Depends(common_import_params)):
    return await import_service.import_expenses(
        params["session"], params["data"], params["company_id"], params["user_id"]
    )


@router.get("/template/vehicles")
async def download_vehicles_template(
    format: str = Query("xlsx", description="Формат шаблона: csv или xlsx"),
):
    """Скачать шаблон для импорта ТС"""
    columns = list(VehicleCSVRow.model_json_schema()["properties"].keys())
    return import_service.generate_template(format, columns)


@router.get("/template/expenses")
async def download_expenses_template(
    format: str = Query("xlsx", description="Формат шаблона: csv или xlsx"),
):
    """Скачать шаблон для импорта расходов"""
    columns = list(ExpenseCSVRow.model_json_schema()["properties"].keys())
    return import_service.generate_template(format, columns)

