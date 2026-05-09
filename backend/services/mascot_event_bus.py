"""
Mascot Event Bus — Redis Pub/Sub layer for real-time mascot state broadcasting.
All events are published here and consumed by the WebSocket handler.
"""
import redis
import json
import logging
from core.config import settings

logger = logging.getLogger("cara.mascot.eventbus")

try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception as e:
    logger.warning(f"Redis not available: {e}. Real-time events disabled.")
    redis_client = None


def _publish(channel: str, payload: dict):
    """Publishes a message to a Redis pub/sub channel."""
    if redis_client is None:
        logger.debug(f"[MOCK PUBLISH] {channel}: {payload}")
        return
    try:
        redis_client.publish(channel, json.dumps(payload))
    except Exception as e:
        logger.error(f"Redis publish error on {channel}: {e}")


def publish_mood_event(patient_id: int, mood: str, intensity: float, animation_key: str, voice_tone: str, dialogue: str):
    _publish(f"mascot:{patient_id}", {
        "event": "MOOD_UPDATE",
        "patient_id": patient_id,
        "mood": mood,
        "intensity": intensity,
        "animation_key": animation_key,
        "voice_tone": voice_tone,
        "dialogue": dialogue,
    })


def publish_xp_event(patient_id: int, xp_earned: int, action_type: str):
    _publish(f"mascot:{patient_id}", {
        "event": "XP_EARNED",
        "patient_id": patient_id,
        "xp_earned": xp_earned,
        "action_type": action_type,
    })


def publish_streak_event(patient_id: int, streak_type: str, current_streak: int, longest_streak: int):
    _publish(f"mascot:{patient_id}", {
        "event": "STREAK_UPDATE",
        "patient_id": patient_id,
        "streak_type": streak_type,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    })


def publish_badge_event(patient_id: int, badge_key: str, badge_name: str):
    _publish(f"mascot:{patient_id}", {
        "event": "BADGE_UNLOCKED",
        "patient_id": patient_id,
        "badge_key": badge_key,
        "badge_name": badge_name,
    })


def publish_celebration_event(patient_id: int, celebration_type: str):
    _publish(f"mascot:{patient_id}", {
        "event": "CELEBRATION",
        "patient_id": patient_id,
        "celebration_type": celebration_type,
    })


def publish_evolution_event(patient_id: int, new_level: int, cosmetic_name: str):
    _publish(f"mascot:{patient_id}", {
        "event": "EVOLUTION",
        "patient_id": patient_id,
        "new_level": new_level,
        "cosmetic_name": cosmetic_name,
    })
