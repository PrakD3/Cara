from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.domain import IVRLog, AdherenceLog
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger("cara.ivr.webhooks")


@router.post("/exotel/callback")
async def exotel_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook endpoint called by Exotel after the patient presses a key.
    DTMF input: 1 = Taken, 2 = Remind Later, 3 = Escalate to Caregiver
    """
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid", "UNKNOWN")
        digits = str(form_data.get("digits", "")).strip('"')
        patient_id_raw = request.query_params.get("patient_id", "0")

        # Validate patient_id safely
        try:
            patient_id = int(patient_id_raw)
        except (ValueError, TypeError):
            patient_id = 0

        status_map = {"1": "TAKEN", "2": "DELAYED", "3": "ESCALATED"}
        adherence_status = status_map.get(digits, "MISSED")

        # Only link to patient if patient_id > 0
        patient_fk = patient_id if patient_id > 0 else None

        # Log raw IVR call
        ivr_log = IVRLog(
            patient_id=patient_fk,
            call_sid=call_sid,
            status="COMPLETED",
            dtmf_input=digits,
            created_at=datetime.utcnow()
        )
        db.add(ivr_log)

        # Log adherence outcome
        adherence = AdherenceLog(
            patient_id=patient_fk,
            medication_id=None,
            status=adherence_status,
            source="IVR",
            logged_at=datetime.utcnow()
        )
        db.add(adherence)
        db.commit()

        logger.info(f"IVR: CallSid={call_sid}, Patient={patient_fk}, Key={digits} → {adherence_status}")
        return {"status": "processing", "adherence_status": adherence_status}

    except Exception as e:
        db.rollback()
        logger.error(f"IVR Webhook Error: {str(e)}")
        return {"status": "error", "detail": str(e)}
