# CARA — Full Project Build Prompt v2
> Combined architecture: CARA's behavioral engagement + MedBuddy's tech depth
> Paste this entire document into Cursor, Claude Code, or any AI coding assistant.
> ONE codebase → Web + iOS + Android | HIPAA & GDPR compliant | 24hr buildable

---

## What CARA Is

**CARA** (Contextual Adherence & Recovery Architecture) is a mobile-first medication adherence ecosystem — not just a reminder app. It is a behavioral health companion with:

- A friendly mascot (Dosi) that creates emotional investment
- Adaptive reminders that escalate intelligently (Telegram → WhatsApp → IVR voice → Caregiver → Doctor)
- AI health coaching via Gemini (free tier)
- ML-based risk prediction to flag high-risk patients before they deteriorate
- A gamification engine (streaks, XP, badges, Dosi evolution)
- A doctor dashboard with traffic-light prioritization
- Full support for elderly users via IVR voice calls (no smartphone required)

---

## Tech Stack (Combined — Best of Both)

### Client — ONE codebase, three platforms
| Layer | Technology | Why |
|---|---|---|
| Framework | **Expo + React Native** (with Expo Router) | Single codebase → Web PWA + iOS + Android |
| Web renderer | **React Native Web** | Same components render in browser |
| Styling | **NativeWind** (Tailwind for React Native) | Tailwind syntax across all platforms |
| Navigation | **Expo Router** (file-based) | Same routing pattern as Next.js |
| State | **Zustand** | Lightweight, works on all platforms |
| Data fetching | **TanStack Query v5** | Caching, background refresh, offline support |
| Forms | **React Hook Form + Zod** | Validation on all platforms |
| Charts | **Victory Native** | Works on RN + Web |
| Animations | **React Native Reanimated 3** | 60fps native animations for Dosi |
| Push notifications | **Expo Push Notifications** | iOS + Android + Web, free |
| PWA | **Expo web build** + `manifest.json` | Installable on home screen |

### Backend / Gateway
| Layer | Technology | Why |
|---|---|---|
| Framework | **FastAPI** (Python 3.11) | Auto OpenAPI docs, async, great for ML |
| Gateway | **FastAPI** with JWT middleware | Rate limiting, CORS, HTTPS only |
| Auth | **JWT + 2FA** (TOTP via pyotp) | Secure, stateless |
| Job scheduler | **APScheduler** (Python) | Cron-style reminder engine |
| Queue | **Redis + RQ** (Redis Queue) | Escalation pipeline, async jobs |
| ORM | **SQLAlchemy + Alembic** | Schema migrations |
| API validation | **Pydantic v2** | Request/response schemas with auto docs |

### AI / ML Layer
| Service | Technology | Why |
|---|---|---|
| Health coach AI | **Gemini 1.5 Flash API** (Google free tier) | Conversational health guidance |
| Behavior engine | **Custom Python service** | Learns patient timing patterns, adjusts reminders |
| Adherence ML | **scikit-learn** | Risk predictor (RandomForest on miss patterns) |
| Vector search | **Pinecone** (free tier) | Semantic search over health knowledge base |

### Data Layer
| Service | Technology | Why |
|---|---|---|
| Primary DB | **Supabase** (PostgreSQL + RLS) | Row-level security baked in, free tier |
| Cache / Queue | **Redis** (Upstash free tier) | Sessions, job queue, rate limiting |
| File storage | **Supabase Storage** | Profile pictures, exports |

### Communication Channels
| Channel | Technology | Target users |
|---|---|---|
| WhatsApp | **WhatsApp Cloud API** (Meta, free) | Primary for India — widest reach |
| Telegram | **python-telegram-bot** | Tech-savvy users, bots |
| IVR Voice | **Exotel REST API** | Elderly, keypad phone users — strongest differentiator |
| SMS | **MSG91** | Fallback for all users |
| Push | **Expo Push** (free) | App users, iOS + Android + Web |

### Infrastructure
| Service | Technology |
|---|---|
| Frontend hosting | **Vercel** (Expo web build) |
| Backend hosting | **Railway** or **Render** |
| Database | **Supabase** (PostgreSQL) |
| Cache | **Upstash Redis** |
| CDN / Edge | **Vercel Edge Network** (SSL/TLS, DDoS, static) |
| CI/CD | **GitHub Actions** |
| Monitoring | **Sentry** (free tier) |

### Compliance
| Requirement | Implementation |
|---|---|
| HIPAA | AES-256 encryption for PHI at rest, zero PHI in messages |
| GDPR | Consent management, "delete my data" endpoint, data minimization |
| Audit logging | Every access to patient data logged with timestamp + actor |
| RLS | Supabase Row Level Security — patients can only see their own data |
| TLS | All traffic HTTPS only, enforced at Vercel edge |

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                              │
│   ┌──────────────────┐        ┌────────────────────────┐   │
│   │   Web PWA        │        │   Mobile App           │   │
│   │   Expo Web       │        │   Expo React Native    │   │
│   │   React + NW     │        │   iOS & Android        │   │
│   └──────────────────┘        └────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              VERCEL EDGE NETWORK                            │
│        CDN · SSL/TLS · DDoS protection · static hosting    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  FastAPI GATEWAY                            │
│       JWT auth · rate limiting · CORS · Pydantic validation │
└──────┬──────────┬──────────┬──────────┬────────────────────┘
       │          │          │          │
