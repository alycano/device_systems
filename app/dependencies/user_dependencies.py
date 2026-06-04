# app/dependencies/user_dependencies.py
from fastapi import HTTPException, status, Path
from app.data.users_db import users_db

# Dependencia para buscar un usuario por ID. Si no existe, lanza un 404 de inmediato.
def get_user_or_404(user_id: int = Path(..., description="ID numérico del usuario a consultar", gt=0)) -> dict:
    for user in users_db:
        if user["id"] == user_id:
            return user
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

# Validador de negocio para evitar correos duplicados (Fase 6)
def verificar_email_duplicado(email: str, excluir_id: int = None):
    for user in users_db:
        if user["email"] == email.lower() and user["id"] != excluir_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este email"
            )