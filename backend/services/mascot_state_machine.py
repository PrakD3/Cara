"""
Mascot State Machine — defines all valid emotional states and their transitions.
This is NOT hardcoded in Python logic.
States are seeded into the DB at startup; transitions are resolved by the engine.
"""

# Default mood state definitions to seed into DB
DEFAULT_MOOD_STATES = [
    {
        "state_id": "HAPPY",
        "label": "Happy",
        "intensity_range_min": 0.6,
        "intensity_range_max": 0.8,
        "dialogue_category": "HAPPY",
        "animation_key": "anim_happy_bounce",
        "voice_tone": "warm",
        "cooldown_seconds": 300,
        "priority": 5,
    },
    {
        "state_id": "PROUD",
        "label": "Proud",
        "intensity_range_min": 0.7,
        "intensity_range_max": 0.9,
        "dialogue_category": "PROUD",
        "animation_key": "anim_proud_chest",
        "voice_tone": "uplifting",
        "cooldown_seconds": 300,
        "priority": 6,
    },
    {
        "state_id": "CELEBRATING",
        "label": "Celebrating",
        "intensity_range_min": 0.9,
        "intensity_range_max": 1.0,
        "dialogue_category": "CELEBRATING",
        "animation_key": "anim_confetti_dance",
        "voice_tone": "celebratory",
        "cooldown_seconds": 600,
        "priority": 9,
    },
    {
        "state_id": "EXCITED",
        "label": "Excited",
        "intensity_range_min": 0.8,
        "intensity_range_max": 1.0,
        "dialogue_category": "EXCITED",
        "animation_key": "anim_jump_excited",
        "voice_tone": "energetic",
        "cooldown_seconds": 300,
        "priority": 8,
    },
    {
        "state_id": "GENTLE_REMINDER",
        "label": "Gentle Reminder",
        "intensity_range_min": 0.4,
        "intensity_range_max": 0.6,
        "dialogue_category": "GENTLE_REMINDER",
        "animation_key": "anim_tap_shoulder",
        "voice_tone": "soft",
        "cooldown_seconds": 1800,
        "priority": 7,
    },
    {
        "state_id": "CARING",
        "label": "Caring",
        "intensity_range_min": 0.5,
        "intensity_range_max": 0.7,
        "dialogue_category": "CARING",
        "animation_key": "anim_hug_motion",
        "voice_tone": "caring",
        "cooldown_seconds": 600,
        "priority": 5,
    },
    {
        "state_id": "CONCERNED",
        "label": "Concerned",
        "intensity_range_min": 0.4,
        "intensity_range_max": 0.6,
        "dialogue_category": "CONCERNED",
        "animation_key": "anim_worried_look",
        "voice_tone": "gentle",
        "cooldown_seconds": 3600,
        "priority": 7,
    },
    {
        "state_id": "WORRIED",
        "label": "Worried",
        "intensity_range_min": 0.2,
        "intensity_range_max": 0.4,
        "dialogue_category": "WORRIED",
        "animation_key": "anim_pacing_worry",
        "voice_tone": "gentle",
        "cooldown_seconds": 3600,
        "priority": 8,
    },
    {
        "state_id": "SAD",
        "label": "Sad",
        "intensity_range_min": 0.1,
        "intensity_range_max": 0.3,
        "dialogue_category": "SAD",
        "animation_key": "anim_droop_sad",
        "voice_tone": "soft",
        "cooldown_seconds": 7200,
        "priority": 6,
    },
    {
        "state_id": "RELIEVED",
        "label": "Relieved",
        "intensity_range_min": 0.6,
        "intensity_range_max": 0.8,
        "dialogue_category": "RELIEVED",
        "animation_key": "anim_sigh_relief",
        "voice_tone": "warm",
        "cooldown_seconds": 300,
        "priority": 5,
    },
    {
        "state_id": "MOTIVATIONAL",
        "label": "Motivational",
        "intensity_range_min": 0.7,
        "intensity_range_max": 0.9,
        "dialogue_category": "MOTIVATIONAL",
        "animation_key": "anim_fist_pump",
        "voice_tone": "uplifting",
        "cooldown_seconds": 600,
        "priority": 7,
    },
    {
        "state_id": "SLEEPY",
        "label": "Sleepy",
        "intensity_range_min": 0.3,
        "intensity_range_max": 0.5,
        "dialogue_category": "SLEEPY",
        "animation_key": "anim_yawn_sleepy",
        "voice_tone": "calm",
        "cooldown_seconds": 3600,
        "priority": 3,
    },
    {
        "state_id": "WELCOME_BACK",
        "label": "Welcome Back",
        "intensity_range_min": 0.7,
        "intensity_range_max": 0.9,
        "dialogue_category": "WELCOME_BACK",
        "animation_key": "anim_wave_welcome",
        "voice_tone": "warm",
        "cooldown_seconds": 86400,
        "priority": 8,
    },
    {
        "state_id": "FOCUSED",
        "label": "Focused",
        "intensity_range_min": 0.6,
        "intensity_range_max": 0.8,
        "dialogue_category": "FOCUSED",
        "animation_key": "anim_deep_breath",
        "voice_tone": "calm",
        "cooldown_seconds": 600,
        "priority": 5,
    },
]