┌──────▼──┐ ┌────▼────┐ ┌───▼────┐ ┌──▼──────────┐ ┌────────┐
│  Auth   │ │  Meds   │ │AI Coach│ │  Notify     │ │Analytics│
│JWT + 2FA│ │schedules│ │ Gemini │ │push/WA/IVR  │ │ reports │
└─────────┘ └─────────┘ └───┬────┘ └─────────────┘ └────────┘
                             │
           ┌─────────────────┼──────────────────┐
    ┌───────▼──────┐ ┌───────▼──────┐ ┌─────────▼──────┐
    │  Gemini API  │ │  Behavior    │ │  Adherence ML  │
    │  health coach│ │  engine      │ │  risk predictor│
    │  free · GCP  │ │  smart timing│ │  scikit-learn  │
    └──────────────┘ └──────────────┘ └────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────┐
│                       DATA LAYER                            │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │  Supabase    │  │   Redis    │  │    Pinecone        │  │
│  │ PostgreSQL   │  │ sessions   │  │   vector DB        │  │
│  │   + RLS      │  │  + cache   │  │      free          │  │
│  └──────────────┘  └────────────┘  └────────────────────┘  │
└──────────┬─────────────────────────────────────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────┐
│                    EXTERNAL CHANNELS                        │
│  ┌────────────────────┐        ┌─────────────────────────┐  │
│  │  WhatsApp Cloud API│        │    Expo Push            │  │
│  │  Meta free tier    │        │    iOS · Android · Web  │  │
│  │  elderly channel   │        │    free                 │  │
│  ├────────────────────┤        └─────────────────────────┘  │
│  │  Exotel IVR        │                                     │
│  │  voice calls       │                                     │
│  │  keypad phone users│                                     │
│  ├────────────────────┤                                     │
│  │  Telegram Bot      │                                     │
│  │  MSG91 SMS         │                                     │
│  └────────────────────┘                                     │
└────────────────────────────────────────────────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────┐
│                     COMPLIANCE                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │    HIPAA     │  │     GDPR     │  │  Audit logging   │  │
│  │ AES-256 PHI  │  │ consent +    │  │ all access       │  │
│  │   encrypt    │  │   deletion   │  │   tracked        │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
cara/
├── apps/
│   ├── mobile/                         # Expo React Native (Web + iOS + Android)
│   │   ├── app/                        # Expo Router file-based routing
│   │   │   ├── (auth)/
│   │   │   │   ├── login.tsx
│   │   │   │   └── register.tsx
│   │   │   ├── (patient)/
│   │   │   │   ├── _layout.tsx         # Bottom tab navigator
│   │   │   │   ├── dashboard.tsx
│   │   │   │   ├── medications.tsx
│   │   │   │   ├── schedule.tsx
│   │   │   │   ├── streaks.tsx
│   │   │   │   └── profile.tsx
│   │   │   ├── (caregiver)/
│   │   │   │   └── care/[patientId].tsx
│   │   │   ├── (doctor)/
│   │   │   │   └── doctor/dashboard.tsx
│   │   │   └── _layout.tsx
│   │   ├── components/
│   │   │   ├── dosi/                   # Dosi mascot + animations
│   │   │   ├── medications/
│   │   │   ├── dashboard/
│   │   │   ├── charts/
│   │   │   └── ui/                     # Shared design system
│   │   ├── lib/
│   │   │   ├── api.ts                  # TanStack Query + axios
│   │   │   ├── auth.ts
│   │   │   └── store.ts                # Zustand stores
│   │   ├── hooks/
│   │   ├── constants/
│   │   └── assets/
│   │
│   └── api/                            # FastAPI backend
│       ├── main.py
│       ├── routers/
│       │   ├── auth.py
│       │   ├── patients.py
│       │   ├── medications.py
│       │   ├── adherence.py
│       │   ├── caregiver.py
│       │   ├── doctor.py
│       │   ├── ai_coach.py
│       │   ├── notifications.py
│       │   └── webhooks.py
│       ├── services/
│       │   ├── adherence_engine.py
│       │   ├── behavior_engine.py      # ML timing predictor
│       │   ├── risk_predictor.py       # scikit-learn model
│       │   ├── gemini_coach.py         # Gemini AI health coach
│       │   ├── telegram_bot.py
│       │   ├── whatsapp_service.py
│       │   ├── ivr_service.py          # Exotel IVR
│       │   ├── sms_service.py
│       │   ├── push_service.py         # Expo Push
│       │   └── gamification.py
│       ├── jobs/
│       │   ├── reminder_scheduler.py   # APScheduler cron
│       │   └── escalation_worker.py    # RQ worker
│       ├── models/
│       │   └── database.py             # SQLAlchemy models
│       ├── schemas/
│       │   └── pydantic_models.py      # Pydantic v2 schemas
│       ├── middleware/
│       │   ├── auth.py
│       │   ├── rate_limit.py
│       │   └── audit_log.py
│       ├── ml/
│       │   ├── train_risk_model.py
│       │   └── risk_model.pkl          # Saved sklearn model
│       ├── alembic/                    # DB migrations
│       └── requirements.txt
│
└── packages/
    └── shared-types/                   # Shared TypeScript types (generated from Pydantic)
