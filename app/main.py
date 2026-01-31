"""Main FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Model Autopsy AI",
    description="Automated Root Cause Analysis for ML Model Failure",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "status": "Model Autopsy AI is running",
        "version": "1.0.0",
        "message": "Upload your data to /run-autopsy endpoint"
    }

@app.get("/health")
def detailed_health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Model Autopsy AI",
        "endpoints": {
            "docs": "/docs",
            "autopsy": "/run-autopsy"
        }
    }
