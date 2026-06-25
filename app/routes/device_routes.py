from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin, require_admin_only
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/", response_model=List[DeviceResponse])
def read_devices(
    device_type: Optional[str] = Query(None, description="Filtrar por tipo de equipo"),
    is_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    search: Optional[str] = Query(None, description="Buscar por nombre o número de serie"),
    db: Session = Depends(get_db)
):
    return DeviceService.get_all(db, device_type=device_type, is_available=is_available, search=search)

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    db_device = DeviceService.get_by_serial(db, device.serial_number)
    if db_device:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    return DeviceService.create(db, device)

@router.get("/{device_id}", response_model=DeviceResponse)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = DeviceService.get_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db_device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    db_device = DeviceService.get_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return DeviceService.update(db, db_device, device_data)

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_only)
):
    db_device = DeviceService.get_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    DeviceService.delete(db, db_device)
    return None