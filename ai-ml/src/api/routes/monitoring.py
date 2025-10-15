"""
Monitoring Routes
Model performance monitoring, metrics, and alerting endpoints
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from ..dependencies import get_metrics_collector, get_model_registry
from ...utils.monitoring import MonitoringService

logger = logging.getLogger(__name__)
router = APIRouter()


class MetricsResponse(BaseModel):
    """Metrics response model"""
    timestamp: datetime
    metrics: Dict[str, Any]
    model_metrics: Dict[str, Dict[str, Any]]


class AlertRule(BaseModel):
    """Alert rule configuration"""
    name: str
    model_name: str
    metric: str
    threshold: float
    operator: str  # "gt", "lt", "eq", "gte", "lte"
    severity: str  # "low", "medium", "high", "critical"
    enabled: bool = True


class Alert(BaseModel):
    """Alert information"""
    id: str
    rule_name: str
    model_name: str
    metric: str
    current_value: float
    threshold: float
    severity: str
    status: str  # "active", "resolved", "acknowledged"
    created_at: datetime
    resolved_at: Optional[datetime] = None
    message: str


class PerformanceMetrics(BaseModel):
    """Model performance metrics"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    auc_roc: float
    prediction_latency_ms: float
    throughput_per_second: float
    error_rate: float
    timestamp: datetime


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    time_range: str = Query("1h", description="Time range for metrics (1h, 24h, 7d, 30d)"),
    model_name: Optional[str] = Query(None, description="Filter by specific model")
):
    """Get system and model metrics"""
    try:
        monitoring_service = MonitoringService()
        metrics = await monitoring_service.get_metrics(
            time_range=time_range,
            model_name=model_name
        )
        
        return MetricsResponse(**metrics)
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get metrics")


@router.get("/performance", response_model=List[PerformanceMetrics])
async def get_performance_metrics(
    model_name: Optional[str] = Query(None, description="Filter by specific model"),
    days: int = Query(7, ge=1, le=365, description="Number of days to look back"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """Get model performance metrics"""
    try:
        monitoring_service = MonitoringService()
        performance = await monitoring_service.get_performance_metrics(
            model_name=model_name,
            days=days,
            limit=limit
        )
        
        return performance
        
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")


@router.get("/alerts", response_model=List[Alert])
async def get_alerts(
    status: Optional[str] = Query(None, description="Filter by alert status"),
    severity: Optional[str] = Query(None, description="Filter by alert severity"),
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of alerts to return")
):
    """Get active and recent alerts"""
    try:
        monitoring_service = MonitoringService()
        alerts = await monitoring_service.get_alerts(
            status=status,
            severity=severity,
            model_name=model_name,
            limit=limit
        )
        
        return alerts
        
    except Exception as e:
        logger.error(f"Failed to get alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alerts")


@router.post("/alerts/rules", response_model=Dict[str, str])
async def create_alert_rule(rule: AlertRule):
    """Create a new alert rule"""
    try:
        monitoring_service = MonitoringService()
        rule_id = await monitoring_service.create_alert_rule(rule.dict())
        
        return {"message": "Alert rule created successfully", "rule_id": rule_id}
        
    except Exception as e:
        logger.error(f"Failed to create alert rule: {e}")
        raise HTTPException(status_code=500, detail="Failed to create alert rule")


@router.get("/alerts/rules", response_model=List[AlertRule])
async def get_alert_rules(
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    enabled_only: bool = Query(True, description="Show only enabled rules")
):
    """Get alert rules"""
    try:
        monitoring_service = MonitoringService()
        rules = await monitoring_service.get_alert_rules(
            model_name=model_name,
            enabled_only=enabled_only
        )
        
        return rules
        
    except Exception as e:
        logger.error(f"Failed to get alert rules: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alert rules")


@router.put("/alerts/rules/{rule_id}")
async def update_alert_rule(
    rule_id: str = Path(..., description="ID of the alert rule"),
    rule: AlertRule = None
):
    """Update an alert rule"""
    try:
        monitoring_service = MonitoringService()
        success = await monitoring_service.update_alert_rule(rule_id, rule.dict())
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {"message": "Alert rule updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update alert rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update alert rule")


@router.delete("/alerts/rules/{rule_id}")
async def delete_alert_rule(
    rule_id: str = Path(..., description="ID of the alert rule")
):
    """Delete an alert rule"""
    try:
        monitoring_service = MonitoringService()
        success = await monitoring_service.delete_alert_rule(rule_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {"message": "Alert rule deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete alert rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete alert rule")


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str = Path(..., description="ID of the alert")
):
    """Acknowledge an alert"""
    try:
        monitoring_service = MonitoringService()
        success = await monitoring_service.acknowledge_alert(alert_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert acknowledged successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to acknowledge alert")


@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str = Path(..., description="ID of the alert")
):
    """Resolve an alert"""
    try:
        monitoring_service = MonitoringService()
        success = await monitoring_service.resolve_alert(alert_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert resolved successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to resolve alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to resolve alert")


@router.get("/dashboard")
async def get_dashboard_data(
    time_range: str = Query("24h", description="Time range for dashboard data")
):
    """Get dashboard data for monitoring UI"""
    try:
        monitoring_service = MonitoringService()
        dashboard_data = await monitoring_service.get_dashboard_data(time_range=time_range)
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard data")


@router.get("/models/{model_name}/drift")
async def get_model_drift(
    model_name: str = Path(..., description="Name of the model"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """Get model drift analysis"""
    try:
        monitoring_service = MonitoringService()
        drift_analysis = await monitoring_service.get_model_drift(model_name, days=days)
        
        return drift_analysis
        
    except Exception as e:
        logger.error(f"Failed to get model drift for {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model drift analysis")
