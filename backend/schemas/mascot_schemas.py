from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# ─── Mascot State ────────────────────────────────────────────────────────────

class MascotStateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    patient_id: int
    mascot_name: str
    current_mood: str
    mood_intensity: float
    current_level: int
    current_xp: int
    total_xp_earned: int
    engagement_score: float
    animation_key: Optional[str] = None
    voice_tone: Optional[str] = None
    last_interaction: Optional[datetime] = None


class MascotNameUpdate(BaseModel):
    mascot_name: str


# ─── Events ──────────────────────────────────────────────────────────────────

class MascotEventPayload(BaseModel):
    event_type: str  # MEDICATION_TAKEN, MISSED_DOSE, APP_OPENED, STREAK_MILESTONE
    patient_id: int
    metadata: Optional[Dict[str, Any]] = None


# ─── XP ──────────────────────────────────────────────────────────────────────

class XPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    patient_id: int
    current_xp: int
    total_xp_earned: int
    current_level: int
    xp_to_next_level: int


class XPLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    action_type: str
    xp_earned: int
    timestamp: datetime


# ─── Streak ──────────────────────────────────────────────────────────────────

class StreakResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    streak_type: str
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[datetime] = None


# ─── Badge ───────────────────────────────────────────────────────────────────

class BadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    badge_key: str
    name: str
    description: Optional[str]
    icon_url: Optional[str]
    unlocked_at: datetime


# ─── Dialogue ────────────────────────────────────────────────────────────────

class DialogueResponse(BaseModel):
    mood: str
    message: str
    voice_tone: str
    animation_key: str
    mascot_name: str


# ─── Evolution ───────────────────────────────────────────────────────────────

class EvolutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    current_level: int
    level_name: str
    cosmetic_name: Optional[str]
    animation_key: Optional[str]
    xp_required: int
    description: Optional[str]
