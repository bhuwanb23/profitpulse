"""
Admin Routes
Administrative functions, A/B testing, and system management endpoints
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from ..dependencies import get_model_registry, get_metrics_collector
from ...utils.admin import AdminService

logger = logging.getLogger(__name__)
router = APIRouter()


class ABTestConfig(BaseModel):
    """A/B test configuration"""
    test_name: str
    model_a: str
    model_b: str
    traffic_split: float = Field(0.5, ge=0.0, le=1.0, description="Traffic split ratio")
    success_metric: str = "accuracy"
    minimum_sample_size: int = 1000
    max_duration_days: int = 30
    enabled: bool = True


class ABTestResult(BaseModel):
    """A/B test result"""
    test_id: str
    test_name: str
    status: str
    model_a_performance: Dict[str, float]
    model_b_performance: Dict[str, float]
    statistical_significance: float
    winner: Optional[str] = None
    confidence_level: float
    sample_size: int
    created_at: datetime
    ended_at: Optional[datetime] = None


class SystemConfig(BaseModel):
    """System configuration"""
    max_concurrent_predictions: int = 100
    prediction_timeout_seconds: int = 30
    model_cache_size: int = 10
    auto_retrain_enabled: bool = True
    retrain_threshold: float = 0.05
    monitoring_enabled: bool = True
    alerting_enabled: bool = True


class ModelRetrainJob(BaseModel):
    """Model retraining job"""
    job_id: str
    model_name: str
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    error_message: Optional[str] = None


@router.get("/system/config", response_model=SystemConfig)
async def get_system_config():
    """Get current system configuration"""
    try:
        admin_service = AdminService()
        config = await admin_service.get_system_config()
        
        return SystemConfig(**config)
        
    except Exception as e:
        logger.error(f"Failed to get system config: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system configuration")


@router.put("/system/config", response_model=Dict[str, str])
async def update_system_config(config: SystemConfig):
    """Update system configuration"""
    try:
        admin_service = AdminService()
        success = await admin_service.update_system_config(config.dict())
        
        if not success:
            raise HTTPException(status_code=400, detail="Invalid configuration")
        
        return {"message": "System configuration updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update system config: {e}")
        raise HTTPException(status_code=500, detail="Failed to update system configuration")


@router.get("/ab-tests", response_model=List[ABTestResult])
async def list_ab_tests(
    status: Optional[str] = Query(None, description="Filter by test status"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of tests to return")
):
    """List A/B tests"""
    try:
        admin_service = AdminService()
        tests = await admin_service.list_ab_tests(status=status, limit=limit)
        
        return tests
        
    except Exception as e:
        logger.error(f"Failed to list A/B tests: {e}")
        raise HTTPException(status_code=500, detail="Failed to list A/B tests")


@router.post("/ab-tests", response_model=Dict[str, str])
async def create_ab_test(test_config: ABTestConfig):
    """Create a new A/B test"""
    try:
        admin_service = AdminService()
        test_id = await admin_service.create_ab_test(test_config.dict())
        
        return {"message": "A/B test created successfully", "test_id": test_id}
        
    except Exception as e:
        logger.error(f"Failed to create A/B test: {e}")
        raise HTTPException(status_code=500, detail="Failed to create A/B test")


@router.get("/ab-tests/{test_id}", response_model=ABTestResult)
async def get_ab_test(
    test_id: str = Path(..., description="ID of the A/B test")
):
    """Get A/B test details"""
    try:
        admin_service = AdminService()
        test_result = await admin_service.get_ab_test(test_id)
        
        if not test_result:
            raise HTTPException(status_code=404, detail="A/B test not found")
        
        return test_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get A/B test {test_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get A/B test")


@router.post("/ab-tests/{test_id}/stop")
async def stop_ab_test(
    test_id: str = Path(..., description="ID of the A/B test")
):
    """Stop an A/B test"""
    try:
        admin_service = AdminService()
        success = await admin_service.stop_ab_test(test_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="A/B test not found")
        
        return {"message": "A/B test stopped successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stop A/B test {test_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop A/B test")


@router.get("/retrain/jobs", response_model=List[ModelRetrainJob])
async def list_retrain_jobs(
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    status: Optional[str] = Query(None, description="Filter by job status"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of jobs to return")
):
    """List model retraining jobs"""
    try:
        admin_service = AdminService()
        jobs = await admin_service.list_retrain_jobs(
            model_name=model_name,
            status=status,
            limit=limit
        )
        
        return jobs
        
    except Exception as e:
        logger.error(f"Failed to list retrain jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to list retrain jobs")


@router.get("/retrain/jobs/{job_id}", response_model=ModelRetrainJob)
async def get_retrain_job(
    job_id: str = Path(..., description="ID of the retrain job")
):
    """Get retraining job details"""
    try:
        admin_service = AdminService()
        job = await admin_service.get_retrain_job(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Retrain job not found")
        
        return job
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get retrain job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get retrain job")


@router.post("/retrain/jobs/{job_id}/cancel")
async def cancel_retrain_job(
    job_id: str = Path(..., description="ID of the retrain job")
):
    """Cancel a retraining job"""
    try:
        admin_service = AdminService()
        success = await admin_service.cancel_retrain_job(job_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Retrain job not found")
        
        return {"message": "Retrain job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel retrain job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to cancel retrain job")


@router.get("/models/{model_name}/versions/{version}/explain")
async def explain_model_prediction(
    model_name: str = Path(..., description="Name of the model"),
    version: str = Path(..., description="Version of the model"),
    prediction_id: str = Query(..., description="ID of the prediction to explain")
):
    """Get model prediction explanation"""
    try:
        admin_service = AdminService()
        explanation = await admin_service.explain_prediction(
            model_name=model_name,
            version=version,
            prediction_id=prediction_id
        )
        
        if not explanation:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        return explanation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to explain prediction {prediction_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to explain prediction")


@router.get("/system/status")
async def get_system_status():
    """Get overall system status"""
    try:
        admin_service = AdminService()
        status = await admin_service.get_system_status()
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system status")


@router.post("/system/maintenance")
async def start_maintenance_mode(
    duration_minutes: int = Query(60, ge=1, le=1440, description="Maintenance duration in minutes")
):
    """Start system maintenance mode"""
    try:
        admin_service = AdminService()
        success = await admin_service.start_maintenance_mode(duration_minutes)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to start maintenance mode")
        
        return {"message": f"Maintenance mode started for {duration_minutes} minutes"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start maintenance mode: {e}")
        raise HTTPException(status_code=500, detail="Failed to start maintenance mode")


@router.delete("/system/maintenance")
async def stop_maintenance_mode():
    """Stop system maintenance mode"""
    try:
        admin_service = AdminService()
        success = await admin_service.stop_maintenance_mode()
        
        if not success:
            raise HTTPException(status_code=400, detail="Maintenance mode not active")
        
        return {"message": "Maintenance mode stopped"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stop maintenance mode: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop maintenance mode")
