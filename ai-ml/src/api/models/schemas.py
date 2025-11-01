"""
API Schemas
Pydantic models for request/response validation
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Base Models
class PredictionRequest(BaseModel):
    """Base prediction request model"""
    data: Dict[str, Any] = Field(..., description="Input data for prediction")
    model_version: Optional[str] = Field(None, description="Specific model version to use")
    return_probabilities: bool = Field(False, description="Whether to return prediction probabilities")
    return_confidence: bool = Field(False, description="Whether to return confidence scores")


class PredictionResponse(BaseModel):
    """Base prediction response model"""
    prediction: Union[float, int, str, List[Any]]
    model_name: str
    model_version: str
    prediction_id: str
    timestamp: datetime
    processing_time_ms: float
    confidence: Optional[float] = None
    probabilities: Optional[Dict[str, float]] = None


class BatchPredictionRequest(BaseModel):
    """Batch prediction request model"""
    data: List[Dict[str, Any]] = Field(..., description="List of input data for predictions")
    model_version: Optional[str] = Field(None, description="Specific model version to use")
    return_probabilities: bool = Field(False, description="Whether to return prediction probabilities")
    return_confidence: bool = Field(False, description="Whether to return confidence scores")


class BatchPredictionResponse(BaseModel):
    """Batch prediction response model"""
    predictions: List[PredictionResponse]
    total_predictions: int
    processing_time_ms: float
    model_name: str
    model_version: str


# Anomaly Detection Models
class AnomalyDetectionRequest(BaseModel):
    """Anomaly detection request"""
    data: List[Dict[str, Any]] = Field(..., description="Time series data for anomaly detection")
    stream_type: str = Field("system_metrics", description="Type of data stream")
    detection_method: str = Field("ensemble", description="Detection method to use")
    window_size: int = Field(100, description="Window size for analysis")


class AnomalyDetectionResponse(PredictionResponse):
    """Anomaly detection response"""
    anomalies: List[Dict[str, Any]] = Field(default_factory=list, description="Detected anomalies")
    severity_scores: List[float] = Field(default_factory=list, description="Anomaly severity scores")
    alert_triggered: bool = Field(False, description="Whether alert was triggered")


# Budget Optimization Models
class BudgetOptimizationRequest(BaseModel):
    """Budget optimization request"""
    current_budget: float = Field(..., description="Current budget allocation")
    departments: List[Dict[str, Any]] = Field(..., description="Department information")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Optimization constraints")
    optimization_method: str = Field("genetic_algorithm", description="Optimization method to use")


class BudgetOptimizationResponse(PredictionResponse):
    """Budget optimization response"""
    optimized_allocation: Dict[str, float] = Field(default_factory=dict, description="Optimized budget allocation")
    expected_roi_improvement: float = Field(0.0, description="Expected ROI improvement")
    efficiency_gains: float = Field(0.0, description="Expected efficiency gains")


# Demand Forecasting Models
class DemandForecastingRequest(BaseModel):
    """Demand forecasting request"""
    historical_data: List[Dict[str, Any]] = Field(..., description="Historical demand data")
    forecast_horizon: int = Field(30, description="Forecast horizon in days")
    seasonality: bool = Field(True, description="Whether to consider seasonality")
    method: str = Field("ensemble", description="Forecasting method to use")


class DemandForecastingResponse(PredictionResponse):
    """Demand forecasting response"""
    forecast: List[Dict[str, Any]] = Field(default_factory=list, description="Demand forecast")
    confidence_intervals: List[Dict[str, float]] = Field(default_factory=list, description="Confidence intervals")
    seasonal_components: Optional[Dict[str, Any]] = None


# Dynamic Pricing Models
class DynamicPricingRequest(BaseModel):
    """Dynamic pricing request"""
    client_profile: Dict[str, Any] = Field(..., description="Client profile information")
    service_type: str = Field(..., description="Type of service")
    market_conditions: Dict[str, Any] = Field(default_factory=dict, description="Current market conditions")
    competitor_data: List[Dict[str, Any]] = Field(default_factory=list, description="Competitor pricing data")


class DynamicPricingResponse(PredictionResponse):
    """Dynamic pricing response"""
    recommended_price: float = Field(..., description="Recommended price")
    price_range: Dict[str, float] = Field(default_factory=dict, description="Price range with confidence")
    market_sensitivity: float = Field(0.0, description="Market sensitivity score")
    acceptance_probability: float = Field(0.0, description="Probability of client acceptance")


# Client Churn Prediction Models
class ClientChurnPredictionRequest(BaseModel):
    """Client churn prediction request"""
    client_id: str = Field(..., description="Client identifier")
    features: Dict[str, Any] = Field(..., description="Client features for prediction")
    timeframe_days: int = Field(90, description="Prediction timeframe in days")


class ClientChurnPredictionResponse(PredictionResponse):
    """Client churn prediction response"""
    churn_probability: float = Field(..., description="Probability of churn")
    risk_level: str = Field("low", description="Risk level (low, medium, high)")
    intervention_recommendations: List[str] = Field(default_factory=list, description="Recommended interventions")


# Revenue Leak Detection Models
class RevenueLeakDetectionRequest(BaseModel):
    """Revenue leak detection request"""
    billing_data: List[Dict[str, Any]] = Field(..., description="Billing and invoice data")
    service_data: List[Dict[str, Any]] = Field(..., description="Service delivery data")
    time_period_days: int = Field(30, description="Analysis time period")


class RevenueLeakDetectionResponse(PredictionResponse):
    """Revenue leak detection response"""
    leak_probability: float = Field(..., description="Probability of revenue leak")
    leak_amount: float = Field(0.0, description="Estimated leak amount")
    leak_categories: List[str] = Field(default_factory=list, description="Categories of detected leaks")
    recovery_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Recovery recommendations")


# Client Profitability Prediction Models
class ClientProfitabilityPredictionRequest(BaseModel):
    """Client profitability prediction request"""
    client_id: str = Field(..., description="Client identifier")
    financial_data: Dict[str, Any] = Field(..., description="Financial data for analysis")
    operational_data: Dict[str, Any] = Field(default_factory=dict, description="Operational data")
    historical_period_months: int = Field(12, description="Historical analysis period")


class ClientProfitabilityPredictionResponse(PredictionResponse):
    """Client profitability prediction response"""
    profitability_score: float = Field(..., description="Profitability score (0-100)")
    profitability_category: str = Field("low", description="Profitability category (low, medium, high)")
    improvement_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Improvement recommendations")


# Bulk Processing Models
class BulkPredictionJob(BaseModel):
    """Bulk prediction job"""
    job_id: str
    model_name: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    total_records: int = 0
    processed_records: int = 0
    failed_records: int = 0


class BulkPredictionRequest(BaseModel):
    """Bulk prediction request"""
    model_name: str = Field(..., description="Model to use for predictions")
    data_file_url: Optional[str] = Field(None, description="URL to data file")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Data for prediction")
    callback_url: Optional[str] = Field(None, description="Callback URL for job completion")


class BulkPredictionResponse(BaseModel):
    """Bulk prediction response"""
    job_id: str
    status: str
    message: str
    estimated_completion_time: Optional[int] = None


# Scheduled Runs Models
class ScheduledRun(BaseModel):
    """Scheduled model run"""
    run_id: str
    model_name: str
    schedule: str  # Cron expression
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ScheduledRunRequest(BaseModel):
    """Scheduled run request"""
    model_name: str
    schedule: str  # Cron expression
    parameters: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


class ScheduledRunResponse(BaseModel):
    """Scheduled run response"""
    run_id: str
    message: str
    schedule_details: ScheduledRun


# Performance Reporting Models
class PerformanceMetrics(BaseModel):
    """Performance metrics"""
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    rmse: Optional[float] = None
    mae: Optional[float] = None
    r_squared: Optional[float] = None


class ModelPerformanceReport(BaseModel):
    """Model performance report"""
    model_name: str
    version: str
    period_start: datetime
    period_end: datetime
    metrics: PerformanceMetrics
    data_drift: Optional[Dict[str, Any]] = None
    concept_drift: Optional[Dict[str, Any]] = None
    recommendations: List[str] = Field(default_factory=list)


# Authentication Models
class AuthRequest(BaseModel):
    """Authentication request"""
    api_key: str = Field(..., description="API key for authentication")


class AuthResponse(BaseModel):
    """Authentication response"""
    token: str
    expires_in: int
    permissions: List[str]


# Alert Models
class Alert(BaseModel):
    """Alert model"""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    source: str
    details: Dict[str, Any] = Field(default_factory=dict)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


class AlertResponse(BaseModel):
    """Alert response"""
    alerts: List[Alert]
    total_count: int
    unread_count: int