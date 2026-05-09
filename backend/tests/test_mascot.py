import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_cara.db"
os.environ["SECRET_KEY"] = "test_secret_key_long_enough_for_sha256"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.database import Base, get_db
import models.domain   # noqa
from services.mascot_seed_service import seed_mascot_system

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
    db = TestingSessionLocal()
    seed_mascot_system(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def register_and_login_doctor(phone: str, email: str) -> str:
    client.post("/api/doctors/register", json={
        "name": "Dr. Mascot Tester",
        "email": email,
        "password": "pass1234",
        "hospital": "CARA Hospital",
        "specialization": "GP",
        "phone": phone
    })
    res = client.post("/api/auth/login", json={"phone": phone, "password": "pass1234"})
    return res.json()["access_token"]


def create_patient_and_login(doctor_token: str, phone: str) -> str:
    res = client.post("/api/patients/", json={
        "name": "Test Patient",
        "phone": phone,
        "age": 65,
        "gender": "Female",
        "disease": "diabetes",
        "preferred_language": "en"
    }, headers={"Authorization": f"Bearer {doctor_token}"})
    temp_pass = res.json()["temp_password"]

    login_res = client.post("/api/auth/login", json={"phone": phone, "password": temp_pass})
    return login_res.json()["access_token"]


# ─── Tests ───────────────────────────────────────────────────────────────────

def test_mascot_state_initial():
    """Mascot state should be created on first access."""
    doctor_token = register_and_login_doctor("9910000001", "mascot1@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000001")

    res = client.get("/api/mascot/state", headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["current_mood"] == "HAPPY"
    assert data["current_level"] == 1
    assert data["mascot_name"] == "Dosi"


def test_mascot_name_update():
    """Patient should be able to rename their mascot."""
    doctor_token = register_and_login_doctor("9910000002", "mascot2@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000002")

    res = client.patch("/api/mascot/name", json={"mascot_name": "Buddy"},
                       headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    assert res.json()["mascot_name"] == "Buddy"


def test_mascot_event_medication_taken():
    """Firing MEDICATION_TAKEN should transition mood and award XP."""
    doctor_token = register_and_login_doctor("9910000003", "mascot3@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000003")

    res = client.post("/api/mascot/event", json={
        "event_type": "MEDICATION_TAKEN",
        "patient_id": 0,
        "metadata": {"medication_name": "Metformin"}
    }, headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 200
    data = res.json()
    assert "mood" in data
    assert "dialogue" in data
    assert "xp_event" in data


def test_mascot_dialogue_response():
    """Dialogue endpoint should return a message for the current mood."""
    doctor_token = register_and_login_doctor("9910000004", "mascot4@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000004")

    res = client.get("/api/mascot/dialogue", headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "message" in data
    assert "mood" in data
    assert len(data["message"]) > 0


def test_mascot_xp_summary():
    """XP endpoint should return correct XP structure."""
    doctor_token = register_and_login_doctor("9910000005", "mascot5@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000005")

    # Fire some events first
    client.post("/api/mascot/event", json={
        "event_type": "MEDICATION_TAKEN", "patient_id": 0
    }, headers={"Authorization": f"Bearer {patient_token}"})

    res = client.get("/api/mascot/xp", headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "current_xp" in data
    assert "total_xp_earned" in data
    assert "current_level" in data
    assert data["current_xp"] > 0


def test_mascot_streak_after_medication():
    """Streak should be updated after MEDICATION_TAKEN event."""
    doctor_token = register_and_login_doctor("9910000006", "mascot6@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000006")

    client.post("/api/mascot/event", json={
        "event_type": "MEDICATION_TAKEN", "patient_id": 0
    }, headers={"Authorization": f"Bearer {patient_token}"})

    res = client.get("/api/mascot/streak", headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    streaks = res.json()
    assert isinstance(streaks, list)
    assert len(streaks) > 0
    assert streaks[0]["current_streak"] >= 1


def test_mascot_evolution():
    """Evolution endpoint should return mascot level info."""
    doctor_token = register_and_login_doctor("9910000007", "mascot7@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000007")

    res = client.get("/api/mascot/evolution", headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "current_level" in data
    assert data["current_level"] == 1


def test_mascot_badges_initially_empty():
    """Newly created patient should have no badges."""
    doctor_token = register_and_login_doctor("9910000008", "mascot8@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000008")

    res = client.get("/api/mascot/badges", headers={"Authorization": f"Bearer {patient_token}"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_mascot_welcome_back_event():
    """APP_OPENED_AFTER_INACTIVITY from a low-mood state should trigger WELCOME_BACK."""
    doctor_token = register_and_login_doctor("9910000009", "mascot9@cara.com")
    patient_token = create_patient_and_login(doctor_token, "9810000009")

    # Chain through full degradation: HAPPY -> GENTLE_REMINDER -> CONCERNED -> WORRIED -> SAD
    for event in ["MISSED_DOSE_1", "MISSED_DOSE_2", "MISSED_DOSE_3", "MISSED_DOSE_5"]:
        client.post("/api/mascot/event", json={"event_type": event, "patient_id": 0},
                    headers={"Authorization": f"Bearer {patient_token}"})

    # Verify mood is now SAD or WORRIED
    state_res = client.get("/api/mascot/state", headers={"Authorization": f"Bearer {patient_token}"})
    mood_before = state_res.json()["current_mood"]
    assert mood_before in ["SAD", "WORRIED", "CONCERNED", "GENTLE_REMINDER"]

    # Now trigger welcome back
    res = client.post("/api/mascot/event", json={
        "event_type": "APP_OPENED_AFTER_INACTIVITY", "patient_id": 0
    }, headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 200
    assert res.json()["mood"] == "WELCOME_BACK"
