from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class LoginRequest(BaseModel):
    phone: str
    password: str

# --- Doctor ---
class DoctorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    hospital: str
    specialization: str
    phone: str
    organization_id: Optional[int] = None

class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    hospital: str
    specialization: str

# --- Patient ---
class PatientCreate(BaseModel):
    name: str
    phone: str
    age: int
    gender: str
    disease: str
    preferred_language: str = "en"
    caregiver_phone: Optional[str] = None

class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    age: int
    gender: str

# --- Medication ---
class MedicationScheduleCreate(BaseModel):
    timing: str
    frequency: str

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    instructions: str
    disease_id: Optional[int] = None
    refill_cycle_days: int = 30
    schedules: List[MedicationScheduleCreate]

class AdherenceLogCreate(BaseModel):
    medication_id: Optional[int] = None
    schedule_id: Optional[int] = None
    status: str
    source: str

# --- Adherence ---
class AdherenceLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    status: str
    source: str
