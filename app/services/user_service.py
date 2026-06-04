# app/services/user_service.py
from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate

class UserService:
    
    @staticmethod
    def obtener_y_filtrar(role: str = None, is_active: bool = None) -> list:
        resultado = users_db
        if role:
            resultado = [u for u in resultado if u["role"] == role]
        if is_active is not None:
            resultado = [u for u in resultado if u["is_active"] == is_active]
        return resultado

    @staticmethod
    def guardar_nuevo(datos: UserCreate) -> dict:
        nuevo_id = max([u["id"] for u in users_db], default=0) + 1
        nuevo_usuario = {
            "id": nuevo_id,
            "name": datos.name,
            "email": datos.email.lower(),
            "role": datos.role,
            "is_active": datos.is_active
        }
        users_db.append(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def sobreescribir_registro(usuario_actual: dict, nuevos_datos: UserCreate) -> dict:
        usuario_actual["name"] = nuevos_datos.name
        usuario_actual["email"] = nuevos_datos.email.lower()
        usuario_actual["role"] = nuevos_datos.role
        usuario_actual["is_active"] = nuevos_datos.is_active
        return usuario_actual

    @staticmethod
    def actualizar_campos_parciales(usuario_actual: dict, datos_filtrados: dict) -> dict:
        for llave, valor in datos_filtrados.items():
            if llave == "email" and valor:
                usuario_actual[llave] = valor.lower()
            else:
                usuario_actual[llave] = valor
        return usuario_actual

    @staticmethod
    def borrar_registro(usuario_actual: dict) -> None:
        users_db.remove(usuario_actual)