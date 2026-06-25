from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="El nombre debe tener al menos 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo electrónico con formato válido")
    role: UserRole = Field(default=UserRole.USER, description="Roles permitidos: admin, support, user")
    is_active: bool = Field(default=True, description="Estado de actividad del usuario")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Contraseña del usuario (mínimo 8 caracteres)")

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8, description="Nueva contraseña (opcional)")

class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Modificación opcional del nombre")
    email: Optional[EmailStr] = Field(None, description="Modificación opcional del correo electrónico")
    password: Optional[str] = Field(None, min_length=8, description="Modificación opcional de la contraseña")
    role: Optional[UserRole] = Field(None, description="Modificación opcional del rol operativo")
    is_active: Optional[bool] = Field(None, description="Modificación opcional del estado de actividad")

    @field_validator('name')
    def validar_nombre_no_vacio(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('El nombre no puede estar vacío ni contener solo espacios en blanco')
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True