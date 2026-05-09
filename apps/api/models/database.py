import os
import enum
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, JSON, Enum, ARRAY, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
load_dotenv()

# Use SQLite for bulletproof local development
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cara.db")

# Create engine - SQLite doesn't support the same pooling as Postgres
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.PATIENT)
    preferred_channel = Column(Enum(ReminderChannel), default=ReminderChannel.WHATSAPP)
    preferred_language = Column(String, default="en")
    whatsapp_number = Column(String)
    telegram_chat_id = Column(String, unique=True)
    expo_push_token = Column(String)
    totp_secret = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class PatientProfile(Base):
    __tablename__ = "patient_profiles"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    date_of_birth = Column(DateTime)
    conditions = Column(ARRAY(String))
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    dosi_level = Column(Integer, default=1)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.STABLE)
    risk_score = Column(Float, default=0.0)
    last_dose_at = Column(DateTime)
    learned_morning_time = Column(String)
    learned_afternoon_time = Column(String)
    user = relationship("User", backref="profile")
    learned_night_time = Column(String)

class Medication(Base):
    __tablename__ = "medications"
    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient_profiles.id"))
    name_encrypted = Column(String)
    dosage = Column(String)
    unit = Column(String, default="mg")
    instructions_encrypted = Column(String)
    color = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"
    id = Column(String, primary_key=True)
    medication_id = Column(String, ForeignKey("medications.id"))
    time_slot = Column(Enum(TimeSlot))
    scheduled_time = Column(String)
    days_of_week = Column(ARRAY(Integer))
    is_active = Column(Boolean, default=True)

class AdherenceLog(Base):
    __tablename__ = "adherence_logs"
    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient_profiles.id"))
    medication_id = Column(String, ForeignKey("medications.id"))
    scheduled_at = Column(DateTime)
    responded_at = Column(DateTime)
    status = Column(Enum(AdherenceStatus))
    channel = Column(Enum(ReminderChannel))
    escalation_stage = Column(Integer, default=1)
    note = Column(String)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    actor_id = Column(String)
    action = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(JSON)