# Transition rules: event → mood mapping (no code logic, fully data-driven)
TRANSITION_RULES = {
    "MEDICATION_TAKEN": {
        "from": ["HAPPY", "CARING", "GENTLE_REMINDER", "CONCERNED", "FOCUSED"],
        "to": "PROUD",
    },
    "STREAK_MILESTONE_7": {
        "from": ["PROUD", "HAPPY", "EXCITED"],
        "to": "CELEBRATING",
    },
    "STREAK_MILESTONE_30": {
        "from": ["CELEBRATING", "PROUD"],
        "to": "CELEBRATING",
    },
    "MISSED_DOSE_1": {
        "from": ["HAPPY", "PROUD", "CARING"],
        "to": "GENTLE_REMINDER",
    },
    "MISSED_DOSE_2": {
        "from": ["GENTLE_REMINDER", "CARING"],
        "to": "CONCERNED",
    },
    "MISSED_DOSE_3": {
        "from": ["CONCERNED"],
        "to": "WORRIED",
    },
    "MISSED_DOSE_5": {
        "from": ["WORRIED"],
        "to": "SAD",
    },
    "APP_OPENED_AFTER_INACTIVITY": {
        "from": ["SAD", "WORRIED", "SLEEPY"],
        "to": "WELCOME_BACK",
    },
    "MEDICATION_TAKEN_AFTER_MISS": {
        "from": ["CONCERNED", "WORRIED", "SAD", "WELCOME_BACK"],
        "to": "RELIEVED",
    },
    "DAILY_COMPLETE": {
        "from": ["PROUD", "HAPPY", "RELIEVED"],
        "to": "CELEBRATING",
    },
    "NIGHT_CHECK": {
        "from": ["HAPPY", "PROUD"],
        "to": "SLEEPY",
    },
}

# XP reward table (seeds into XPConfig)
DEFAULT_XP_CONFIG = [
    {"action_type": "MEDICATION_TAKEN", "xp_reward": 10, "description": "Patient confirmed taking a medication"},
    {"action_type": "PERFECT_DAY", "xp_reward": 25, "description": "All medications taken in a single day"},
    {"action_type": "STREAK_7", "xp_reward": 50, "description": "7-day adherence streak"},
    {"action_type": "STREAK_30", "xp_reward": 200, "description": "30-day adherence streak"},
    {"action_type": "IVR_RESPONSE", "xp_reward": 5, "description": "Responded to IVR call"},
    {"action_type": "AI_INTERACTION", "xp_reward": 8, "description": "Interacted with AI voice assistant"},
    {"action_type": "APP_OPENED", "xp_reward": 2, "description": "Opened the app"},
    {"action_type": "PREVENTIVE_CARE", "xp_reward": 15, "description": "Engaged in preventive care activity"},
]

# Level progression table
LEVEL_DEFINITIONS = [
    {"level": 1, "name": "Dosi Beginner", "xp_required": 0, "cosmetic_name": None, "animation_key": "anim_level1", "description": "Just starting the health journey"},
    {"level": 2, "name": "Dosi with Bandana", "xp_required": 100, "cosmetic_name": "bandana", "animation_key": "anim_level2", "description": "A week of consistency unlocked the bandana"},
    {"level": 3, "name": "Dosi with Glasses", "xp_required": 300, "cosmetic_name": "glasses", "animation_key": "anim_level3", "description": "Dosi is getting wise and consistent"},
    {"level": 4, "name": "Dosi with Cape", "xp_required": 700, "cosmetic_name": "cape", "animation_key": "anim_level4", "description": "A true healthcare hero"},
    {"level": 5, "name": "Golden Dosi", "xp_required": 1500, "cosmetic_name": "golden_glow", "animation_key": "anim_level5_golden", "description": "The highest form of Dosi — legendary adherence"},
]

# Default badge catalog
DEFAULT_BADGES = [
    {"badge_key": "first_step", "name": "First Step", "description": "Took first medication", "unlock_condition_type": "MEDICATION_COUNT", "unlock_condition_value": 1, "xp_reward": 10},
    {"badge_key": "one_week_hero", "name": "One Week Hero", "description": "7-day streak", "unlock_condition_type": "STREAK_COUNT", "unlock_condition_value": 7, "xp_reward": 50},
    {"badge_key": "consistency_champion", "name": "Consistency Champion", "description": "30-day streak", "unlock_condition_type": "STREAK_COUNT", "unlock_condition_value": 30, "xp_reward": 200},
    {"badge_key": "diabetes_warrior", "name": "Diabetes Warrior", "description": "30 days of diabetes medication adherence", "unlock_condition_type": "DISEASE_STREAK", "unlock_condition_value": 30, "xp_reward": 150},
    {"badge_key": "heart_guardian", "name": "Heart Guardian", "description": "30 days of cardiac medication adherence", "unlock_condition_type": "DISEASE_STREAK", "unlock_condition_value": 30, "xp_reward": 150},
    {"badge_key": "perfect_week", "name": "Perfect Week", "description": "7 consecutive perfect days", "unlock_condition_type": "STREAK_COUNT", "unlock_condition_value": 7, "xp_reward": 75},
    {"badge_key": "preventive_care_hero", "name": "Preventive Care Hero", "description": "Completed 10 preventive care actions", "unlock_condition_type": "PREVENTIVE_CARE_COUNT", "unlock_condition_value": 10, "xp_reward": 100},
]
