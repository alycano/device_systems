# app/services/loan_service.py
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app.models.loan_model import Loan
from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate

class LoanService:
    @staticmethod
    def get_all(db: Session, status: str = None):
        query = db.query(Loan)
        if status:
            query = query.where(Loan.status == status)
        return query.all()

    @staticmethod
    def get_all_detailed(db: Session):
        # Aquí cruzamos las tablas usando Inner Joins y joinedload para optimizar la carga
        return db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).where(Loan.status == "active").all()

    @staticmethod
    def get_by_id(db: Session, loan_id: int):
        return db.query(Loan).where(Loan.id == loan_id).first()

    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate, device: Device):
        # 1. Registramos el préstamo en la tabla 'loans'
        db_loan = Loan(
            user_id=loan_data.user_id,
            device_id=loan_data.device_id,
            status="active",
            loan_date=datetime.utcnow()
        )
        # 2. Cambiamos el estado del dispositivo a NO disponible
        device.is_available = False
        
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        return db_loan

    @staticmethod
    def return_device(db: Session, db_loan: Loan, device: Device):
        # 1. Cerramos el préstamo asentando la fecha de devolución
        db_loan.status = "returned"
        db_loan.return_date = datetime.utcnow()
        
        # 2. Volvemos a poner el dispositivo disponible para otros aprendices
        device.is_available = True
        
        db.commit()
        db.refresh(db_loan)
        return db_loan