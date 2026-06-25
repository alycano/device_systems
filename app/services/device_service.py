# app/services/device_service.py
from sqlalchemy.orm import Session
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate

class DeviceService:
    @staticmethod
    def get_all(db: Session, device_type: str = None, is_available: bool = None, search: str = None):
        query = db.query(Device)
        if device_type:
            query = query.filter(Device.device_type == device_type)
        if is_available is not None:
            query = query.filter(Device.is_available == is_available)
        if search:
            query = query.filter(
                Device.name.ilike(f"%{search}%") | Device.serial_number.ilike(f"%{search}%")
            )
        return query.all()

    @staticmethod
    def get_by_id(db: Session, device_id: int):
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_by_serial(db: Session, serial_number: str):
        return db.query(Device).filter(Device.serial_number == serial_number).first()

    @staticmethod
    def create(db: Session, device_data: DeviceCreate):
        db_device = Device(
            name=device_data.name,
            serial_number=device_data.serial_number,
            device_type=device_data.device_type,
            brand=device_data.brand,
            is_available=device_data.is_available
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    @staticmethod
    def update(db: Session, db_device: Device, device_data: DeviceUpdate):
        for key, value in device_data.model_dump(exclude_unset=True).items():
            setattr(db_device, key, value)
        db.commit()
        db.refresh(db_device)
        return db_device

    @staticmethod
    def delete(db: Session, db_device: Device):
        db.delete(db_device)
        db.commit()