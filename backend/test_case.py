import pytest
import os

# MUST set DATABASE_URL BEFORE any app imports to prevent Postgres connection
os.environ["DATABASE_URL"] = "sqlite:///./test_cara.db"
os.environ["SECRET_KEY"] = "test_secret_key_long_enough_for_sha256"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.database import Base, get_db
import models.domain  # noqa: registers all models

TEST_DATABASE_URL = "sqlite:///./test_cara.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True, scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ==========================
# TEST 1: Health Check
# ==========================
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Healthy"
    assert "CARA" in data["message"]


# ==========================
# TEST 2: Unauthorized Access
# ==========================
def test_unauthorized_patient_access():
    response = client.get("/api/patients/")
    assert response.status_code == 401


# ==========================
# TEST 3: Doctor Registration
# ==========================
def test_doctor_registration():
    response = client.post("/api/doctors/register", json={
        "name": "Dr. Ramesh Kumar",
        "email": "ramesh@hospital.com",
        "password": "securepass123",
        "hospital": "Apollo Hospital",
        "specialization": "Diabetologist",
        "phone": "9900000001"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dr. Ramesh Kumar"


# ==========================
# TEST 4: Duplicate Doctor Registration
# ==========================
def test_duplicate_doctor_registration():
    client.post("/api/doctors/register", json={
        "name": "Dr. Duplicate",
        "email": "dup@hospital.com",
        "password": "pass123",
        "hospital": "City Hospital",
        "specialization": "GP",
        "phone": "9900000002"
    })
    response = client.post("/api/doctors/register", json={
        "name": "Dr. Duplicate",
        "email": "dup@hospital.com",
        "password": "pass123",
        "hospital": "City Hospital",
        "specialization": "GP",
        "phone": "9900000002"
    })
    assert response.status_code == 400


# ==========================
# TEST 5: Doctor Login
# ==========================
def test_doctor_login():
    client.post("/api/doctors/register", json={
        "name": "Dr. Login Test",
        "email": "logintest@cara.com",
        "password": "testpass123",
        "hospital": "Test Hospital",
        "specialization": "Cardiology",
        "phone": "9900000003"
    })
    response = client.post("/api/auth/login", json={
        "phone": "9900000003",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "DOCTOR"


# ==========================
# TEST 6: Invalid Login
# ==========================
def test_invalid_login():
    response = client.post("/api/auth/login", json={
        "phone": "0000000000",
        "password": "wrongpassword"
    })
    assert response.status_code == 400


# ==========================
# TEST 7: Create Patient (Doctor only)
# ==========================
def test_create_patient():
    client.post("/api/doctors/register", json={
        "name": "Dr. Patient Creator",
        "email": "patientcreator@cara.com",
        "password": "docpass123",
        "hospital": "Cara Hospital",
        "specialization": "Endocrinology",
        "phone": "9900000004"
    })
    login_res = client.post("/api/auth/login", json={
        "phone": "9900000004",
        "password": "docpass123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    response = client.post("/api/patients/", json={
        "name": "Lakshmi Devi",
        "phone": "9800000001",
        "age": 65,
        "gender": "Female",
        "disease": "diabetes",
        "preferred_language": "kn"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "patient_id" in data
    assert "temp_password" in data
    assert len(data["temp_password"]) == 6


# ==========================
# TEST 8: Assign Medication
# ==========================
def test_assign_medication():
    client.post("/api/doctors/register", json={
        "name": "Dr. Med Assign",
        "email": "medassign@cara.com",
        "password": "medpass123",
        "hospital": "Cara Hospital",
        "specialization": "Cardiology",
        "phone": "9900000005"
    })
    login_res = client.post("/api/auth/login", json={
        "phone": "9900000005",
        "password": "medpass123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    patient_res = client.post("/api/patients/", json={
        "name": "Ramu Naik",
        "phone": "9800000002",
        "age": 70,
        "gender": "Male",
        "disease": "hypertension",
        "preferred_language": "hi"
    }, headers={"Authorization": f"Bearer {token}"})
    assert patient_res.status_code == 200
    patient_id = patient_res.json()["patient_id"]

    response = client.post(f"/api/medications/{patient_id}", json={
        "name": "Metformin",
        "dosage": "500mg",
        "instructions": "After meals",
        "disease_id": None,
        "refill_cycle_days": 30,
        "schedules": [
            {"timing": "08:00", "frequency": "DAILY"},
            {"timing": "20:00", "frequency": "DAILY"}
        ]
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200


# ==========================
# TEST 9: IVR Webhook Callback
# ==========================
def test_ivr_dtmf_taken():
    response = client.post(
        "/api/ivr/exotel/callback?patient_id=0",
        data={"CallSid": "ABC123", "digits": "1"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "processing"


def test_ivr_dtmf_remind_later():
    response = client.post(
        "/api/ivr/exotel/callback?patient_id=0",
        data={"CallSid": "ABC124", "digits": "2"}
    )
    assert response.status_code == 200


def test_ivr_dtmf_escalate():
    response = client.post(
        "/api/ivr/exotel/callback?patient_id=0",
        data={"CallSid": "ABC125", "digits": "3"}
    )
    assert response.status_code == 200


# ==========================
# TEST 10: Risk Engine
# ==========================
def test_risk_engine():
    from ml.risk_engine import risk_engine
    score = risk_engine.predict_risk(patient_age=70, missed_doses_7d=6, disease_severity=7)
    assert 0.0 <= score <= 1.0
    print(f"\nRisk Score (elderly, 6 missed doses, severity 7): {score:.2f}")
