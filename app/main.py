from fastapi import FastAPI
from app.routes.user_routes import router as user_router

# Inicialización de la aplicación FastAPI con metadatos del proyecto
app = FastAPI(
    title="Device Systems API",
    description="Sistema de gestión y validación de usuarios para control de hardware IT",
    version="1.0.0"
)

# Inclusión del enrutador modular de usuarios
app.include_router(user_router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz para verificación del estado inicial de la API.
    """
    return {
        "status": "online",
        "project": "Device Systems API",
        "documentation": "/docs"
    }