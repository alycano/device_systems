from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserAuthResponse
from app.auth.auth_service import AuthService
from app.auth.security import create_access_token
from app.middlewares.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserAuthResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    existing = AuthService.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    return AuthService.register(db, user_data)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserAuthResponse)
def read_users_me(current_user: UserAuthResponse = Depends(get_current_active_user)):
    return current_user