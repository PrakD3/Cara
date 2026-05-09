"""
XP Engine — handles all experience point operations.
Dynamically reads XP values from the database. Nothing hardcoded.
"""
from sqlalchemy.orm import Session
from models.mascot import XPConfig, XPLog, MascotProfile, MascotEvolution
from services.mascot_event_bus import publish_xp_event
import logging
from datetime import datetime

logger = logging.getLogger("cara.mascot.xp")


def award_xp(db: Session, patient_id: int, action_type: str, metadata: dict = None, extra_data: dict = None) -> int:
    """
    Awards XP to a patient for a given action.
    Reads XP value from DB config table — fully dynamic.
    """
    config = db.query(XPConfig).filter(
        XPConfig.action_type == action_type,
        XPConfig.is_active == True
    ).first()

    if not config:
        logger.warning(f"No XP config found for action: {action_type}")
        return 0

    xp_earned = config.xp_reward

    # Log XP event
    xp_log = XPLog(
        patient_id=patient_id,
        action_type=action_type,
        xp_earned=xp_earned,
        extra_data=extra_data or metadata or {},
        timestamp=datetime.utcnow()
    )
    db.add(xp_log)

    # Update mascot profile XP
    mascot = db.query(MascotProfile).filter(MascotProfile.patient_id == patient_id).first()
    if mascot:
        mascot.current_xp += xp_earned
        mascot.total_xp_earned += xp_earned

        # Check for level up
        new_level = _calculate_level(db, mascot.total_xp_earned)
        if new_level > mascot.current_level:
            mascot.current_level = new_level
            logger.info(f"Patient {patient_id} leveled up to {new_level}")

    db.commit()

    # Publish to Redis/WebSocket for real-time update
    publish_xp_event(patient_id=patient_id, xp_earned=xp_earned, action_type=action_type)

    logger.info(f"Awarded {xp_earned} XP to patient {patient_id} for {action_type}")
    return xp_earned


def _calculate_level(db: Session, total_xp: int) -> int:
    """
    Determines current level based on total XP and evolution thresholds.
    All thresholds are stored in DB — no hardcoding.
    """
    levels = db.query(MascotEvolution).order_by(MascotEvolution.xp_required.desc()).all()
    for level in levels:
        if total_xp >= level.xp_required:
            return level.level
    return 1


def get_xp_summary(db: Session, patient_id: int) -> dict:
    """Returns full XP summary for a patient."""
    mascot = db.query(MascotProfile).filter(MascotProfile.patient_id == patient_id).first()
    if not mascot:
        return {}

    # Find XP needed for next level
    next_level = db.query(MascotEvolution).filter(
        MascotEvolution.level == mascot.current_level + 1
    ).first()

    xp_to_next = (next_level.xp_required - mascot.total_xp_earned) if next_level else 0

    return {
        "patient_id": patient_id,
        "current_xp": mascot.current_xp,
        "total_xp_earned": mascot.total_xp_earned,
        "current_level": mascot.current_level,
        "xp_to_next_level": max(0, xp_to_next),
    }
