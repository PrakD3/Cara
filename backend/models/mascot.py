from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from models.database import Base


class MascotProfile(Base):
    """Core mascot profile per patient. Mascot name is set by patient."""
    __tablename__ = "mascot_profiles"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    mascot_name = Column(String, default="Dosi")  # Patient-defined name
    current_mood = Column(String, default="HAPPY")
    mood_intensity = Column(Float, default=0.7)  # 0.0 - 1.0
    current_level = Column(Integer, default=1)
    current_xp = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)
    engagement_score = Column(Float, default=1.0)  # Drops on misses, rises on takes
    last_interaction = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MascotEvolution(Base):
    """Defines mascot evolution levels and cosmetic unlocks."""
    __tablename__ = "mascot_evolutions"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)  # e.g. "Dosi the Brave"
    xp_required = Column(Integer, nullable=False)
    cosmetic_name = Column(String)  # e.g. "bandana", "glasses", "cape"
    animation_key = Column(String)  # Key for frontend animation
    description = Column(Text)


class MoodState(Base):
    """Defines each emotional state and its metadata."""
    __tablename__ = "mood_states"
    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(String, unique=True, nullable=False)  # e.g. HAPPY, WORRIED
    label = Column(String, nullable=False)
    intensity_range_min = Column(Float, default=0.0)
    intensity_range_max = Column(Float, default=1.0)
    dialogue_category = Column(String)  # Maps to dialogue templates
    animation_key = Column(String)  # Frontend animation reference
    voice_tone = Column(String)  # celebratory, calm, caring, etc.
    cooldown_seconds = Column(Integer, default=300)
    priority = Column(Integer, default=5)  # Higher = shown first
    is_active = Column(Boolean, default=True)


class MascotStateLog(Base):
    """Audit log of all mascot mood transitions."""
    __tablename__ = "mascot_state_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_mood = Column(String, nullable=True)
    to_mood = Column(String, nullable=False)
    trigger_event = Column(String)  # e.g. MEDICATION_TAKEN, MISSED_DOSE
    timestamp = Column(DateTime, default=datetime.utcnow)


class XPConfig(Base):
    """Dynamic XP reward configuration — no hardcoding."""
    __tablename__ = "xp_configs"
    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String, unique=True, nullable=False)  # e.g. MEDICATION_TAKEN
    xp_reward = Column(Integer, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)


class XPLog(Base):
    """Records every XP earning event per patient."""
    __tablename__ = "xp_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String, nullable=False)
    xp_earned = Column(Integer, nullable=False)
    extra_data = Column(JSON, nullable=True)  # Extra context e.g. medication name
    timestamp = Column(DateTime, default=datetime.utcnow)


class StreakLog(Base):
    """Tracks streaks per patient per streak type."""
    __tablename__ = "streak_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    streak_type = Column(String, default="DAILY")  # DAILY, WEEKLY, DISEASE_SPECIFIC
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    grace_period_used = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)


class BadgeDefinition(Base):
    """Database-driven badge catalog — add new badges without code changes."""
    __tablename__ = "badge_definitions"
    id = Column(Integer, primary_key=True, index=True)
    badge_key = Column(String, unique=True, nullable=False)  # e.g. first_step
    name = Column(String, nullable=False)
    description = Column(Text)
    icon_url = Column(String, nullable=True)
    unlock_condition_type = Column(String)  # STREAK_COUNT, XP_TOTAL, MEDICATION_COUNT
    unlock_condition_value = Column(Integer)
    xp_reward = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class PatientBadge(Base):
    """Records which badges a patient has earned."""
    __tablename__ = "patient_badges"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badge_definitions.id"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    badge = relationship("BadgeDefinition")


class DialogueTemplate(Base):
    """Database-driven dialogue templates for multilingual, context-aware messages."""
    __tablename__ = "dialogue_templates"
    id = Column(Integer, primary_key=True, index=True)
    dialogue_category = Column(String, nullable=False)  # e.g. HAPPY, CONCERNED
    language_code = Column(String, default="en")
    template = Column(Text, nullable=False)  # Supports {mascot_name}, {patient_name}
    age_group = Column(String, default="all")  # elderly, adult, all
    is_active = Column(Boolean, default=True)
