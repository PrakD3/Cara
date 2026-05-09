from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db, Medication
from schemas.pydantic_models import Medication as MedicationSchema

router = APIRouter()

@router.get("/patient/{patient_id}", response_model=List[MedicationSchema])
def get_patient_medications(patient_id: str, db: Session = Depends(get_db)):
    medications = db.query(Medication).filter(Medication.patient_id == patient_id).all()
    return medications

@router.get("/{medication_id}", response_model=MedicationSchema)
def get_medication(medication_id: str, db: Session = Depends(get_db)):
    medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication