# app/schemas/device_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Esquema base con los atributos comunes
class DeviceBase(BaseModel):
    name: str = Field(..., min_length=2, description="Nombre o modelo del dispositivo")
    serial_number: str = Field(..., description="Número de serie único de hardware")
    device_type: str = Field(..., description="Tipo de dispositivo: laptop, tablet, proyector, etc.")
    brand: Optional[str] = Field(None, description="Marca del fabricante")
    is_available: bool = Field(default=True, description="Disponibilidad actual para préstamos")

# Esquema para recibir datos al crear un dispositivo
class DeviceCreate(DeviceBase):
    pass

# Esquema para actualizar un dispositivo por completo
class DeviceUpdate(DeviceBase):
    pass

# Esquema para respuestas de la API (añade ID y fecha de registro)
class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True