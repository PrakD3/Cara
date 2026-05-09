from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # DOCTOR, PATIENT, CAREGIVER, ADMIN
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    name = Column(String, nullable=False)
    hospital = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    user = relationship("User", foreign_keys=[user_id])

class CaregiverProfile(Base):
    __tablename__ = "caregiver_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    user = relationship("User", foreign_keys=[user_id])

class PatientProfile(Base):
    __tablename__ = "patient_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    caregiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    preferred_language = Column(String, default="en")
    risk_score = Column(Float, default=0.0)
    user = relationship("User", foreign_keys=[user_id])
    doctor = relationship("User", foreign_keys=[doctor_id])
    caregiver = relationship("User", foreign_keys=[caregiver_id])

class Disease(Base):
    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)

class PatientDisease(Base):
    __tablename__ = "patient_diseases"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    disease_id = Column(Integer, ForeignKey("diseases.id"))

class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)
    refill_cycle_days = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicationImage(Base):
    __tablename__ = "medication_images"
    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"))
    tablet_image_url = Column(String, nullable=True)
    strip_image_url = Column(String, nullable=True)
    bottle_image_url = Column(String, nullable=True)

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"
    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"))
    timing = Column(String)
    frequency = Column(String)

class AdherenceLog(Base):
    __tablename__ = "adherence_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=True)
    schedule_id = Column(Integer, ForeignKey("medication_schedules.id"), nullable=True)
    status = Column(String)  # TAKEN, MISSED, DELAYED, SKIPPED
    source = Column(String)  # APP, IVR, CAREGIVER
    logged_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    body = Column(Text)
    status = Column(String, default="PENDING")  # PENDING, SENT, FAILED
    created_at = Column(DateTime, default=datetime.utcnow)

class VoiceAssistantLog(Base):
    __tablename__ = "voice_assistant_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    transcript = Column(Text)
    response = Column(Text)
    duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class IVRLog(Base):
    __tablename__ = "ivr_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    call_sid = Column(String, nullable=True)
    status = Column(String)
    duration_seconds = Column(Integer, default=0)
    dtmf_input = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Float)
    reasoning = Column(Text, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)

class MascotState(Base):
    __tablename__ = "mascot_states"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    current_mood = Column(String, default="happy")
    streak_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    badge_name = Column(String)
    earned_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)
    entity = Column(String)
    entity_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
