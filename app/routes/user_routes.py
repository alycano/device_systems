from fastapi import APIRouter, Depends, status, HTTPException, Query, Response
from typing import List, Optional
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdateParcial, UserRole
from app.services.user_service import UserService
from app.dependencies.user_dependencies import get_user_or_404, verificar_email_duplicado

router = APIRouter(prefix="/users", tags=["Users"])

# --- Función Auxiliar para Cabeceras HTTP Personalizadas (Evolución Fase 5) ---
def add_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

# --- ENDPOINTS GET (FASE 5 Y RETO INTEGRADOR) ---

@router.get(
    "", 
    response_model=List[UserResponse], 
    status_code=status.HTTP_200_OK,
    summary="Listar y filtrar usuarios",
    description="Listar todos los usuarios del sistema. Permite la personalización de la respuesta mediante filtros opcionales de consulta (Query Parameters) por rol o estado activo."
)
def get_users(
    response: Response,
    role: Optional[UserRole] = Query(None, description="Filtrar usuarios por rol administrativo u operativo"),
    is_active: Optional[bool] = Query(None, description="Filtrar usuarios por estado activo o inactivo")
):
    add_custom_headers(response)
    return UserService.obtener_y_filtrar(role, is_active)


@router.get(
    "/{user_id}", 
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Obtener los detalles de un usuario específico utilizando su ID único a través de un parámetro de ruta (Path Parameter) e inyección de dependencias."
)
def get_user_by_id(response: Response, usuario: dict = Depends(get_user_or_404)):
    add_custom_headers(response)
    return usuario

# --- ENDPOINT POST (FASE 4 Y 5) ---

@router.post(
    "", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
    description="Registrar un nuevo usuario en el sistema. Valida que el correo electrónico sea único para evitar duplicados."
)
def create_user(user: UserCreate, response: Response):
    add_custom_headers(response)
    # Validar si el Email ya existe en el sistema global
    verificar_email_duplicado(user.email)
    return UserService.guardar_nuevo(user)

# --- ENDPOINTS PUT Y PATCH (FASE 3) ---

@router.put(
    "/{user_id}", 
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK,
    summary="Actualización completa (PUT)",
    description="Reemplaza por completo la información de un usuario existente en el sistema identificándolo por su ID."
)
def update_user_complete(payload: UserCreate, response: Response, usuario_actual: dict = Depends(get_user_or_404)):
    add_custom_headers(response)
    # Validar duplicado de email excluyendo al usuario que se está editando
    verificar_email_duplicado(payload.email, excluir_id=usuario_actual["id"])
    return UserService.sobreescribir_registro(usuario_actual, payload)


@router.patch(
    "/{user_id}", 
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial (PATCH)",
    description="Permite modificar solo algunos campos del usuario de manera selectiva. Si el cuerpo de la petición está vacío, responde con un error 400."
)
def update_user_partial(payload: UserUpdateParcial, response: Response, usuario_actual: dict = Depends(get_user_or_404)):
    add_custom_headers(response)
    
    # Extraer campos enviados explícitamente por el cliente
    datos_actualizacion = payload.model_dump(exclude_unset=True)
    
    # Fase 3 y 6: Responder con 400 Bad Request si envían un cuerpo vacío {}
    if not datos_actualizacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Intento de actualización sin datos. Debe proporcionar al menos un campo válido."
        )
    
    # Si se intenta cambiar el correo, validar que no cause duplicados
    if "email" in datos_actualizacion:
        verificar_email_duplicado(datos_actualizacion["email"], excluir_id=usuario_actual["id"])
        
    return UserService.actualizar_campos_parciales(usuario_actual, datos_actualizacion)

# --- ENDPOINT DELETE (FASE 4) ---

@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
    description="Permite eliminar de forma permanente un usuario existente del sistema. Retorna un estado 204 No Content sin cuerpo de respuesta."
)
def delete_user(response: Response, usuario_actual: dict = Depends(get_user_or_404)):
    add_custom_headers(response)
    UserService.borrar_registro(usuario_actual)
    return Response(status_code=status.HTTP_204_NO_CONTENT)