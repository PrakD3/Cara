# CARA - Contextual Adherence & Recovery Architecture

## Overview
CARA is a production-grade, AI-powered healthcare adherence ecosystem designed specifically for elderly care, diabetes management, and chronic illness monitoring.

## Tech Stack
- **FastAPI** (Python 3.11+)
- **PostgreSQL** + SQLAlchemy + Alembic
- **Redis** + APScheduler
- **WebSockets**
- **AI Integrations**: Groq (Llama 3, Whisper), Wispr
- **Security**: JWT, Passlib, Security Headers

## Folder Structure
```text
backend/
├── api/             # API Routers & Dependencies
├── auth/            # JWT Token generation
├── core/            # Environment configurations
├── ivr/             # Exotel Webhooks & Triggers
├── middleware/      # HIPAA/GDPR Security Headers & Audit Logging
├── ml/              # Scikit-learn Risk Engines
├── models/          # SQLAlchemy Domain Models
├── notifications/   # WhatsApp & Push Notifications
├── schemas/         # Pydantic v2 validation
├── scheduler/       # Background tasks for missed doses
├── services/        # Decoupled Business Logic
├── websocket/       # Real-time dashboard updates
└── tests/           # Pytest suite
```

## Running the Application

### 1. Docker
```bash
docker-compose up --build
```

### 2. Manual Execution
```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
