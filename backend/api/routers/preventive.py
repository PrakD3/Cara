from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.domain import User, PatientProfile, AdherenceLog, Medication
from api.deps import get_current_user
from ml.risk_engine import risk_engine
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger("cara.preventive")


@router.get("/risk/{patient_id}")
def get_risk_score(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns a full risk profile for a patient.
    Includes adherence breakdown, risk score, and recommendation.
    """
    patient = db.query(PatientProfile).filter(PatientProfile.user_id == patient_id).first()
    if not patient:
        return {"error": "Patient not found"}

    since = datetime.utcnow() - timedelta(days=7)
    logs = db.query(AdherenceLog).filter(
        AdherenceLog.patient_id == patient_id,
        AdherenceLog.logged_at >= since
    ).all()

    taken = sum(1 for l in logs if l.status == "TAKEN")
    missed = sum(1 for l in logs if l.status == "MISSED")
    delayed = sum(1 for l in logs if l.status == "DELAYED")
    total = len(logs)

    adherence_rate = (taken / total * 100) if total > 0 else 0

    risk_score = risk_engine.predict_risk(
        patient_age=patient.age,
        missed_doses_7d=missed,
        disease_severity=6
    )

    recommendation = (
        "Immediate caregiver notification recommended."
        if risk_score > 0.7
        else "Monitor closely. Encourage patient."
        if risk_score > 0.4
        else "Patient is doing well. Maintain current routine."
    )

    return {
        "patient_id": patient_id,
        "adherence_rate_7d": round(adherence_rate, 1),
        "taken": taken,
        "missed": missed,
        "delayed": delayed,
        "risk_score": round(risk_score, 2),
        "risk_level": "HIGH" if risk_score > 0.7 else "MEDIUM" if risk_score > 0.4 else "LOW",
        "recommendation": recommendation,
    }


@router.get("/heatmap/{patient_id}")
def get_adherence_heatmap(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns a 30-day adherence heatmap for a patient.
    Each entry is a date + adherence status for frontend chart rendering.
    """
    since = datetime.utcnow() - timedelta(days=30)
    logs = db.query(AdherenceLog).filter(
        AdherenceLog.patient_id == patient_id,
        AdherenceLog.logged_at >= since
    ).order_by(AdherenceLog.logged_at.asc()).all()

    heatmap = {}
    for log in logs:
        day = log.logged_at.strftime("%Y-%m-%d")
        # Priority: TAKEN > DELAYED > MISSED
        current = heatmap.get(day)
        if current != "TAKEN":
            heatmap[day] = log.status

    return {
        "patient_id": patient_id,
        "heatmap": [{"date": k, "status": v} for k, v in heatmap.items()],
    }
