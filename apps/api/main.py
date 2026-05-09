from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, patients, medications, adherence, ai_coach, notifications, webhooks

app = FastAPI(
    title="CARA API",
    description="Contextual Adherence & Recovery Architecture API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(medications.router, prefix="/api/medications", tags=["Medications"])
app.include_router(adherence.router, prefix="/api/adherence", tags=["Adherence"])
app.include_router(ai_coach.router, prefix="/api/ai", tags=["AI Coach"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])

@app.get("/")
async def root():
    return {"message": "Welcome to CARA API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
