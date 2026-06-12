from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
from typing import Optional
from datetime import datetime

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

# 3. Esquema de Entrada: Lo que el cliente envía al registrar un usuario (POST)
# Nota: Quitamos el ID obligatorio de aquí porque SQLAlchemy lo autogenera de forma incremental en la BD
class UserCreate(UserBase):
    pass

# 4. Esquema de Actualización Completa (PUT)
class UserUpdate(UserBase):
    pass

# 5. Esquema de Modificación Parcial: Requerido para el método PATCH (Invocado como UserPatch)
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Modificación opcional del nombre")
    email: Optional[EmailStr] = Field(None, description="Modificación opcional del correo electrónico")
    role: Optional[UserRole] = Field(None, description="Modificación opcional del rol operativo")
    is_active: Optional[bool] = Field(None, description="Modificación opcional del estado de actividad")

    @field_validator('name')
    def validar_nombre_no_vacio(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('El nombre no puede estar vacío ni contener solo espacios en blanco')
        return v

# 6. Esquema de Salida: Lo que la API devuelve al cliente (Response Model)
class UserResponse(UserBase):
    id: int
    created_at: datetime  # Incluido para cumplir con la Fase 5 del modelo de datos de la guía

    class Config:
        # Permite a Pydantic mapear de forma directa los objetos de la base de datos de SQLAlchemy
        from_attributes = True