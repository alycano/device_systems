
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router  # Rutas de dispositivos
from app.routes.loan_routes import router as loan_router      # Rutas de préstamos
from app.database.connection import engine, Base  # Importación del ORM para la persistencia

# Inicializar las tablas físicas en la base de datos de forma automática al arrancar
Base.metadata.create_all(bind=engine)

# Inicialización de la aplicación FastAPI con metadatos del proyecto
app = FastAPI(
    title="Device Systems API",
    description="""
    Sistema avanzado de gestión, validación y administración del recurso de usuarios, 
    inventario de hardware IT y control relacional de préstamos para el proyecto RegisTech.
    
    Esta versión incorpora persistencia real de datos mediante SQLAlchemy ORM, 
    base de datos relacional SQLite con Integridad Referencial y control estricto de excepciones HTTP.
    """,
    version="2.0.0",
    contact={
        "name": "Aly Santiago Cano",
        "email": "aly.santiago@sena.edu.co"
    }
)

# Manejador global para intercepción de fallos imprevistos en el servidor (Errores 500)
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

# Inclusión de los enrutadores modulares conectados a la base de datos relacional
app.include_router(user_router)
app.include_router(device_router)  # Activación de rutas para /devices
app.include_router(loan_router)    # Activación de rutas para /loans

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz para verificación del estado de la API.
    """
    return {
        "status": "online",
        "project": "Device Systems API",
        "version": "2.0.0",
        "documentation": "/docs"
    }