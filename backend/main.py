from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes.generate import router as generate_router
from routes.upload import router as upload_router


app = FastAPI(
    title="PDD to SDD Generator",
    description="AI-powered solution design document generator",
    version="1.0.0",
)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")  # Replace with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Allow requests from the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "PDD to SDD Generator Backend is running."}


@app.get("/health")
def health_check():
    from services.ollama_service import check_connection

    return {
        "backend": "running",
        "ollama": "connected" if check_connection() else "disconnected",
    }


app.include_router(upload_router, prefix="/api", tags=["PDD Upload"])
app.include_router(generate_router, prefix="/api", tags=["SDD Generation"])
