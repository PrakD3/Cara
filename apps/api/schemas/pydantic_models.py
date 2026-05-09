from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from models.database import UserRole, ReminderChannel, AdherenceStatus, RiskLevel, TimeSlot

class UserBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.PATIENT
    preferred_channel: ReminderChannel = ReminderChannel.WHATSAPP
    preferred_language: str = "en"

class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PatientProfile(BaseModel):
    id: str
    user_id: str
    user: Optional[UserResponse] = None
    current_streak: int
    total_xp: int
    dosi_level: int
    risk_level: RiskLevel
    risk_score: float

    class Config:
        from_attributes = True

class MedicationBase(BaseModel):
    name_encrypted: str # Align with DB column name
    dosage: str
    unit: str = "mg"
    color: str = "indigo"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Medication(MedicationBase):
    id: str
    patient_id: str
    is_active: bool

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    streak: int
    total_xp: int
    dosi_level: int
    dosi_state: str
    today_schedule: List[dict]
    weekly_insight: str
