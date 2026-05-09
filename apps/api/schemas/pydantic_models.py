from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from ..models.database import UserRole, ReminderChannel, AdherenceStatus, RiskLevel, TimeSlot

class UserBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.PATIENT
    preferred_channel: ReminderChannel = ReminderChannel.WHATSAPP
    preferred_language: str = "en"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PatientProfileResponse(BaseModel):
    id: str
    user_id: str
    current_streak: int
    total_xp: int
    dosi_level: int
    risk_level: RiskLevel
    risk_score: float

    class Config:
        from_attributes = True

class MedicationBase(BaseModel):
    name: str
    dosage: str
    unit: str = "mg"
    color: str = "indigo"
    start_date: datetime
    end_date: Optional[datetime] = None

class MedicationCreate(MedicationBase):
    instructions: Optional[str] = None

class MedicationResponse(MedicationBase):
    id: str
    patient_id: str
    is_active: bool

    class Config:
        from_attributes = True

class AdherenceLogCreate(BaseModel):
    medication_id: str
    status: AdherenceStatus
    note: Optional[str] = None

class DashboardResponse(BaseModel):
    streak: int
    total_xp: int
    dosi_level: int
    dosi_state: str
    today_schedule: List[dict]
    weekly_insight: str
