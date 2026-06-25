# app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch
from app.auth.security import get_password_hash

class UserService:

    @staticmethod
    def get_all(db: Session, role: str = None, is_active: bool = None):
        query = db.query(User)
        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        return query.order_by(User.name).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user_data: UserCreate):
        db_user = User(
            name=user_data.name,
            email=user_data.email.lower(),
            hashed_password=get_password_hash(user_data.password),
            role=user_data.role,
            is_active=user_data.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_complete(db: Session, user: User, user_data: UserUpdate):
        user.name = user_data.name
        user.email = user_data.email.lower()
        user.role = user_data.role
        user.is_active = user_data.is_active
        if user_data.password:
            user.hashed_password = get_password_hash(user_data.password)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_partial(db: Session, user: User, user_data: UserPatch):
        update_data = user_data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"]:
            update_data["email"] = update_data["email"].lower()
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User):
        db.delete(user)
        db.commit()