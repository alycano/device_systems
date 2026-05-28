Python
from pydantic import BaseModel, Field, EmailStr
from enum import Enum

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

# 4. Esquema de Salida: Lo que la API devuelve al cliente (Fase 5 - Response Model)
class UserResponse(UserBase):
    id: int

    class Config:
        # Permite a Pydantic leer datos incluso si mapeamos objetos de bases de datos más adelante
        from_attributes = True