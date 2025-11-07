"""
Simple FastAPI Main Application
Model serving API without MLflow dependency for testing
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

# Use absolute imports instead of relative imports
from src.api.routes import health, models, predictions, monitoring, admin, profitability, churn, revenue_leak, pricing, budget, demand, anomaly
from src.api.middleware.logging import LoggingMiddleware
from src.api.middleware.metrics import MetricsMiddleware
from src.api.middleware.error_handler import ErrorHandlerMiddleware
from src.api.middleware.auth import AuthMiddleware
from src.api.middleware.ratelimit import RateLimitMiddleware
from src.api.simple_dependencies import get_model_registry, get_metrics_collector
from src.utils.logging_config import setup_logging
from config import settings

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting SuperHack AI/ML Model Server (Simple Version)...")
    
    # Initialize model registry
    model_registry = get_model_registry()
    await model_registry.initialize()
    
    # Initialize metrics collector
    metrics_collector = get_metrics_collector()
    await metrics_collector.initialize()
    
    logger.info("Model server startup completed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SuperHack AI/ML Model Server...")
    # Note: SimpleModelRegistry doesn't have cleanup method
    await metrics_collector.cleanup()
    logger.info("Model server shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="SuperHack AI/ML Model Server (Simple)",
    description="AI/ML model serving API for MSP profitability optimization and predictive analytics (Simple Version)",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(models.router, prefix="/api/models", tags=["Models"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(profitability.router, prefix="/api/profitability", tags=["Profitability"])
app.include_router(churn.router, prefix="/api/churn", tags=["Churn"])
app.include_router(revenue_leak.router, prefix="/api/revenue-leak", tags=["Revenue Leak"])
app.include_router(pricing.router, prefix="/api/pricing", tags=["Pricing"])
app.include_router(budget.router, prefix="/api/budget", tags=["Budget"])
app.include_router(demand.router, prefix="/api/demand", tags=["Demand"])
app.include_router(anomaly.router, prefix="/api/anomaly", tags=["Anomaly"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SuperHack AI/ML Model Server (Simple Version)",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.debug else "disabled",
        "endpoints": {
            "health": "/api/health",
            "models": "/api/models",
            "predictions": "/api/predictions",
            "profitability": "/api/profitability",
            "churn": "/api/churn",
            "revenue-leak": "/api/revenue-leak",
            "pricing": "/api/pricing",
            "budget": "/api/budget",
            "demand": "/api/demand",
            "anomaly": "/api/anomaly",
            "monitoring": "/api/monitoring",
            "admin": "/api/admin"
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
            "message": "An unexpected error occurred",
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    return app


if __name__ == "__main__":
    uvicorn.run(
        "src.api.simple_main:app",
        host=settings.model_server.host,
        port=settings.model_server.port,
        reload=settings.model_server.reload,
        workers=1 if settings.model_server.reload else settings.model_server.workers,
        log_level="info"
    )