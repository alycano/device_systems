# app/schemas/loan_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Esquema básico para solicitar un préstamo
class LoanBase(BaseModel):
    user_id: int = Field(..., gt=0, description="ID del usuario (aprendiz/instructor)")
    device_id: int = Field(..., gt=0, description="ID del dispositivo solicitado")

class LoanCreate(LoanBase):
    pass

# Esquema para responder de forma simple
class LoanResponse(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True

# --- ESTRUCTURAS ANIDADAS PARA JOINS AVANZADOS (Fase 7) ---

class UserMinResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class DeviceMinResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    class Config:
        from_attributes = True

# Esquema de respuesta detallada que combina las tres entidades
class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]
    user: UserMinResponse       # Información anidada del usuario
    device: DeviceMinResponse   # Información anidada del dispositivo

    class Config:
        from_attributes = True