```

---

## Database Schema (SQLAlchemy / PostgreSQL)

```python
# models/database.py

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Enum, ARRAY
from sqlalchemy.orm import relationship
import enum

class UserRole(str, enum.Enum):
    PATIENT = "PATIENT"
    CAREGIVER = "CAREGIVER"
    DOCTOR = "DOCTOR"

class ReminderChannel(str, enum.Enum):
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"
    IVR = "IVR"
    SMS = "SMS"
    PUSH = "PUSH"

class AdherenceStatus(str, enum.Enum):
    TAKEN = "TAKEN"
    MISSED = "MISSED"
    LATE = "LATE"
    SKIPPED = "SKIPPED"

class RiskLevel(str, enum.Enum):
    STABLE = "STABLE"      # ≥80% adherence, 0 consecutive misses
    AT_RISK = "AT_RISK"    # 60-79% or 2 consecutive misses
    CRITICAL = "CRITICAL"  # <60% or 3+ consecutive misses

class TimeSlot(str, enum.Enum):
    MORNING = "MORNING"      # default 08:00
    AFTERNOON = "AFTERNOON"  # default 13:00
    NIGHT = "NIGHT"          # default 21:00

# --- User ---
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=cuid)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.PATIENT)
    preferred_channel = Column(Enum(ReminderChannel), default=ReminderChannel.WHATSAPP)
    preferred_language = Column(String, default="en")  # en|hi|ta|te|kn
    whatsapp_number = Column(String)
    telegram_chat_id = Column(String, unique=True)
    expo_push_token = Column(String)
    totp_secret = Column(String)          # 2FA
    created_at = Column(DateTime, default=datetime.utcnow)

# --- PatientProfile ---
class PatientProfile(Base):
    __tablename__ = "patient_profiles"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    date_of_birth = Column(DateTime)
    conditions = Column(ARRAY(String))    # encrypted at rest
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    dosi_level = Column(Integer, default=1)  # 1-5
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.STABLE)
    risk_score = Column(Float, default=0.0)  # ML model output 0.0-1.0
    last_dose_at = Column(DateTime)
    # Behavior engine learned times
    learned_morning_time = Column(String)    # e.g. "08:30"
    learned_afternoon_time = Column(String)
    learned_night_time = Column(String)

# --- Medication ---
class Medication(Base):
    __tablename__ = "medications"
    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient_profiles.id"))
    name_encrypted = Column(String)       # AES-256 encrypted (HIPAA)
    dosage = Column(String)
    unit = Column(String, default="mg")
    instructions_encrypted = Column(String)
    color = Column(String)                # UI color: "indigo"|"rose"|"amber" etc
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

# --- MedicationSchedule ---
class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"
    id = Column(String, primary_key=True)
    medication_id = Column(String, ForeignKey("medications.id"))
    time_slot = Column(Enum(TimeSlot))    # MORNING | AFTERNOON | NIGHT
    scheduled_time = Column(String)       # "08:00" — overridden by behavior engine
    days_of_week = Column(ARRAY(Integer)) # [1,2,3,4,5,6,7]
    is_active = Column(Boolean, default=True)

# --- AdherenceLog ---
class AdherenceLog(Base):
    __tablename__ = "adherence_logs"
    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient_profiles.id"))
    medication_id = Column(String, ForeignKey("medications.id"))
    scheduled_at = Column(DateTime)
    responded_at = Column(DateTime)
    status = Column(Enum(AdherenceStatus))
    channel = Column(Enum(ReminderChannel))
    escalation_stage = Column(Integer, default=1)  # which stage responded
    note = Column(String)

# --- Badge, PatientBadge, CaregiverLink, DoctorLink, Notification ---
# (same structure as v1, add audit_logs table below)

# --- AuditLog (HIPAA/GDPR requirement) ---
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    actor_id = Column(String)             # who performed the action
    action = Column(String)               # "READ_PATIENT" | "UPDATE_MED" etc
    resource_type = Column(String)
    resource_id = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)
```

Supabase RLS policies (run after migration):
```sql
-- Patients can only see their own data
ALTER TABLE patient_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "patient_own_data" ON patient_profiles
  FOR ALL USING (user_id = auth.uid());

-- Caregivers can only see linked patients
CREATE POLICY "caregiver_linked_patients" ON patient_profiles
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM caregiver_links
      WHERE caregiver_id = auth.uid()
      AND patient_id = patient_profiles.id
      AND is_active = true
    )
  );

-- Doctors same pattern
CREATE POLICY "doctor_linked_patients" ON patient_profiles
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM doctor_links
      WHERE doctor_id = auth.uid()
      AND patient_id = patient_profiles.id
    )
  );
```

---

## Backend API Routes (FastAPI)

```python
# Auto-documented at /docs (Swagger UI) and /redoc

# Auth
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/verify-otp          # 2FA
POST   /api/auth/refresh
DELETE /api/auth/logout

# Patient
GET    /api/patients/profile
PUT    /api/patients/profile
GET    /api/patients/dashboard        # streak, XP, Dosi state, today's schedule
DELETE /api/patients/data             # GDPR right to erasure

# Medications
GET    /api/medications
POST   /api/medications
PUT    /api/medications/{id}
DELETE /api/medications/{id}

