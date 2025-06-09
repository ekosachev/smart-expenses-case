from fastapi import APIRouter, status, Depends, Path, HTTPException
from ..schemas.vehicle import VehicleCreate, VehicleData, VehicleEdit
from ..services.vehicle import VehicleService
from src.database.db import get_session
from src.services.auth_utils import get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleData, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = VehicleService()
    return await service.create_vehicle(
        session, vehicle_data, user_id=current_user["id"]
    )


@router.get("/{vehicle_id}", response_model=VehicleData)
async def get_vehicle(
    session=Depends(get_session),
    vehicle_id: int = Path(..., title="ID транспортного средства"),
):
    service = VehicleService()
    return await service.get_or_404(
        session, vehicle_id, error_message="Транспортное средство не найдено"
    )


@router.get("/", response_model=list[VehicleData])
async def list_vehicles(
    session=Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
):
    service = VehicleService()
    return await service.get_entities(
        session, skip=skip, limit=limit, include_inactive=include_inactive
    )


@router.put("/{vehicle_id}", response_model=VehicleData)
async def update_vehicle(
    vehicle_data: VehicleEdit,
    vehicle_id: int = Path(..., title="ID транспортного средства"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = VehicleService()
    return await service.update_vehicle(
        session, vehicle_id, vehicle_data, user_id=current_user["id"]
    )


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: int = Path(..., title="ID транспортного средства"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = VehicleService()
    success = await service.delete_entity(session, vehicle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Транспортное средство не найдено",
        )


@router.post("/{vehicle_id}/restore", response_model=VehicleData)
async def restore_vehicle(
    vehicle_id: int = Path(..., title="ID транспортного средства"),
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    service = VehicleService()
    success = await service.restore_entity(session, vehicle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Транспортное средство не найдено или уже активно",
        )
    return await service.get_or_404(
        session, vehicle_id, error_message="Транспортное средство не найдено"
    )


@router.get("/by-license/{license_plate}", response_model=VehicleData)
async def get_vehicle_by_plate(
    license_plate: str = Path(..., title="Госномер транспортного средства"),
    session=Depends(get_session),
):
    service = VehicleService()
    vehicle = await service.repository.get_by_license_plate(session, license_plate)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Транспортное средство не найдено",
        )
    return vehicle
