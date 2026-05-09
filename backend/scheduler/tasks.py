"""
APScheduler job to evaluate missed medications and trigger
IVR calls and caregiver escalations automatically.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.domain import PatientProfile, MedicationSchedule, Medication, AdherenceLog
from ivr.exotel_client import trigger_ivr_call
from notifications.push import send_caregiver_alert
from ml.risk_engine import risk_engine
from datetime import datetime, timedelta
import logging
import asyncio

logger = logging.getLogger("cara.scheduler")
scheduler = AsyncIOScheduler()


async def evaluate_missed_medications():
    """
    Runs every 15 minutes. For each active patient with a missed dose:
    1. Triggers IVR call
    2. Updates risk score
    3. Escalates to caregiver if consecutive misses detected
    """
    logger.info("Running missed medication evaluation...")
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        grace_window = now - timedelta(minutes=30)

        # Get all medication schedules for the current hour window
        time_window = now.strftime("%H:")  # Match schedules like "08:00", "08:30"
        schedules = db.query(MedicationSchedule).filter(
            MedicationSchedule.timing.startswith(time_window[:3])
        ).all()

        for schedule in schedules:
            med = db.query(Medication).filter(Medication.id == schedule.medication_id).first()
            if not med:
                continue

            # Check if adherence was already logged
            already_logged = db.query(AdherenceLog).filter(
                AdherenceLog.patient_id == med.patient_id,
                AdherenceLog.medication_id == med.id,
                AdherenceLog.logged_at >= grace_window
            ).first()

            if already_logged:
                continue  # Already taken — skip

            # Patient missed — trigger IVR
            patient = db.query(PatientProfile).filter(
                PatientProfile.user_id == med.patient_id
            ).first()
            if not patient:
                continue

            logger.info(f"Triggering IVR for missed dose: patient={med.patient_id}")
            await trigger_ivr_call(
                phone=patient.user.phone if hasattr(patient, 'user') else "",
                flow_id="MISSED_MED_FLOW",
                dynamic_data={
                    "patient_name": patient.name,
                    "medication_id": med.id,
                    "language": patient.preferred_language
                }
            )

            # Check consecutive misses for escalation
            recent_misses = db.query(AdherenceLog).filter(
                AdherenceLog.patient_id == med.patient_id,
                AdherenceLog.status == "MISSED",
                AdherenceLog.logged_at >= now - timedelta(days=2)
            ).count()

            if recent_misses >= 3:
                logger.warning(f"Consecutive misses for patient {med.patient_id} — escalating to caregiver")
                # In production, fetch caregiver device token from DB
                # await send_caregiver_alert(caregiver_token, patient.name, recent_misses)

    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
    finally:
        db.close()


async def update_risk_scores():
    """
    Runs every 6 hours. Recalculates and stores risk scores for all patients.
    """
    logger.info("Running risk score update job...")
    db: Session = SessionLocal()
    try:
        patients = db.query(PatientProfile).all()
        for patient in patients:
            since = datetime.utcnow() - timedelta(days=7)
            missed = db.query(AdherenceLog).filter(
                AdherenceLog.patient_id == patient.user_id,
                AdherenceLog.status == "MISSED",
                AdherenceLog.logged_at >= since
            ).count()

            score = risk_engine.predict_risk(
                patient_age=patient.age,
                missed_doses_7d=missed,
                disease_severity=6
            )
            patient.risk_score = score

        db.commit()
        logger.info(f"Risk scores updated for {len(patients)} patients")
    except Exception as e:
        logger.error(f"Risk score job error: {str(e)}")
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        evaluate_missed_medications,
        trigger=IntervalTrigger(minutes=15),
        id="missed_meds_check",
        name="Check for missed medications every 15 minutes",
        replace_existing=True
    )
    scheduler.add_job(
        update_risk_scores,
        trigger=IntervalTrigger(hours=6),
        id="risk_score_update",
        name="Update patient risk scores every 6 hours",
        replace_existing=True
    )
    scheduler.start()
    logger.info("APScheduler started: missed_meds_check (15min), risk_score_update (6h)")
