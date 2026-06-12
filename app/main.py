# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.routes.user_routes import router as user_router
from app.database.connection import engine, Base  # Importación del ORM para la persistencia

# Inicializar las tablas físicas en la base de datos SQLite de forma automática al arrancar
Base.metadata.create_all(bind=engine)

# Fase 8: Inicialización evolucionada de la aplicación FastAPI con metadatos extendidos y persistencia ORM
app = FastAPI(
    title="Device Systems API",
    description="""
    Sistema de gestión, validación y administración del recurso de usuarios para el control de hardware IT 'device_systems'.
    
    Esta versión definitiva incorpora persistencia real de datos mediante SQLAlchemy ORM, una base de datos relacional SQLite y control estricto de excepciones HTTP.
    """,
    version="2.0.0",
    contact={
        "name": "Aly Santiago Cano",
        "email": "aly.santiago@sena.edu.co"
    }
)

# Fase 6: Robustez del backend mediante un manejador global para intercepción de fallos imprevistos (500)
@app.exception_handler(Exception)
async def manejador_errores_inesperados(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Ha ocurrido un inconveniente interno inesperado en el servidor.",
            "status_code": 500,
            "detail": str(exc)
        }
    )

# Inclusión del enrutador modular de usuarios conectado a la base de datos
app.include_router(user_router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz para verificación del estado de la API en su versión evolucionada.
    """
    return {
        "status": "online",
        "project": "Device Systems API",
        "version": "2.0.0",
        "documentation": "/docs"
    }