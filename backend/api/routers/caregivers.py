from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.domain import User, PatientProfile, AdherenceLog, Medication
from api.deps import get_current_user
from services.mascot_event_bus import publish_mood_event
from ml.risk_engine import risk_engine
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger("cara.caregiver")


@router.get("/patients")
def get_linked_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns all patients linked to this caregiver."""
    if current_user.role != "CAREGIVER":
        raise HTTPException(status_code=403, detail="Only caregivers can access this endpoint")

    patients = db.query(PatientProfile).filter(PatientProfile.caregiver_id == current_user.id).all()
    return [
        {
            "patient_id": p.user_id,
            "name": p.name,
            "age": p.age,
            "disease": p.preferred_language,
            "risk_score": p.risk_score,
        }
        for p in patients
    ]


@router.get("/patients/{patient_id}/adherence")
def get_patient_adherence(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns the last 7 days of adherence logs for a linked patient."""
    if current_user.role not in ["CAREGIVER", "DOCTOR"]:
        raise HTTPException(status_code=403, detail="Access denied")

    since = datetime.utcnow() - timedelta(days=7)
    logs = db.query(AdherenceLog).filter(
        AdherenceLog.patient_id == patient_id,
        AdherenceLog.logged_at >= since
    ).order_by(AdherenceLog.logged_at.desc()).all()

    return [
        {
            "status": log.status,
            "source": log.source,
            "logged_at": log.logged_at,
        }
        for log in logs
    ]


@router.get("/patients/{patient_id}/risk")
def get_patient_risk(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculates and returns the real-time risk score for a patient."""
    if current_user.role not in ["CAREGIVER", "DOCTOR"]:
        raise HTTPException(status_code=403, detail="Access denied")

    patient = db.query(PatientProfile).filter(PatientProfile.user_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Count missed doses in last 7 days
    since = datetime.utcnow() - timedelta(days=7)
    missed = db.query(AdherenceLog).filter(
        AdherenceLog.patient_id == patient_id,
        AdherenceLog.status == "MISSED",
        AdherenceLog.logged_at >= since
    ).count()

    # Dynamic risk scoring
    score = risk_engine.predict_risk(
        patient_age=patient.age,
        missed_doses_7d=missed,
        disease_severity=6  # Future: derive from disease DB config
    )

    # Update stored risk score
    patient.risk_score = score
    db.commit()

    return {
        "patient_id": patient_id,
        "risk_score": round(score, 2),
        "risk_level": "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW",
        "missed_doses_last_7_days": missed,
    }
