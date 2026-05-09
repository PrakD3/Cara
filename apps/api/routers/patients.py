from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db, PatientProfile, User
from schemas.pydantic_models import PatientProfile as PatientSchema

router = APIRouter()

@router.get("/me", response_model=PatientSchema)
def get_current_patient_profile(db: Session = Depends(get_db)):
    # For now, we fetch the first patient in the DB
    # In a real app, this would be based on the JWT token
    patient = db.query(PatientProfile).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient

@router.get("/{patient_id}", response_model=PatientSchema)
def get_patient_profile(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(PatientProfile).filter(PatientProfile.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient