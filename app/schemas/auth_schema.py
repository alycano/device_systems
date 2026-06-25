from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ConfigDict
from typing import Optional
from enum import Enum
import re

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"

class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=8, description="Contraseña segura")
    role: UserRole = Field(default=UserRole.USER, description="Rol del usuario")

    @field_validator("password")
    @classmethod
    def validar_contrasena(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contrasena debe tener al menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contrasena debe contener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contrasena debe contener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("La contrasena debe contener al menos un numero")
        if " " in v:
            raise ValueError("La contrasena no puede contener espacios en blanco")
        return v

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico registrado")
    password: str = Field(..., min_length=1, description="Contraseña del usuario")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)