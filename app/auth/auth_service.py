from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token

class AuthService:

    @staticmethod
    def register(db: Session, user_data: UserRegister) -> User:
        db_user = User(
            name=user_data.name,
            email=user_data.email.lower(),
            hashed_password=get_password_hash(user_data.password),
            role=user_data.role.value,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.lower()).first()