# Schedule
GET    /api/schedule/today            # grouped Morning/Afternoon/Night
GET    /api/schedule/week
GET    /api/schedule/month            # heatmap data

# Adherence
POST   /api/adherence/log            # mark dose taken
GET    /api/adherence/history         # last 30 days
GET    /api/adherence/stats           # %, streak, miss patterns
GET    /api/adherence/heatmap         # calendar data

# AI Coach
POST   /api/ai/chat                  # Gemini health coach conversation
GET    /api/ai/insights              # weekly AI-generated insight summary

# Caregiver
GET    /api/caregiver/patients
GET    /api/caregiver/patient/{id}
POST   /api/caregiver/encourage/{id} # send encouragement message

# Doctor
GET    /api/doctor/patients          # sorted by risk level
GET    /api/doctor/patient/{id}
POST   /api/doctor/flag/{id}         # manually flag as critical

# Badges
GET    /api/badges/all
GET    /api/badges/earned

# Webhooks (internal — not public)
POST   /api/webhooks/telegram
POST   /api/webhooks/whatsapp
POST   /api/webhooks/ivr             # Exotel callback
POST   /api/webhooks/sms             # MSG91 delivery
```

---

## Core Services — Detailed Implementation

### 1. Reminder Scheduler (APScheduler)

```python
# jobs/reminder_scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', minute='*')   # every minute
async def check_due_reminders():
    now = datetime.utcnow()
    due = await get_due_reminders(now)          # query schedules due in this minute
    for reminder in due:
        # Use learned time if behavior engine has data, else default
        await escalation_queue.enqueue(
            send_stage_1_reminder,
            reminder,
            job_timeout=600
        )

# Behavior engine overrides scheduled_time with learned_time
# e.g. patient always takes morning meds at 8:45 not 8:00
# → system shifts reminder window to 8:40
```

### 2. Escalation Pipeline (Redis Queue)

```python
# jobs/escalation_worker.py

# Stage 1 — immediate (preferred channel: WhatsApp / Telegram / Push)
# Stage 2 — +30 min if no response → IVR voice call
# Stage 3 — +60 min if still no response → Caregiver WhatsApp alert
# Stage 4 — 2+ consecutive misses → Doctor risk flag + ML risk score update

async def send_stage_1_reminder(reminder):
    patient = await get_patient(reminder.patient_id)
    channel = patient.preferred_channel

    msg = build_privacy_safe_message(patient.name, reminder.time_slot)
    # "Time for your scheduled dose, Lakshmi! ✅"
    # NEVER includes drug name or condition

    if channel == "WHATSAPP":
        await whatsapp_service.send_interactive(
            to=patient.whatsapp_number,
            body=msg,
            buttons=["✅ Taken", "⏰ Remind in 15 min", "❌ Skip"]
        )
    elif channel == "TELEGRAM":
        await telegram_bot.send_inline_keyboard(patient.telegram_chat_id, msg)
    elif channel == "PUSH":
        await expo_push.send(patient.expo_push_token, msg)

    # Schedule stage 2 in 30 minutes if no response logged
    await escalation_queue.enqueue_in(
        timedelta(minutes=30),
        check_and_escalate_stage_2,
        reminder
    )

async def send_stage_2_ivr(reminder):
    patient = await get_patient(reminder.patient_id)
    script = get_ivr_script(patient.name, patient.preferred_language, reminder.time_slot)
    # "Hello Lakshmi, this is CARA. Press 1 if you've taken your medicine."
    await exotel_service.make_call(
        to=patient.phone,
        script=script,
        callback_url="/api/webhooks/ivr"
    )

async def send_stage_3_caregiver(reminder):
    caregivers = await get_linked_caregivers(reminder.patient_id)
    patient = await get_patient(reminder.patient_id)
    for cg in caregivers:
        # Human-readable, not "adherence score: 61%"
        msg = f"Your {get_relation(cg, patient)} missed their {reminder.time_slot.lower()} medication today."
        await whatsapp_service.send(cg.whatsapp_number, msg)

async def send_stage_4_doctor_flag(patient_id):
    await update_risk_level(patient_id)  # re-run ML model
    await notify_linked_doctors(patient_id)
```

### 3. Gemini AI Health Coach

```python
# services/gemini_coach.py

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])  # free tier
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are Dosi, a friendly medication adherence companion for CARA.
You help patients understand their health journey and stay motivated.
STRICT RULES:
- Never provide specific medical advice or diagnose
- Never tell patients to change dosage
- Always encourage them to consult their doctor for medical questions
- Keep responses short (2-3 sentences max) — users are on mobile
- Be warm, encouraging, like a supportive friend
- If asked about their specific medications, say you can see they have a schedule set up
  but never name the drug (privacy)
