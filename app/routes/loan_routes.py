from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService
from app.services.device_service import DeviceService
from app.middlewares.rate_limiter import limiter

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    device = DeviceService.get_by_id(db, loan.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="El dispositivo no existe")
    if not device.is_available:
        raise HTTPException(status_code=400, detail="El dispositivo no está disponible actualmente")
    return LoanService.create_loan(db, loan, device)

@router.patch("/{loan_id}/return", response_model=LoanResponse)
def return_device(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    loan = LoanService.get_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Registro de préstamo no encontrado")
    if loan.status == "returned":
        raise HTTPException(status_code=400, detail="Este dispositivo ya fue devuelto previamente")
    device = DeviceService.get_by_id(db, loan.device_id)
    return LoanService.return_device(db, loan, device)

@router.get("/details", response_model=List[LoanDetailResponse])
def read_active_loans_details(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return LoanService.get_all_detailed(db)