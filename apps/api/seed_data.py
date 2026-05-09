import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models.database import Base, User, PatientProfile, Medication, RiskLevel, UserRole

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    db = SessionLocal()
    try:
        # Create a sample user
        user = User(
            id="user_123",
            name="John Doe",
            phone="+1234567890",
            email="john@example.com",
            role=UserRole.PATIENT
        )
        
        # Create a sample patient profile
        profile = PatientProfile(
            id="patient_123",
            user_id="user_123",
            current_streak=15,
            longest_streak=22,
            total_xp=1250,
            dosi_level=4,
            risk_level=RiskLevel.STABLE,
            risk_score=0.1
        )
        
        # Create some sample medications
        meds = [
            Medication(
                id="med_1",
                patient_id="patient_123",
                name_encrypted="Atorvastatin", # In real app, this would be encrypted
                dosage="20mg",
                unit="mg",
                color="#4F46E5", # Indigo
                is_active=True
            ),
            Medication(
                id="med_2",
                patient_id="patient_123",
                name_encrypted="Lisinopril",
                dosage="10mg",
                unit="mg",
                color="#7C3AED", # Violet
                is_active=True
            )
        ]
        
        db.add(user)
        db.add(profile)
        for m in meds:
            db.add(m)
            
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
