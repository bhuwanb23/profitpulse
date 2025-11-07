"""
Minimal FastAPI Main Application
Simple model serving API without complex dependencies for testing
"""

import logging
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Simple health check endpoint without complex dependencies
from fastapi import APIRouter

# Create a simple router for health check
health_router = APIRouter()

@health_router.get("/")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "AI/ML service is running"}

@health_router.get("/api/health")
async def api_health_check():
    """API health check endpoint"""
    return {"status": "healthy", "service": "AI/ML Model Server"}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Minimal SuperHack AI/ML Model Server...")
    yield
    # Shutdown
    logger.info("Shutting down Minimal SuperHack AI/ML Model Server...")

# Create FastAPI application
app = FastAPI(
    title="Minimal SuperHack AI/ML Model Server",
    description="Minimal AI/ML model serving API for testing",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Include routers
app.include_router(health_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Minimal SuperHack AI/ML Model Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "src.api.minimal_main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        workers=1,
        log_level="info"
    )