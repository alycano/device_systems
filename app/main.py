from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router
from app.database.connection import engine, Base
from app.middlewares.request_middleware import RequestMiddleware
from app.middlewares.rate_limiter import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="""
    API REST segura para gestión de usuarios, dispositivos y préstamos.
    
    Esta versión incorpora autenticación OAuth2 con JWT, hash de contraseñas con bcrypt,
    protección de rutas por roles, middleware personalizado, rate limiting y CORS.
    """,
    version="3.0.0",
    contact={
        "name": "Aly Santiago Cano",
        "email": "aly.santiago@sena.edu.co"
    }
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestMiddleware)

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

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "online",
        "project": "device_systems API",
        "version": "3.0.0",
        "documentation": "/docs"
    }
