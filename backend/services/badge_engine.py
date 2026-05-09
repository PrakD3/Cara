"""
Badge Engine — dynamically checks and unlocks badges for patients.
All badge definitions are DB-driven. No badge logic is hardcoded.
"""
from sqlalchemy.orm import Session
from models.mascot import BadgeDefinition, PatientBadge, XPLog, StreakLog
from services.mascot_event_bus import publish_badge_event
from services.xp_engine import award_xp
from datetime import datetime
import logging

logger = logging.getLogger("cara.mascot.badge")


def evaluate_badges(db: Session, patient_id: int, context: dict = None):
    """
    Evaluates all active badge definitions against patient's current state.
    Unlocks any newly eligible badges.
    """
    if context is None:
        context = {}

    all_badges = db.query(BadgeDefinition).filter(BadgeDefinition.is_active == True).all()
    already_earned = {pb.badge_id for pb in db.query(PatientBadge).filter(PatientBadge.patient_id == patient_id).all()}

    newly_unlocked = []

    for badge in all_badges:
        if badge.id in already_earned:
            continue  # Already earned

        if _check_badge_condition(db, patient_id, badge, context):
            _unlock_badge(db, patient_id, badge)
            newly_unlocked.append(badge)

    return newly_unlocked


def _check_badge_condition(db: Session, patient_id: int, badge: BadgeDefinition, context: dict) -> bool:
    """Checks whether the badge condition is met based on condition type."""
    condition_type = badge.unlock_condition_type
    threshold = badge.unlock_condition_value

    if condition_type == "MEDICATION_COUNT":
        count = db.query(XPLog).filter(
            XPLog.patient_id == patient_id,
            XPLog.action_type == "MEDICATION_TAKEN"
        ).count()
        return count >= threshold

    elif condition_type == "STREAK_COUNT":
        streak = db.query(StreakLog).filter(
            StreakLog.patient_id == patient_id,
            StreakLog.streak_type == "DAILY"
        ).first()
        return streak is not None and streak.current_streak >= threshold

    elif condition_type == "XP_TOTAL":
        from models.mascot import MascotProfile
        mascot = db.query(MascotProfile).filter(MascotProfile.patient_id == patient_id).first()
        return mascot is not None and mascot.total_xp_earned >= threshold

    elif condition_type == "DISEASE_STREAK":
        streak = db.query(StreakLog).filter(
            StreakLog.patient_id == patient_id,
            StreakLog.streak_type == "DISEASE_SPECIFIC"
        ).first()
        return streak is not None and streak.current_streak >= threshold

    elif condition_type == "PREVENTIVE_CARE_COUNT":
        count = db.query(XPLog).filter(
            XPLog.patient_id == patient_id,
            XPLog.action_type == "PREVENTIVE_CARE"
        ).count()
        return count >= threshold

    return False


def _unlock_badge(db: Session, patient_id: int, badge: BadgeDefinition):
    """Records a badge unlock and awards the associated XP."""
    patient_badge = PatientBadge(
        patient_id=patient_id,
        badge_id=badge.id,
        unlocked_at=datetime.utcnow()
    )
    db.add(patient_badge)
    db.commit()

    # Award XP for badge unlock
    if badge.xp_reward > 0:
        award_xp(db, patient_id, action_type="BADGE_UNLOCK", metadata={"badge_key": badge.badge_key})

    # Broadcast real-time badge event
    publish_badge_event(
        patient_id=patient_id,
        badge_key=badge.badge_key,
        badge_name=badge.name
    )
    logger.info(f"Badge unlocked: {badge.badge_key} for patient {patient_id}")


def get_patient_badges(db: Session, patient_id: int) -> list:
    """Returns all badges earned by a patient."""
    patient_badges = db.query(PatientBadge).filter(PatientBadge.patient_id == patient_id).all()
    result = []
    for pb in patient_badges:
        b = pb.badge
        result.append({
            "badge_key": b.badge_key,
            "name": b.name,
            "description": b.description,
            "icon_url": b.icon_url,
            "unlocked_at": pb.unlocked_at,
        })
    return result
