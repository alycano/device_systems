from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
from typing import Optional

# 1. Definimos un Enum para restringir los roles permitidos
class UserRole(str, Enum):
    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"

# 2. Esquema Base: Define los atributos comunes y sus validaciones
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="El nombre debe tener al menos 3 caracteres")
    email: EmailStr = Field(..., description="Debe ser un correo electrónico con formato válido")
    role: UserRole = Field(default=UserRole.USER, description="Roles permitidos: admin, support, user")
    is_active: bool = Field(default=True, description="Estado de actividad del usuario")

# 3. Esquema de Entrada: Lo que el cliente envía al registrar un usuario (Fase 4)
class UserCreate(UserBase):
    id: int = Field(..., gt=0, description="ID único y obligatorio, debe ser mayor a cero")

# 3.5 Esquema de Modificación Parcial: Requerido para el método PATCH (Fase 3 de la guía)
class UserUpdateParcial(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Modificación opcional del nombre")
    email: Optional[EmailStr] = Field(None, description="Modificación opcional del correo electrónico")
    role: Optional[UserRole] = Field(None, description="Modificación opcional del rol operativo")
    is_active: Optional[bool] = Field(None, description="Modificación opcional del estado de actividad")

    @field_validator('name')
    def validar_nombre_no_vacio(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('El nombre no puede estar vacío ni contener solo espacios en blanco')
        return v

# 4. Esquema de Salida: Lo que la API devuelve al cliente (Fase 5 - Response Model)
class UserResponse(UserBase):
    id: int

    class Config:
        # Permite a Pydantic leer datos incluso si mapeamos objetos de bases de datos más adelante
        from_attributes = True