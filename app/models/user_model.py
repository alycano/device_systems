# app/models/user_model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship  # <-- PASO CLAVE: Importamos relationship
from datetime import datetime
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Fase 6: Un usuario puede tener muchos préstamos (Relación One-to-Many)
    # back_populates se encarga de conectar bidireccionalmente con el campo 'user' en Loan
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")