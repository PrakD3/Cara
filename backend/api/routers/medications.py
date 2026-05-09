from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.domain_schemas import MedicationCreate, AdherenceLogCreate
from models.database import get_db
from models.domain import User
from api.deps import get_current_user
from services.medication_service import assign_medication, get_patient_medications, log_adherence_event

router = APIRouter()

@router.post("/{patient_id}")
def create_medication(
    patient_id: int, 
    data: MedicationCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "DOCTOR":
        raise HTTPException(status_code=403, detail="Only doctors can assign medication.")
    
    med = assign_medication(db, patient_id, current_user.id, data)
    return med

@router.get("/{patient_id}")
def list_medications(
    patient_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # In production, add authorization check to ensure the doctor owns the patient
    # or the user IS the patient.
    meds = get_patient_medications(db, patient_id)
    return meds

@router.post("/adherence/log")
def log_adherence(
    data: AdherenceLogCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # This route is hit by the mobile app when the patient confirms intake
    if current_user.role != "PATIENT":
        raise HTTPException(status_code=403, detail="Only patients can log app adherence.")
        
    log = log_adherence_event(db, current_user.id, data)
    return {"status": "success", "log_id": log.id}
