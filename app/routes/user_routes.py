from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserRole

router = APIRouter(prefix="/users", tags=["Users"])

# Base de datos simulada en memoria con registros iniciales
db_users: List[dict] = [
    {"id": 1, "name": "Aly Santiago Cano", "email": "aly@santiago.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Jhonatan Gomez", "email": "jhonatan@example.com", "role": "support", "is_active": True},
    {"id": 3, "name": "Cesar Builes", "email": "cesar@example.com", "role": "user", "is_active": False}
]

# --- Función Auxiliar para Cabeceras HTTP Personalizadas (Fase 5) ---
def add_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

# --- ENDPOINTS GET (FASE 3) ---

@router.get("", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[UserRole] = Query(None, description="Filtrar usuarios por rol administrativo u operativo"),
    is_active: Optional[bool] = Query(None, description="Filtrar usuarios por estado activo o inactivo")
):
    """
    Listar todos los usuarios del sistema. Permite la personalización de la respuesta
    mediante filtros opcionales de consulta (Query Parameters).
    """
    add_custom_headers(response)
    filtered_users = db_users

    # Aplicar filtro por rol si el parámetro está presente en la URL
    if role:
        filtered_users = [u for u in filtered_users if u["role"] == role]
    
    # Aplicar filtro por estado activo/inactivo
    if is_active is not None:
        filtered_users = [u for u in filtered_users if u["is_active"] == is_active]

    return filtered_users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response):
    """
    Obtener los detalles de un usuario específico utilizando su ID único 
    a través de un parámetro de ruta (Path Parameter).
    """
    add_custom_headers(response)
    
    # Buscar el usuario en la lista en memoria
    for user in db_users:
        if user["id"] == user_id:
            return user
            
    # Si el ID no existe, lanzar una excepción HTTP 404 estructurada
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Usuario con ID {user_id} no encontrado en el sistema"
    )