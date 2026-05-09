from sqlalchemy.orm import Session
from models.domain import Medication, MedicationSchedule, AdherenceLog
from schemas.domain_schemas import MedicationCreate, AdherenceLogCreate

def assign_medication(db: Session, patient_id: int, doctor_id: int, data: MedicationCreate):
    # Create the Medication base record
    medication = Medication(
        patient_id=patient_id,
        doctor_id=doctor_id,
        disease_id=data.disease_id,
        name=data.name,
        dosage=data.dosage,
        instructions=data.instructions,
        refill_cycle_days=data.refill_cycle_days
    )
    db.add(medication)
    db.commit()
    db.refresh(medication)
    
    # Bind the schedules
    for sched in data.schedules:
        schedule_entry = MedicationSchedule(
            medication_id=medication.id,
            timing=sched.timing,
            frequency=sched.frequency
        )
        db.add(schedule_entry)
        
    db.commit()
    return medication

def get_patient_medications(db: Session, patient_id: int):
    return db.query(Medication).filter(Medication.patient_id == patient_id).all()

def log_adherence_event(db: Session, patient_id: int, data: AdherenceLogCreate):
    log = AdherenceLog(
        patient_id=patient_id,
        medication_id=data.medication_id,
        schedule_id=data.schedule_id,
        status=data.status,
        source=data.source
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # Fire off WebSocket Broadcast event or AI Emotion update trigger here
    return log
