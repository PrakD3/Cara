from sqlalchemy.orm import Session
from models.domain import User, DoctorProfile, Organization
from schemas.domain_schemas import DoctorCreate
from auth.jwt import get_password_hash
from fastapi import HTTPException

def register_doctor_service(db: Session, data: DoctorCreate):
    # Check if doctor exists
    existing = db.query(User).filter((User.phone == data.phone) | (User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone or email already registered")
        
    # Create User Base
    user = User(
        phone=data.phone,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role="DOCTOR"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create Profile
    profile = DoctorProfile(
        user_id=user.id,
        organization_id=data.organization_id,
        name=data.name,
        hospital=data.hospital,
        specialization=data.specialization
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return profile
