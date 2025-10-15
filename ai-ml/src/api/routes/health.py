"""
Health Check Routes
System health monitoring and status endpoints
"""

import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..dependencies import get_model_registry, get_metrics_collector
from ...utils.health_checker import HealthChecker

logger = logging.getLogger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    uptime: float
    services: Dict[str, Any]
    metrics: Dict[str, Any]


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response model"""
    dependencies: Dict[str, Any]
    performance: Dict[str, Any]
    alerts: list


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    try:
        health_checker = HealthChecker()
        health_status = await health_checker.get_basic_health()
        
        return HealthResponse(**health_status)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """Detailed health check with comprehensive system status"""
    try:
        health_checker = HealthChecker()
        detailed_status = await health_checker.get_detailed_health()
        
        return DetailedHealthResponse(**detailed_status)
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    try:
        health_checker = HealthChecker()
        is_ready = await health_checker.is_ready()
        
        if is_ready:
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
            
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    try:
        health_checker = HealthChecker()
        is_alive = await health_checker.is_alive()
        
        if is_alive:
            return {"status": "alive"}
        else:
            raise HTTPException(status_code=503, detail="Service not alive")
            
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not alive")


@router.get("/metrics")
async def health_metrics():
    """Health metrics endpoint"""
    try:
        health_checker = HealthChecker()
        metrics = await health_checker.get_health_metrics()
        
        return metrics
        
    except Exception as e:
        logger.error(f"Health metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get health metrics")
