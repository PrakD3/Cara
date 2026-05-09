"""
Mascot Service — core orchestration layer.
Handles mood transitions, event processing, and dialogue generation.
All logic is data-driven via the state machine and DB config.
"""
from sqlalchemy.orm import Session
from models.mascot import (
    MascotProfile, MoodState, MascotStateLog,
    MascotEvolution, DialogueTemplate
)
from services.mascot_state_machine import TRANSITION_RULES
from services.mascot_event_bus import publish_mood_event, publish_celebration_event, publish_evolution_event
from services.xp_engine import award_xp
from services.streak_engine import update_streak
from services.badge_engine import evaluate_badges
import random
import logging
from datetime import datetime

logger = logging.getLogger("cara.mascot.service")


def get_or_create_mascot_profile(db: Session, patient_id: int) -> MascotProfile:
    """Gets or creates the mascot profile for a patient."""
    mascot = db.query(MascotProfile).filter(MascotProfile.patient_id == patient_id).first()
    if not mascot:
        mascot = MascotProfile(
            patient_id=patient_id,
            mascot_name="Dosi",
            current_mood="HAPPY",
            mood_intensity=0.7,
            current_level=1,
            current_xp=0,
            total_xp_earned=0,
            engagement_score=1.0,
        )
        db.add(mascot)
        db.commit()
        db.refresh(mascot)
    return mascot


def process_mascot_event(db: Session, patient_id: int, event_type: str, metadata: dict = None) -> dict:
    """
    Core event processor — the heart of the DOSI engine.
    Receives an event, resolves mood transition, awards XP, updates streaks,
    evaluates badges, and broadcasts real-time updates.
    """
    mascot = get_or_create_mascot_profile(db, patient_id)
    metadata = metadata or {}

    # 1. Resolve mood transition
    new_mood = _resolve_mood_transition(db, mascot.current_mood, event_type)

    # 2. Log state change if mood changed
    if new_mood != mascot.current_mood:
        log = MascotStateLog(
            patient_id=patient_id,
            from_mood=mascot.current_mood,
            to_mood=new_mood,
            trigger_event=event_type,
            timestamp=datetime.utcnow()
        )
        db.add(log)
        mascot.current_mood = new_mood
        db.commit()

    # 3. Update engagement score
    _update_engagement_score(mascot, event_type)
    mascot.last_interaction = datetime.utcnow()
    db.commit()

    # 4. Award XP based on event type
    xp_map = {
        "MEDICATION_TAKEN": "MEDICATION_TAKEN",
        "PERFECT_DAY": "PERFECT_DAY",
        "IVR_RESPONSE": "IVR_RESPONSE",
        "AI_INTERACTION": "AI_INTERACTION",
        "APP_OPENED": "APP_OPENED",
        "PREVENTIVE_CARE": "PREVENTIVE_CARE",
    }
    if event_type in xp_map:
        award_xp(db, patient_id, action_type=xp_map[event_type], metadata=metadata)

    # 5. Update streak on medication taken
    if event_type in ["MEDICATION_TAKEN", "PERFECT_DAY"]:
        update_streak(db, patient_id, streak_type="DAILY")

    # 6. Check streak milestones for celebration
    _check_streak_milestones(db, patient_id, event_type)

    # 7. Evaluate badges
    newly_unlocked = evaluate_badges(db, patient_id, context={"event_type": event_type})

    # 8. Generate contextual dialogue
    dialogue = generate_dialogue(db, patient_id, mascot.current_mood, mascot.mascot_name)

    # 9. Get mood state metadata
    mood_state = db.query(MoodState).filter(MoodState.state_id == mascot.current_mood).first()
    animation_key = mood_state.animation_key if mood_state else "anim_happy_bounce"
    voice_tone = mood_state.voice_tone if mood_state else "warm"

    # 10. Broadcast via Redis pub/sub
    publish_mood_event(
        patient_id=patient_id,
        mood=mascot.current_mood,
        intensity=mascot.mood_intensity,
        animation_key=animation_key,
        voice_tone=voice_tone,
        dialogue=dialogue
    )

    # 11. Celebration events
    if mascot.current_mood in ["CELEBRATING", "EXCITED"]:
        publish_celebration_event(patient_id, celebration_type="STREAK_OR_MILESTONE")

    return {
        "mood": mascot.current_mood,
        "intensity": mascot.mood_intensity,
        "animation_key": animation_key,
        "voice_tone": voice_tone,
        "dialogue": dialogue,
        "newly_unlocked_badges": [b.badge_key for b in newly_unlocked],
        "xp_event": event_type,
    }


