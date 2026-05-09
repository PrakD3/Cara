"""
CARA Database Seeder
Run this after migrations to populate essential reference data.
Usage: python seed.py
"""
import os
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://cara:cara_password@localhost/cara_db")

from models.database import SessionLocal, Base, engine
import models.domain   # noqa
import models.mascot   # noqa
from services.mascot_seed_service import seed_mascot_system
from models.domain import User, Disease, Organization
from auth.jwt import get_password_hash
from datetime import datetime


def seed_diseases(db):
    diseases = [
        {"name": "Type 2 Diabetes", "description": "Chronic condition affecting blood sugar regulation"},
        {"name": "Hypertension", "description": "High blood pressure management"},
        {"name": "Heart Disease", "description": "Cardiac health management"},
        {"name": "Hypothyroidism", "description": "Thyroid hormone deficiency"},
        {"name": "COPD", "description": "Chronic obstructive pulmonary disease"},
        {"name": "Arthritis", "description": "Joint inflammation management"},
        {"name": "Osteoporosis", "description": "Bone density loss management"},
    ]
    for d in diseases:
        if not db.query(Disease).filter(Disease.name == d["name"]).first():
            db.add(Disease(**d))
    db.commit()
    print(f"✓ Seeded {len(diseases)} diseases")


def seed_default_admin(db):
    if not db.query(User).filter(User.phone == "0000000000").first():
        admin = User(
            phone="0000000000",
            email="admin@cara.health",
            hashed_password=get_password_hash("admin@CARA2024!"),
            role="ADMIN",
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(admin)
        db.commit()
        print("✓ Default admin created: phone=0000000000 / password=admin@CARA2024!")
    else:
        print("✓ Admin already exists")


def seed_default_organization(db):
    if not db.query(Organization).filter(Organization.name == "CARA Health Network").first():
        org = Organization(name="CARA Health Network", address="Bangalore, India")
        db.add(org)
        db.commit()
        print("✓ Seeded default organization")


if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Seeding mascot system...")
        seed_mascot_system(db)

        print("Seeding diseases...")
        seed_diseases(db)

        print("Seeding admin user...")
        seed_default_admin(db)

        print("Seeding organization...")
        seed_default_organization(db)

        print("\n✅ Database seed complete. CARA is ready.")
    finally:
        db.close()
