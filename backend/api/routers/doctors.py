from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.domain_schemas import DoctorCreate, DoctorResponse
from models.database import get_db
from services.doctor_service import register_doctor_service

router = APIRouter()

@router.post("/register", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def register_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    """
    Registers a new doctor into the system.
    """
    profile = register_doctor_service(db, data)
    return profile
