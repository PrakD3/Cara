from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from models.database import get_db
from models.domain import User
from api.deps import get_current_user
from schemas.mascot_schemas import (
    MascotEventPayload, MascotStateResponse, DialogueResponse,
    XPResponse, StreakResponse, BadgeResponse, EvolutionResponse,
    MascotNameUpdate
)
from services.mascot_service import (
    get_mascot_state, process_mascot_event, generate_dialogue,
    get_or_create_mascot_profile
)
from services.xp_engine import get_xp_summary
from services.streak_engine import get_streak_summary
from services.badge_engine import get_patient_badges
from models.mascot import MascotEvolution, StreakLog
from websocket.connection_manager import manager
import json
import logging
import asyncio

router = APIRouter()
logger = logging.getLogger("cara.mascot.router")


# ─── GET: Current Mascot State ───────────────────────────────────────────────

@router.get("/state")
def get_state(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns the full current mascot emotional state for the authenticated patient."""
    return get_mascot_state(db, current_user.id)


# ─── GET: Contextual Dialogue ─────────────────────────────────────────────────

@router.get("/dialogue", response_model=DialogueResponse)
def get_dialogue(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns a contextual dialogue message for the current mascot mood."""
    mascot = get_or_create_mascot_profile(db, current_user.id)
    from models.mascot import MoodState
    mood_state = db.query(MoodState).filter(MoodState.state_id == mascot.current_mood).first()

    dialogue = generate_dialogue(db, current_user.id, mascot.current_mood, mascot.mascot_name)
    return {
        "mood": mascot.current_mood,
        "message": dialogue,
        "voice_tone": mood_state.voice_tone if mood_state else "warm",
        "animation_key": mood_state.animation_key if mood_state else "anim_happy_bounce",
        "mascot_name": mascot.mascot_name,
    }


# ─── POST: Fire Mascot Event ──────────────────────────────────────────────────

@router.post("/event")
def fire_event(
    payload: MascotEventPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fires a mascot event and triggers mood transitions, XP awards, streak updates,
    badge evaluations, and real-time WebSocket broadcasts.
    """
    result = process_mascot_event(db, current_user.id, payload.event_type, payload.metadata)
    return result


# ─── GET: XP Summary ─────────────────────────────────────────────────────────

@router.get("/xp")
def get_xp(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns XP summary including current level and XP to next level."""
    return get_xp_summary(db, current_user.id)


# ─── GET: Streak Summary ──────────────────────────────────────────────────────

@router.get("/streak")
def get_streak(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns all active streaks for the current patient."""
    return get_streak_summary(db, current_user.id)


# ─── GET: Badges ──────────────────────────────────────────────────────────────

@router.get("/badges")
def get_badges(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns all earned badges for the current patient."""
    return get_patient_badges(db, current_user.id)


# ─── GET: Evolution ───────────────────────────────────────────────────────────

@router.get("/evolution")
def get_evolution(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns the patient's mascot evolution details."""
    mascot = get_or_create_mascot_profile(db, current_user.id)
    evolution = db.query(MascotEvolution).filter(MascotEvolution.level == mascot.current_level).first()
    if not evolution:
        raise HTTPException(status_code=404, detail="Evolution data not found")
    return {
        "current_level": evolution.level,
        "level_name": evolution.name,
        "cosmetic_name": evolution.cosmetic_name,
        "animation_key": evolution.animation_key,
        "xp_required": evolution.xp_required,
        "description": evolution.description,
    }


# ─── PATCH: Update Mascot Name ────────────────────────────────────────────────

@router.patch("/name")
def update_mascot_name(
    payload: MascotNameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Allows patient to rename their mascot."""
    mascot = get_or_create_mascot_profile(db, current_user.id)
    if not payload.mascot_name or len(payload.mascot_name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Mascot name cannot be empty")
    mascot.mascot_name = payload.mascot_name.strip()
    db.commit()
    return {"message": f"Mascot renamed to {mascot.mascot_name}", "mascot_name": mascot.mascot_name}


# ─── WebSocket: Live Mascot Feed ─────────────────────────────────────────────

@router.websocket("/ws/{patient_id}")
async def mascot_websocket(websocket: WebSocket, patient_id: int):
    """
    WebSocket endpoint for real-time mascot state updates.
    Frontend connects here to receive live mood, XP, badge, streak events.
    """
    await manager.connect(websocket, patient_id)
    try:
        while True:
            # Keep alive — listen for client ping, respond with pong
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket, patient_id)
        logger.info(f"Patient {patient_id} disconnected from mascot WebSocket")
