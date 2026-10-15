from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, patients, hospitals, doctors, reports, documents, admin

app = FastAPI(title="MediMate API", description="Backend API for MediMate Healthcare Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "MediMate API is running"}

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(hospitals.router)
app.include_router(doctors.router)
app.include_router(reports.router)
app.include_router(documents.router)
app.include_router(admin.router)