def _resolve_mood_transition(db: Session, current_mood: str, event_type: str) -> str:
    """
    Resolves what mood the mascot should transition to.
    Reads from TRANSITION_RULES — no hardcoded if/else chains.
    """
    rule = TRANSITION_RULES.get(event_type)
    if rule is None:
        return current_mood

    # Check if current mood is valid for this transition
    valid_froms = rule.get("from", [])
    if current_mood in valid_froms or "*" in valid_froms:
        return rule["to"]

    return current_mood


def _update_engagement_score(mascot: MascotProfile, event_type: str):
    """Adjusts the engagement score dynamically based on event type."""
    positive_events = {"MEDICATION_TAKEN", "PERFECT_DAY", "AI_INTERACTION", "APP_OPENED"}
    negative_events = {"MISSED_DOSE_1", "MISSED_DOSE_2", "MISSED_DOSE_3"}

    if event_type in positive_events:
        mascot.engagement_score = min(1.0, mascot.engagement_score + 0.05)
    elif event_type in negative_events:
        mascot.engagement_score = max(0.0, mascot.engagement_score - 0.1)


def _check_streak_milestones(db: Session, patient_id: int, event_type: str):
    """Checks for 7-day and 30-day streak milestones and updates mood if needed."""
    from models.mascot import StreakLog
    streak = db.query(StreakLog).filter(
        StreakLog.patient_id == patient_id,
        StreakLog.streak_type == "DAILY"
    ).first()

    if not streak:
        return

    if streak.current_streak == 7:
        award_xp(db, patient_id, "STREAK_7")
        mascot = db.query(MascotProfile).filter(MascotProfile.patient_id == patient_id).first()
        if mascot:
            mascot.current_mood = "CELEBRATING"
            db.commit()

    elif streak.current_streak == 30:
        award_xp(db, patient_id, "STREAK_30")
        mascot = db.query(MascotProfile).filter(MascotProfile.patient_id == patient_id).first()
        if mascot:
            mascot.current_mood = "CELEBRATING"
            db.commit()


def generate_dialogue(db: Session, patient_id: int, mood: str, mascot_name: str, language: str = "en") -> str:
    """
    Generates contextual dialogue based on mood, language, and templates in DB.
    Falls back to default messages if no template found.
    """
    templates = db.query(DialogueTemplate).filter(
        DialogueTemplate.dialogue_category == mood,
        DialogueTemplate.language_code == language,
        DialogueTemplate.is_active == True
    ).all()

    if not templates:
        # Graceful fallback defaults (these should be seeded in DB)
        fallbacks = {
            "HAPPY": "You're doing great! Keep it up! 🌟",
            "PROUD": "I'm so proud of your consistency! 💪",
            "CELEBRATING": "This is amazing! You're a health champion! 🎉",
            "GENTLE_REMINDER": "Hey, don't forget your medicine. I'm here for you! 🤗",
            "CARING": "I care about you. Let's keep going together. ❤️",
            "CONCERNED": "I'm a little worried. Your health matters a lot.",
            "WORRIED": "I really hope you take your medicine. Please take care.",
            "SAD": "I miss seeing you healthy. Let's try again today.",
            "WELCOME_BACK": "Welcome back! I missed you so much! 😊",
            "MOTIVATIONAL": "You can do this! Every dose counts!",
            "RELIEVED": "So glad you took your medicine! What a relief! 😌",
            "SLEEPY": "Goodnight! Rest well and remember your morning dose. 😴",
            "EXCITED": "This is incredible! You're on fire! 🔥",
            "FOCUSED": "Let's stay focused today. One step at a time.",
        }
        return fallbacks.get(mood, "Stay healthy! I'm with you every step. 💙")

    # Randomly pick from available templates for variety
    template = random.choice(templates)
    return template.template.replace("{mascot_name}", mascot_name)


def get_mascot_state(db: Session, patient_id: int) -> dict:
    """Returns the current mascot state with all metadata."""
    mascot = get_or_create_mascot_profile(db, patient_id)
    mood_state = db.query(MoodState).filter(MoodState.state_id == mascot.current_mood).first()
    evolution = db.query(MascotEvolution).filter(MascotEvolution.level == mascot.current_level).first()

    return {
        "patient_id": patient_id,
        "mascot_name": mascot.mascot_name,
        "current_mood": mascot.current_mood,
        "mood_intensity": mascot.mood_intensity,
        "current_level": mascot.current_level,
        "current_xp": mascot.current_xp,
        "total_xp_earned": mascot.total_xp_earned,
        "engagement_score": mascot.engagement_score,
        "animation_key": mood_state.animation_key if mood_state else None,
        "voice_tone": mood_state.voice_tone if mood_state else None,
        "evolution_name": evolution.name if evolution else "Dosi",
        "cosmetic_name": evolution.cosmetic_name if evolution else None,
        "last_interaction": mascot.last_interaction,
    }
