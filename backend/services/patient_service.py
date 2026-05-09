from sqlalchemy.orm import Session
from models.domain import User, PatientProfile, Disease, PatientDisease
from schemas.domain_schemas import PatientCreate
from auth.jwt import get_password_hash
import random
import string

def create_patient_profile(db: Session, data: PatientCreate, doctor_id: int):
    # 1. Generate 6-digit temp password
    temp_pass = ''.join(random.choices(string.digits, k=6))
    
    # 2. Create base User
    user = User(
        phone=data.phone,
        hashed_password=get_password_hash(temp_pass),
        role="PATIENT"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 3. Handle Disease linkage dynamically
    disease = db.query(Disease).filter(Disease.name.ilike(data.disease)).first()
    if not disease:
        disease = Disease(name=data.disease.lower())
        db.add(disease)
        db.commit()
        db.refresh(disease)
        
    patient_disease = PatientDisease(patient_id=user.id, disease_id=disease.id)
    db.add(patient_disease)
    
    # 4. Caregiver Resolution (Optional)
    caregiver_id = None
    if data.caregiver_phone:
        cg = db.query(User).filter(User.phone == data.caregiver_phone).first()
        if cg:
            caregiver_id = cg.id
            
    # 5. Create Patient Profile
    profile = PatientProfile(
        user_id=user.id,
        doctor_id=doctor_id,
        caregiver_id=caregiver_id,
        name=data.name,
        age=data.age,
        gender=data.gender,
        preferred_language=data.preferred_language
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    # Returning temp_pass allows the router to trigger the SMS Notification
    return profile, temp_pass

def get_patients_for_doctor(db: Session, doctor_id: int):
    return db.query(PatientProfile).filter(PatientProfile.doctor_id == doctor_id).all()
