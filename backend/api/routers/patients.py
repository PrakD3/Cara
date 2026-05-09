from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.domain_schemas import PatientCreate, PatientResponse
from models.database import get_db
from models.domain import User
from api.deps import get_current_user
from services.patient_service import create_patient_profile, get_patients_for_doctor

router = APIRouter()

@router.post("/")
def create_patient(data: PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "DOCTOR":
        raise HTTPException(status_code=403, detail="Only doctors can create patients")
    
    profile, temp_pass = create_patient_profile(db, data, current_user.id)
    return {"message": "Patient created", "patient_id": profile.id, "temp_password": temp_pass}

@router.get("/")
def get_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "DOCTOR":
        return get_patients_for_doctor(db, current_user.id)
    return []
