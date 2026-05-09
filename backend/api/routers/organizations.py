from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.domain import User, DoctorProfile, PatientProfile, Organization
from api.deps import get_current_user
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger("cara.organizations")


class OrganizationCreate(BaseModel):
    name: str
    address: str = ""


@router.post("/")
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new organization. Admin only."""
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can create organizations")

    existing = db.query(Organization).filter(Organization.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    org = Organization(name=data.name, address=data.address)
    db.add(org)
    db.commit()
    db.refresh(org)
    return {"id": org.id, "name": org.name}


@router.get("/")
def list_organizations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Lists all organizations."""
    orgs = db.query(Organization).all()
    return [{"id": o.id, "name": o.name, "address": o.address} for o in orgs]


@router.get("/{org_id}/doctors")
def get_org_doctors(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns all doctors under an organization."""
    doctors = db.query(DoctorProfile).filter(DoctorProfile.organization_id == org_id).all()
    return [
        {
            "doctor_id": d.user_id,
            "name": d.name,
            "hospital": d.hospital,
            "specialization": d.specialization,
        }
        for d in doctors
    ]


@router.get("/{org_id}/stats")
def get_org_stats(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns high-level adherence and patient stats for an organization."""
    doctors = db.query(DoctorProfile).filter(DoctorProfile.organization_id == org_id).all()
    doctor_ids = [d.user_id for d in doctors]

    patient_count = db.query(PatientProfile).filter(
        PatientProfile.doctor_id.in_(doctor_ids)
    ).count()

    high_risk_count = db.query(PatientProfile).filter(
        PatientProfile.doctor_id.in_(doctor_ids),
        PatientProfile.risk_score > 0.7
    ).count()

    return {
        "org_id": org_id,
        "total_doctors": len(doctors),
        "total_patients": patient_count,
        "high_risk_patients": high_risk_count,
    }
