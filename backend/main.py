from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, patients, doctors, medications, mascot, caregivers, organizations, preventive
from ivr.webhooks import router as ivr_router
import models.domain   # noqa: register all domain models

app = FastAPI(
    title="CARA API",
    version="1.0.0",
    description="Contextual Adherence & Recovery Architecture — DOSI Mascot Intelligence Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Core Routes ─────────────────────────────────────────────────────────────
app.include_router(auth.router,           prefix="/api/auth",          tags=["Auth"])
app.include_router(doctors.router,        prefix="/api/doctors",        tags=["Doctors"])
app.include_router(patients.router,       prefix="/api/patients",       tags=["Patients"])
app.include_router(caregivers.router,     prefix="/api/caregivers",     tags=["Caregivers"])
app.include_router(medications.router,    prefix="/api/medications",    tags=["Medications"])
app.include_router(organizations.router,  prefix="/api/organizations",  tags=["Organizations"])
app.include_router(preventive.router,     prefix="/api/preventive",     tags=["Preventive Care"])

# ─── IVR ────────────────────────────────────────────────────────────────────
app.include_router(ivr_router,            prefix="/api/ivr",            tags=["IVR Webhooks"])

# ─── DOSI Mascot Engine ──────────────────────────────────────────────────────
app.include_router(mascot.router,         prefix="/api/mascot",         tags=["DOSI Mascot"])


@app.get("/")
async def root():
    return {
        "message": "CARA Production API is running.",
        "status": "Healthy",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
