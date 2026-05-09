"""
Streak Engine — tracks daily, weekly, and disease-specific adherence streaks.
Supports grace periods, streak repair, and intelligent streak continuation.
"""
from sqlalchemy.orm import Session
from models.mascot import StreakLog
from services.mascot_event_bus import publish_streak_event
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger("cara.mascot.streak")

GRACE_PERIOD_HOURS = 24  # Allow one missed day with grace period


def update_streak(db: Session, patient_id: int, streak_type: str = "DAILY") -> dict:
    """
    Updates the streak for a patient after a medication taken event.
    Handles grace periods and streak continuation intelligently.
    """
    today = date.today()
    streak = db.query(StreakLog).filter(
        StreakLog.patient_id == patient_id,
        StreakLog.streak_type == streak_type
    ).first()

    if not streak:
        # First ever activity — create streak
        streak = StreakLog(
            patient_id=patient_id,
            streak_type=streak_type,
            current_streak=1,
            longest_streak=1,
            last_activity_date=datetime.utcnow(),
            grace_period_used=False
        )
        db.add(streak)
        db.commit()
        _broadcast_streak(patient_id, streak)
        return _streak_dict(streak)

    last_date = streak.last_activity_date.date() if streak.last_activity_date else None

    if last_date == today:
        # Already logged today — no update needed
        return _streak_dict(streak)

    elif last_date == today - timedelta(days=1):
        # Consecutive day — extend streak
        streak.current_streak += 1
        streak.grace_period_used = False

    elif last_date == today - timedelta(days=2) and not streak.grace_period_used:
        # One day gap — use grace period, keep streak alive
        streak.current_streak += 1
        streak.grace_period_used = True
        logger.info(f"Grace period used for patient {patient_id}")

    else:
        # Streak broken — reset
        streak.current_streak = 1
        streak.grace_period_used = False

    # Update longest streak
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_activity_date = datetime.utcnow()
    streak.updated_at = datetime.utcnow()
    db.commit()

    _broadcast_streak(patient_id, streak)
    return _streak_dict(streak)


def check_streak_broken(db: Session, patient_id: int, streak_type: str = "DAILY") -> bool:
    """Returns True if the patient's streak has been broken today."""
    streak = db.query(StreakLog).filter(
        StreakLog.patient_id == patient_id,
        StreakLog.streak_type == streak_type
    ).first()

    if not streak or not streak.last_activity_date:
        return True

    last_date = streak.last_activity_date.date()
    today = date.today()
    gap = (today - last_date).days

    if gap >= 2 and streak.grace_period_used:
        return True
    if gap >= 3:
        return True
    return False


def get_streak_summary(db: Session, patient_id: int) -> list:
    """Returns all streak records for a patient."""
    streaks = db.query(StreakLog).filter(StreakLog.patient_id == patient_id).all()
    return [_streak_dict(s) for s in streaks]


def _streak_dict(streak: StreakLog) -> dict:
    return {
        "streak_type": streak.streak_type,
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_activity_date": streak.last_activity_date,
    }


def _broadcast_streak(patient_id: int, streak: StreakLog):
    publish_streak_event(
        patient_id=patient_id,
        streak_type=streak.streak_type,
        current_streak=streak.current_streak,
        longest_streak=streak.longest_streak
    )