"""

async def chat(patient_id: str, user_message: str, history: list) -> str:
    patient = await get_patient_summary(patient_id)  # streak, adherence %, risk level
    context = f"Patient streak: {patient.streak} days. Adherence this week: {patient.weekly_pct}%."

    chat = model.start_chat(history=history)
    response = await chat.send_message_async(
        f"{SYSTEM_PROMPT}\n\nContext: {context}\n\nUser: {user_message}"
    )
    return response.text

async def generate_weekly_insight(patient_id: str) -> str:
    stats = await get_adherence_stats(patient_id, days=7)
    prompt = f"""Generate a 2-sentence encouraging weekly summary for a patient with:
    - Adherence: {stats.percentage}%
    - Streak: {stats.streak} days
    - Best slot: {stats.best_slot}
    - Worst slot: {stats.worst_slot}
    Keep it warm and motivating. Do not mention any drug names."""
    response = await model.generate_content_async(prompt)
    return response.text
```

### 4. Adherence ML Risk Predictor (scikit-learn)

```python
# services/risk_predictor.py

from sklearn.ensemble import RandomForestClassifier
import joblib

# Features used for risk prediction:
FEATURES = [
    "adherence_7d_pct",       # % doses taken in last 7 days
    "adherence_30d_pct",       # % doses taken in last 30 days
    "consecutive_misses",      # current run of consecutive missed doses
    "morning_miss_rate",       # miss rate by time slot
    "afternoon_miss_rate",
    "night_miss_rate",
    "response_to_ivr_rate",    # did patient respond when called
    "days_since_last_taken",   # recency
    "num_medications",         # complexity of regimen
    "age_bucket",              # 0=<40, 1=40-65, 2=65+
]

# Output: 0=STABLE, 1=AT_RISK, 2=CRITICAL
# Model is pre-trained on synthetic data for hackathon
# In production: retrain weekly on real anonymized data

async def predict_risk(patient_id: str) -> RiskLevel:
    features = await extract_features(patient_id)
    model = joblib.load("ml/risk_model.pkl")
    risk_score = model.predict_proba([features])[0][2]  # probability of CRITICAL
    label = model.predict([features])[0]
    await update_patient_risk_score(patient_id, risk_score, label)
    return RiskLevel(label)
```

### 5. Behavior Engine (Adaptive Timing)

```python
# services/behavior_engine.py

# Learns when each patient actually responds to reminders
# Shifts reminder time to 10 minutes before their typical response time

async def update_learned_times(patient_id: str):
    logs = await get_last_30_adherence_logs(patient_id)

    for slot in ["MORNING", "AFTERNOON", "NIGHT"]:
        slot_logs = [l for l in logs if l.time_slot == slot and l.status == "TAKEN"]
        if len(slot_logs) >= 5:  # need enough data
            response_times = [l.responded_at.strftime("%H:%M") for l in slot_logs]
            avg_time = calculate_average_time(response_times)
            # Set reminder 10 minutes before their usual response time
            learned_time = subtract_minutes(avg_time, 10)
            await update_patient_learned_time(patient_id, slot, learned_time)
```

### 6. WhatsApp Cloud API

```python
# services/whatsapp_service.py

WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/{phone_id}/messages"
HEADERS = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

async def send_interactive(to: str, body: str, buttons: list[str]):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": btn.lower().replace(" ", "_"), "title": btn}}
                    for btn in buttons[:3]  # WhatsApp max 3 buttons
                ]
            }
        }
    }
    async with httpx.AsyncClient() as client:
        await client.post(WHATSAPP_API_URL, json=payload, headers=HEADERS)
```

### 7. IVR Voice Call (Exotel)

```python
# services/ivr_service.py

IVR_SCRIPTS = {
    "en": "Hello {name}, this is CARA. It is time for your scheduled medication. Press 1 if you have taken your medicine. Press 2 to be reminded in 15 minutes.",
    "hi": "नमस्ते {name}, मैं CARA हूँ। आपकी दवा का समय हो गया है। अगर आपने दवा ले ली है तो 1 दबाएं।",
    "ta": "வணக்கம் {name}, நான் CARA. உங்கள் மருந்து நேரம் ஆகிவிட்டது. மருந்து சாப்பிட்டிருந்தால் 1 அழுத்தவும்.",
}

async def make_call(to: str, patient_name: str, language: str, callback_url: str):
    script = IVR_SCRIPTS.get(language, IVR_SCRIPTS["en"]).format(name=patient_name)
    response = await exotel_client.calls.create(
        From=EXOTEL_FROM_NUMBER,
        To=to,
        Url=f"{BASE_URL}/api/webhooks/ivr",
        CallType="trans",
        StatusCallback=callback_url,
        CustomField=script,
    )
    return response.sid

# Webhook handler for keypress response
@router.post("/webhooks/ivr")
async def ivr_callback(digit: str = Form(...), custom_field: str = Form(...)):
    if digit == "1":
        await log_adherence(TAKEN, channel=IVR)
        await trigger_dosi_celebration(patient_id)
    elif digit == "2":
        await schedule_retry(minutes=15)
    else:
        await escalate_to_caregiver(patient_id)
```

---

## Mobile App — Expo React Native

### Expo Router Structure

```tsx
// app/(patient)/_layout.tsx — Bottom Tab Navigator

import { Tabs } from 'expo-router';
import { Home, Pill, Trophy, User } from 'lucide-react-native';

export default function PatientLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarStyle: {
          paddingBottom: insets.bottom,  // safe area for iPhone/Android
          height: 60 + insets.bottom,
        },
        tabBarActiveTintColor: '#6366f1',
      }}
    >
      <Tabs.Screen name="dashboard" options={{ title: 'Home', tabBarIcon: Home }} />
      <Tabs.Screen name="medications" options={{ title: 'Meds', tabBarIcon: Pill }} />
      <Tabs.Screen name="streaks" options={{ title: 'Streaks', tabBarIcon: Trophy }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile', tabBarIcon: User }} />
    </Tabs>
  );
}
```

### Patient Dashboard

```tsx
// app/(patient)/dashboard.tsx

export default function Dashboard() {
  const { data: dashboard } = useQuery({ queryKey: ['dashboard'], queryFn: fetchDashboard });

  return (
    <ScrollView
      className="flex-1 bg-gray-50"
      contentContainerStyle={{ paddingBottom: insets.bottom + 80 }}
      refreshControl={<RefreshControl onRefresh={refetch} />}
    >
      {/* Dosi Mascot */}
      <DosiMascot
        state={dashboard.dosiState}
        streak={dashboard.streak}
        level={dashboard.dosiLevel}
        size="lg"
      />

      {/* Streak + XP */}
      <StreakCard streak={dashboard.streak} xp={dashboard.totalXP} level={dashboard.dosiLevel} />

      {/* Today's Schedule — Morning / Afternoon / Night */}
      <ScheduleSection slot="MORNING" medications={dashboard.morning} onTaken={markTaken} />
      <ScheduleSection slot="AFTERNOON" medications={dashboard.afternoon} onTaken={markTaken} />
      <ScheduleSection slot="NIGHT" medications={dashboard.night} onTaken={markTaken} />

      {/* 7-day adherence ring */}
      <AdherenceChart data={dashboard.weeklyStats} />

      {/* AI Coach message */}
      <AIInsightCard message={dashboard.weeklyInsight} />

      {/* Recent badges */}
      <BadgesRow badges={dashboard.recentBadges} />
    </ScrollView>
  );
}
```

### Dosi Mascot Component

```tsx
// components/dosi/DosiMascot.tsx
import Animated, { useSharedValue, withSpring, withRepeat } from 'react-native-reanimated';

type DosiState = 'happy' | 'neutral' | 'sad' | 'celebrating' | 'sleeping';

// Dosi levels and their visual upgrades:
// Level 1 (0-6 streak):   plain Dosi
// Level 2 (7-13 days):    Dosi + bandana
// Level 3 (14-29 days):   Dosi + sunglasses
// Level 4 (30-59 days):   Dosi + cape
// Level 5 (60+ days):     Dosi golden/glowing

// States:
// happy:       bouncing animation, smile
// neutral:     idle breathing animation
// sad:         droopy, slow pulse (missed dose today)
// celebrating: spin + scale up (badge/streak milestone)
// sleeping:    gentle sway (all doses taken for today)

const DosiMascot = ({ state, streak, level, size = 'md' }: DosiProps) => {
  const scale = useSharedValue(1);
  const translateY = useSharedValue(0);

  useEffect(() => {
    if (state === 'celebrating') {
      scale.value = withRepeat(withSpring(1.2), 3, true);
    } else if (state === 'happy') {
      translateY.value = withRepeat(withSpring(-8), -1, true);
    }
  }, [state]);

  // On celebrating: trigger canvas-confetti / Haptics.notificationAsync(SUCCESS)

  return (
    <Animated.View style={[animatedStyle]}>
      {/* SVG illustration based on level + state */}
      <DosiSVG level={level} state={state} size={sizeMap[size]} />
      <StreakBadge streak={streak} />
    </Animated.View>
  );
};
```

### Mark as Taken — Dose Confirmation Flow

```tsx
// components/medications/DoseCard.tsx

const DoseCard = ({ medication, onTaken }) => {
  const [loading, setLoading] = useState(false);

  const handleTaken = async () => {
    setLoading(true);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    await logAdherence({ medicationId: medication.id, status: 'TAKEN' });
    triggerConfetti();
    onTaken(medication.id);
    setLoading(false);
  };

  return (
    <Pressable
      className="flex-row items-center p-4 bg-white rounded-2xl mb-3 border border-gray-100"
      style={({ pressed }) => [{ opacity: pressed ? 0.9 : 1 }]}
    >
      <View className={`w-3 h-3 rounded-full mr-3 bg-${medication.color}-500`} />
      <View className="flex-1">
        <Text className="font-medium text-gray-900">{medication.displayName}</Text>
        <Text className="text-sm text-gray-500">{medication.dosage} · {medication.scheduledTime}</Text>
      </View>
      {medication.taken ? (
        <View className="w-9 h-9 rounded-full bg-green-100 items-center justify-center">
          <Check size={18} color="#10b981" />
        </View>
      ) : (
        <Pressable
          onPress={handleTaken}
          className="w-9 h-9 rounded-full bg-indigo-600 items-center justify-center"
          style={{ minWidth: 48, minHeight: 48 }}  // touch target
        >
          {loading ? <ActivityIndicator color="#fff" /> : <Check size={18} color="#fff" />}
        </Pressable>
      )}
    </Pressable>
  );
};
```

### Doctor Dashboard

```tsx
// app/(doctor)/dashboard.tsx

const riskConfig = {
  STABLE:   { color: 'bg-green-100',  text: 'text-green-800',  label: '● Stable',   icon: '🟢' },
  AT_RISK:  { color: 'bg-amber-100',  text: 'text-amber-800',  label: '● At risk',  icon: '🟡' },
  CRITICAL: { color: 'bg-red-100',    text: 'text-red-800',    label: '● Critical', icon: '🔴' },
};

export default function DoctorDashboard() {
  const { data: patients } = useQuery({ queryKey: ['doctor-patients'], queryFn: fetchPatients });
  // Sorted: CRITICAL first, then AT_RISK, then STABLE

  return (
    <FlatList
      data={patients}
      ListHeaderComponent={<DashboardSummary patients={patients} />}
      renderItem={({ item }) => (
        <PatientRiskCard
          patient={item}
          riskConfig={riskConfig[item.riskLevel]}
          onPress={() => router.push(`/doctor/patient/${item.id}`)}
        />
      )}
    />
  );
}
```

---

## Gamification System

```python
# services/gamification.py

BADGES = [
    {"name": "First Step",   "condition": "streak_1",   "xp": 10,   "icon": "🌱"},
    {"name": "One Week",     "condition": "streak_7",   "xp": 50,   "icon": "🔥"},
    {"name": "Two Weeks",    "condition": "streak_14",  "xp": 100,  "icon": "⚡"},
    {"name": "One Month",    "condition": "streak_30",  "xp": 250,  "icon": "🏅"},
    {"name": "Iron Will",    "condition": "streak_60",  "xp": 500,  "icon": "💪"},
    {"name": "Legend",       "condition": "streak_90",  "xp": 1000, "icon": "👑"},
    {"name": "Century",      "condition": "total_100",  "xp": 200,  "icon": "💯"},
    {"name": "Perfect Week", "condition": "perfect_7",  "xp": 75,   "icon": "✨"},
    {"name": "Early Bird",   "condition": "morning_14", "xp": 50,   "icon": "🌅"},
    {"name": "Night Owl",    "condition": "night_14",   "xp": 50,   "icon": "🌙"},
]

XP_REWARDS = {
    "dose_taken_on_time": 10,
    "dose_taken_late":    5,
    "perfect_day":        20,  # all slots taken on time
    "streak_milestone":   "badge_xp",
    "daily_login":        2,
    "chat_with_dosi":     3,
}

DOSI_LEVELS = {
    1: {"min_streak": 0,  "name": "Baby Dosi",   "accessory": None},
    2: {"min_streak": 7,  "name": "Dosi",        "accessory": "bandana"},
    3: {"min_streak": 14, "name": "Cool Dosi",   "accessory": "sunglasses"},
    4: {"min_streak": 30, "name": "Super Dosi",  "accessory": "cape"},
    5: {"min_streak": 60, "name": "Golden Dosi", "accessory": "golden"},
}
```

---

## Privacy Implementation (HIPAA + GDPR)

```python
# middleware/privacy.py

from cryptography.fernet import Fernet

ENCRYPTION_KEY = os.environ["PHI_ENCRYPTION_KEY"]  # AES-256
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_phi(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_phi(encrypted: str) -> str:
    return cipher.decrypt(encrypted.encode()).decode()

# Message builder — NEVER sends PHI over any channel
def build_reminder_message(patient_name: str, time_slot: str, language: str = "en") -> str:
    slot_label = {"MORNING": "morning", "AFTERNOON": "afternoon", "NIGHT": "evening"}[time_slot]
    templates = {
        "en": f"Time for your {slot_label} dose, {patient_name}! 💊",
        "hi": f"{patient_name}, आपकी {slot_label} की दवा का समय हो गया है! 💊",
        "ta": f"{patient_name}, உங்கள் {slot_label} மருந்து நேரம் ஆகிவிட்டது! 💊",
    }
    return templates.get(language, templates["en"])
    # ✅ Never includes drug name, condition, dosage, or diagnosis

# GDPR: right to erasure
async def delete_patient_data(user_id: str):
    await anonymize_adherence_logs(user_id)   # keep aggregate stats, remove PII
    await delete_patient_profile(user_id)
    await delete_medications(user_id)
    await revoke_all_sessions(user_id)
    await audit_log("DATA_DELETION", user_id)
```

---

## Environment Variables

```env
# .env.example

# Supabase
DATABASE_URL=postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres
SUPABASE_URL=https://[ref].supabase.co
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Redis (Upstash)
REDIS_URL=redis://:[password]@[host].upstash.io:6379

# Auth
JWT_SECRET=
JWT_EXPIRE_HOURS=24

# Gemini AI (free tier)
GEMINI_API_KEY=

# Pinecone (free tier)
PINECONE_API_KEY=
PINECONE_INDEX=cara-health-kb

# WhatsApp Cloud API (Meta free tier)
WHATSAPP_PHONE_ID=
WHATSAPP_TOKEN=
WHATSAPP_VERIFY_TOKEN=

# Telegram Bot
TELEGRAM_BOT_TOKEN=

# Exotel IVR
EXOTEL_API_KEY=
EXOTEL_API_TOKEN=
EXOTEL_ACCOUNT_SID=
EXOTEL_FROM_NUMBER=

# MSG91 SMS
MSG91_AUTH_KEY=
MSG91_SENDER_ID=CARA

# Expo Push
EXPO_ACCESS_TOKEN=

# Encryption (HIPAA)
PHI_ENCRYPTION_KEY=          # generate: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# App
APP_BASE_URL=https://cara-health.vercel.app
NODE_ENV=production
```

---

## Step-by-Step Build Order (24hr hackathon)

```
PHASE 1 — Foundation (Hours 1–4)
  ✅ 1. Expo app init (npx create-expo-app cara --template tabs)
  ✅ 2. NativeWind + Tailwind setup
  ✅ 3. FastAPI init + Pydantic schemas + Supabase connection
  ✅ 4. SQLAlchemy models + Alembic migration
  ✅ 5. JWT auth (register / login / 2FA skeleton)
  ✅ 6. Expo Router — patient / caregiver / doctor route groups

PHASE 2 — Core Patient Flow (Hours 5–10)
  ✅ 7. Medication CRUD — API + mobile screens
  ✅ 8. Schedule grouping — Morning / Afternoon / Night
  ✅ 9. AdherenceLog — "Mark as Taken" button + haptics + confetti
  ✅ 10. Streak + XP calculation service
  ✅ 11. Patient dashboard — Dosi widget + schedule cards + adherence ring

PHASE 3 — AI + ML (Hours 11–14)
  ✅ 12. Gemini health coach — /api/ai/chat + weekly insight
  ✅ 13. scikit-learn risk model — pre-train on synthetic data, save .pkl
  ✅ 14. Behavior engine — learned timing from adherence logs
  ✅ 15. AI insight card on dashboard

PHASE 4 — Channels (Hours 15–18)
  ✅ 16. WhatsApp Cloud API — interactive button reminders
  ✅ 17. Telegram bot — /start /taken inline keyboard
  ✅ 18. APScheduler cron — due reminder checker
  ✅ 19. Redis Queue escalation pipeline (WA → IVR → Caregiver → Doctor flag)
  ✅ 20. Exotel IVR voice call (Hindi + English scripts)
  ✅ 21. Expo Push notifications

PHASE 5 — Dashboards + Gamification (Hours 19–21)
  ✅ 22. Badge unlock + XP engine
  ✅ 23. Dosi level-up animation (Reanimated 3)
  ✅ 24. Caregiver dashboard — heatmap + human-readable alerts
  ✅ 25. Doctor dashboard — traffic-light list, sorted by risk

PHASE 6 — Polish + Deploy (Hours 22–24)
  ✅ 26. Seed demo data (Lakshmi=stable, Rajan=at-risk, Priya=critical)
  ✅ 27. PWA manifest + icons
  ✅ 28. RLS policies on Supabase
  ✅ 29. Audit logging middleware
  ✅ 30. Deploy: Vercel (web) + Railway (API) + Supabase (DB) + Upstash (Redis)
```

---

## Demo Seed Data

```python
# scripts/seed.py — run before demo

# Patient 1: Lakshmi (elderly, IVR user, 14-day streak, STABLE 🟢)
# - 4 medications: Morning x2, Afternoon x1, Night x1
# - Preferred channel: IVR, language: Tamil
# - Linked caregiver: Sundar (son), Doctor: Dr. Sharma
# - 30 days adherence history — 92% adherence
# - Badges: First Step, One Week, Two Weeks
# - Dosi: Level 3 (sunglasses)

# Patient 2: Rajan (middle-aged, WhatsApp, AT_RISK 🟡)
# - 3 medications across all slots
# - Preferred channel: WhatsApp
# - Missed 2 evening doses this week
# - Adherence: 71%, streak: 2 days
# - Risk score: 0.55

# Patient 3: Priya (young, app user, CRITICAL 🔴)
# - 5 medications (complex hypertension + diabetes regimen)
# - 5 consecutive misses
# - Adherence: 48%, streak: 0
# - Risk score: 0.89 — doctor already flagged

# Doctor: Dr. Arun Sharma — linked to all 3 patients
# Caregiver: Sundar — linked to Lakshmi and Rajan
```

---

## Demo Presentation Script

```
1. Open app on mobile (or show Vercel web PWA URL)
   → Show Lakshmi's dashboard: Dosi with sunglasses, 14-day streak, golden XP bar

2. Tap "Mark as Taken" on morning dose
   → Phone vibrates, confetti fires, Dosi celebrates, XP increments live

3. Show Dosi AI Coach tab
   → Show Gemini-generated weekly insight: "You're 2 weeks strong, Lakshmi!"
   → Type "why is consistency important?" → Gemini responds warmly

4. Switch to Rajan's account
   → Show AT_RISK badge, 2 missed doses visible on heatmap
   → Show WhatsApp message that was sent (screenshot or live)

5. Show IVR call demo
   → Play recording or live dial: "Hello Lakshmi, press 1 if you've taken your medicine"

6. Switch to Caregiver view (Sundar)
   → "Rajan missed his evening medication for 2 days"
   → Tap "Send encouragement" → WhatsApp message sent

7. Switch to Doctor dashboard (Dr. Sharma)
   → Show 🔴 Priya at top (CRITICAL), 🟡 Rajan second, 🟢 Lakshmi third
   → Click Priya → see detailed miss pattern, risk score 0.89

8. Show badge unlock (trigger from demo)
   → Dosi spins, badge card slides up with XP reward
```

---

*CARA — "We don't just remind patients to take medicine. We help them stay consistent."*
*Stack: Expo RN · FastAPI · Gemini · scikit-learn · Supabase · Redis · WhatsApp · Exotel IVR*