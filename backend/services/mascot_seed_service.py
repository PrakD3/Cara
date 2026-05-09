from sqlalchemy.orm import Session
from models.mascot import (
    MascotProfile, MoodState, MascotStateLog, XPConfig, XPLog,
    StreakLog, BadgeDefinition, PatientBadge, DialogueTemplate, MascotEvolution
)
from services.mascot_state_machine import (
    DEFAULT_MOOD_STATES, DEFAULT_XP_CONFIG, LEVEL_DEFINITIONS,
    DEFAULT_BADGES, TRANSITION_RULES
)
import logging

logger = logging.getLogger("cara.mascot.seed")


def seed_mascot_system(db: Session):
    """
    Seeds all default mascot system data into the database.
    Called on application startup. Safe to run multiple times (checks before inserting).
    """
    _seed_mood_states(db)
    _seed_xp_config(db)
    _seed_evolutions(db)
    _seed_badges(db)
    logger.info("Mascot system seed complete.")


def _seed_mood_states(db: Session):
    for state in DEFAULT_MOOD_STATES:
        existing = db.query(MoodState).filter(MoodState.state_id == state["state_id"]).first()
        if not existing:
            db.add(MoodState(**state))
    db.commit()


def _seed_xp_config(db: Session):
    for config in DEFAULT_XP_CONFIG:
        existing = db.query(XPConfig).filter(XPConfig.action_type == config["action_type"]).first()
        if not existing:
            db.add(XPConfig(**config))
    db.commit()


def _seed_evolutions(db: Session):
    for level in LEVEL_DEFINITIONS:
        existing = db.query(MascotEvolution).filter(MascotEvolution.level == level["level"]).first()
        if not existing:
            db.add(MascotEvolution(**level))
    db.commit()


def _seed_badges(db: Session):
    for badge in DEFAULT_BADGES:
        existing = db.query(BadgeDefinition).filter(BadgeDefinition.badge_key == badge["badge_key"]).first()
        if not existing:
            db.add(BadgeDefinition(**badge))
    db.commit()
