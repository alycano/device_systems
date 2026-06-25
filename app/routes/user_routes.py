# app/routes/user_routes.py
from fastapi import APIRouter, Depends, status, HTTPException, Query, Response, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_schema import UserResponse, UserCreate, UserPatch, UserUpdate
from app.services.user_service import UserService
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.middlewares.rate_limiter import limiter

router = APIRouter(prefix="/users", tags=["Users"])

def add_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"

@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar y filtrar usuarios",
    description="Listar todos los usuarios de la base de datos. Requiere autenticación."
)
@limiter.limit("30/minute")
def get_users(
    request: Request,
    response: Response,
    role: Optional[str] = Query(None, description="Filtrar usuarios por rol (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filtrar usuarios por estado activo o inactivo"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    add_custom_headers(response)
    return UserService.get_all(db, role=role, is_active=is_active)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Obtener los detalles de un usuario específico. Requiere autenticación."
)
def get_user_by_id(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    add_custom_headers(response)
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
    description="Registrar un nuevo usuario en la base de datos SQLite. Valida restricciones de unicidad sobre el correo electrónico."
)
def create_user(
    user_in: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    add_custom_headers(response)
    existing_user = UserService.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    return UserService.create(db, user_in)

# --- ENDPOINTS PUT Y PATCH (FASE 9 Y 10) ---

@router.put(
    "/{user_id}", 
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK,
    summary="Actualización completa (PUT)",
    description="Reemplaza por completo la información de un usuario existente en la base de datos identificándolo por su ID."
)
def update_user_complete(user_id: int, payload: UserUpdate, response: Response, db: Session = Depends(get_db)):
    add_custom_headers(response)
    
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error al actualizar usuario inexistente"
        )
    
    # Validar duplicado de email excluyendo al ID que se está editando
    existing_email = UserService.get_by_email(db, payload.email)
    if existing_email and existing_email.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado por otro usuario"
        )
        
    return UserService.update_complete(db, user, payload)


@router.patch(
    "/{user_id}", 
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial (PATCH)",
    description="Permite modificar solo algunos campos del usuario de manera selectiva en la base de datos. Si el cuerpo está vacío, responde con un error 400."
)
def update_user_partial(user_id: int, payload: UserPatch, response: Response, db: Session = Depends(get_db)):
    add_custom_headers(response)
    
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error al actualizar usuario inexistente"
        )
    
    datos_actualizacion = payload.model_dump(exclude_unset=True)
    
    # Controlar error de actualización vacía {} (Fase 10)
    if not datos_actualizacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Intento de actualización sin datos. Debe proporcionar al menos un campo válido."
        )
    
    # Si se cambia el email, validar que no cause conflicto con otro usuario
    if "email" in datos_actualizacion:
        existing_email = UserService.get_by_email(db, datos_actualizacion["email"])
        if existing_email and existing_email.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya registrado por otro usuario"
            )
        
    return UserService.update_partial(db, user, payload)

# --- ENDPOINT DELETE (FASE 9 Y 10) ---

@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
    description="Permite eliminar de forma permanente un usuario existente de la base de datos. Si el usuario no existe, arroja un error 404."
)
def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    add_custom_headers(response)
    
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error al eliminar usuario inexistente"
        )
        
    UserService.delete(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)