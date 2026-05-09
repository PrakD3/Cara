import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from models.database import get_db, PatientProfile, Medication, RiskLevel
from unittest.mock import MagicMock

# Create a mock database session
def override_get_db():
    mock_db = MagicMock()
    
    # Mocking the .first() call for get_current_patient_profile
    mock_patient = MagicMock()
    mock_patient.id = "test-patient-id"
    mock_patient.user_id = "test-user-id"
    mock_patient.current_streak = 5
    mock_patient.total_xp = 1200
    mock_patient.dosi_level = 2
    mock_patient.risk_level = RiskLevel.STABLE
    mock_patient.risk_score = 0.0
    mock_patient.user = None # Optional in schema
    
    # Set up the mock behavior for .query(...).first()
    mock_db.query.return_value.first.return_value = mock_patient
    
    # Mocking the .all() call for get_patient_medications
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    try:
        yield mock_db
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CARA API"}

@pytest.mark.asyncio
async def test_get_patient_me():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/patients/me")
    # Should be 200 now with our fixed mock
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-patient-id"
    assert data["current_streak"] == 5

@pytest.mark.asyncio
async def test_get_medications_empty():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/medications/patient/123")
    assert response.status_code == 200
    assert response.json() == []
