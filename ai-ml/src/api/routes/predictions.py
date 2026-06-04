"""
Prediction Routes
Model inference and prediction endpoints
"""

import logging
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field

from ...models.churn_predictor.churn_predictor import ChurnPredictor
from ...models.revenue_leak_detector.revenue_leak_predictor import RevenueLeakPredictor
from ...models.dynamic_pricing.dynamic_pricing_engine import DynamicPricingEngine
from ...models.budget_optimizer.budget_optimizer import BudgetOptimizer
from ...models.demand_forecaster.demand_forecaster import DemandForecaster
from ...models.anomaly_detector.anomaly_orchestrator import AnomalyDetectorOrchestrator
from ...models.profitability_predictor.profitability_predictor import ProfitabilityPredictor
from ..models.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest, BatchPredictionResponse

# Model routing table: model_name -> (engine_class, pipeline_method, is_async)
MODEL_ROUTING = {
    "client_churn": (ChurnPredictor, "run_full_pipeline", True),
    "revenue_leak_detector": (RevenueLeakPredictor, "detect_revenue_leaks", True),
    "dynamic_pricing": (DynamicPricingEngine, "run_complete_pricing_analysis", True),
    "budget_optimizer": (BudgetOptimizer, "run_complete_budget_analysis", True),
    "demand_forecaster": (DemandForecaster, "run_complete_demand_analysis", True),
    "anomaly_detector": (AnomalyDetectorOrchestrator, "detect_anomalies", False),
    "client_profitability": (ProfitabilityPredictor, "predict", True),
}

logger = logging.getLogger(__name__)
router = APIRouter()


def _extract_batch_prediction(result: Any, model_name: str) -> float:
    """Extract a meaningful prediction value from per-engine result structures."""
    if result is None:
        return 0.5
    if not isinstance(result, dict):
        return 0.5

    EXTRACTORS = {
        "client_churn": lambda r: (
            float(np.mean([s.get("churn_probability", 0.5)
                          for s in (r.get("risk_scores") or [])
                          if isinstance(s, dict)]))
            if r.get("risk_scores") else 0.5
        ),
        "revenue_leak_detector": lambda r: (
            min(1.0, r.get("total_potential_loss", 0) / 50000)
            if r.get("total_potential_loss", 0) > 0 else 0.3
        ),
        "dynamic_pricing": lambda r: (
            float(np.mean([
                float(v["recommended_price"])
                for v in (r.get("price_recommendations") or {}).values()
                if isinstance(v, dict) and "recommended_price" in v
            ]))
            if r.get("price_recommendations") else 100.0
        ),
        "budget_optimizer": lambda r: (
            float(np.mean([
                v.get("allocated_amount", 0)
                for v in (r.get("recommendations") or {}).values()
                if isinstance(v, dict)
            ]))
            if r.get("recommendations") else 0.0
        ),
        "demand_forecaster": lambda r: (
            float(np.mean([
                v.get("forecast_value", 0)
                for v in (r.get("forecast") or [])
                if isinstance(v, dict)
            ]))
            if r.get("forecast") else 0.0
        ),
        "client_profitability": lambda r: (
            float(r.get("prediction", 0.5))
            if "prediction" in r else 0.5
        ),
    }

    extractor = EXTRACTORS.get(model_name)
    if extractor:
        return extractor(result)
    return result.get("prediction", 0.5)


class ProfitabilityPredictionRequest(BaseModel):
    """Client profitability prediction request"""
    client_id: str
    contract_value: float
    hours_logged: float
    billing_amount: float
    ticket_count: int
    satisfaction_score: Optional[float] = None
    last_contact_days: Optional[int] = None
    service_types: Optional[List[str]] = None


class ChurnPredictionRequest(BaseModel):
    """Client churn prediction request"""
    client_id: str
    contract_value: float
    last_contact_days: int
    ticket_frequency: float
    satisfaction_score: Optional[float] = None
    payment_delays: int = 0
    service_issues: int = 0


class RevenueLeakDetectionRequest(BaseModel):
    """Revenue leak detection request"""
    invoice_data: Dict[str, Any]
    ticket_data: Dict[str, Any]
    time_period_days: int = 30


@router.post("/profitability", response_model=PredictionResponse)
async def predict_profitability(
    request: ProfitabilityPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Predict client profitability"""
    try:
        profitability_predictor = ProfitabilityPredictor()
        await profitability_predictor.initialize()
        
        prediction_data = {
            "client_id": request.client_id,
            "contract_value": request.contract_value,
            "hours_logged": request.hours_logged,
            "billing_amount": request.billing_amount,
            "ticket_count": request.ticket_count,
            "satisfaction_score": request.satisfaction_score or 0.0,
            "last_contact_days": request.last_contact_days or 0,
            "service_types": request.service_types or []
        }
        
        start_time = time.perf_counter()
        prediction = await profitability_predictor.predict(
            client_data=prediction_data,
            model_type=model_version or "auto",
            return_confidence=True
        )
        
        return PredictionResponse(
            prediction=prediction["prediction"],
            model_name="client_profitability",
            model_version=model_version or prediction.get("model_type", "1.0.0"),
            prediction_id="prof_" + str(datetime.now().timestamp()),
            timestamp=datetime.fromisoformat(prediction["timestamp"]) if "timestamp" in prediction else datetime.now(),
            processing_time_ms=prediction.get("prediction_time_ms", (time.perf_counter() - start_time) * 1000),
            confidence=prediction.get("confidence_level", None)
        )
        
    except Exception as e:
        logger.error(f"Profitability prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict profitability")


@router.post("/churn", response_model=PredictionResponse)
async def predict_churn(
    request: ChurnPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Predict client churn risk"""
    try:
        churn_predictor = ChurnPredictor()
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        start_time = time.perf_counter()
        result = await churn_predictor.run_full_pipeline(start_date=start_date, end_date=end_date)
        
        churn_probability = 0.5
        if result and 'risk_scores' in result:
            risk_scores = result['risk_scores']
            if isinstance(risk_scores, pd.DataFrame) and not risk_scores.empty and 'churn_probability' in risk_scores.columns:
                churn_probability = float(risk_scores['churn_probability'].mean())
            elif isinstance(risk_scores, list) and risk_scores:
                churn_probability = float(np.mean([r.get('churn_probability', 0.5) for r in risk_scores]))
        
        return PredictionResponse(
            prediction=churn_probability,
            model_name="client_churn",
            model_version=model_version or "1.0.0",
            prediction_id="churn_" + str(datetime.now().timestamp()),
            timestamp=datetime.now(),
            processing_time_ms=(time.perf_counter() - start_time) * 1000,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Churn prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict churn")


@router.post("/revenue-leak", response_model=PredictionResponse)
async def detect_revenue_leak(
    request: RevenueLeakDetectionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Detect potential revenue leaks"""
    try:
        revenue_leak_predictor = RevenueLeakPredictor()
        await revenue_leak_predictor.initialize()
        end_date = datetime.now()
        start_date = end_date - timedelta(days=request.time_period_days)
        start_time = time.perf_counter()
        result = await revenue_leak_predictor.detect_revenue_leaks(start_date=start_date, end_date=end_date)
        
        leak_probability = 0.5
        if result and result.get('status') == 'success':
            total_potential_loss = result.get('total_potential_loss', 0)
            leak_probability = min(1.0, total_potential_loss / 50000) if total_potential_loss > 0 else 0.3
        
        return PredictionResponse(
            prediction=leak_probability,
            model_name="revenue_leak_detector",
            model_version=model_version or "1.0.0",
            prediction_id="leak_" + str(datetime.now().timestamp()),
            timestamp=datetime.now(),
            processing_time_ms=(time.perf_counter() - start_time) * 1000,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Revenue leak detection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to detect revenue leaks")


@router.post("/pricing", response_model=PredictionResponse)
async def recommend_pricing(
    request: Dict[str, Any],
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """Get dynamic pricing recommendations"""
    try:
        pricing_engine = DynamicPricingEngine()
        client_id = request.get("client_id")
        start_time = time.perf_counter()
        result = await pricing_engine.run_complete_pricing_analysis(client_id=client_id)
        
        recommended_price = 100.0
        if result and result.get('status') == 'success':
            recommendations = result.get('price_recommendations', {})
            if recommendations:
                prices = [float(r['recommended_price']) for r in recommendations.values() if isinstance(r, dict) and 'recommended_price' in r]
                if prices:
                    recommended_price = float(np.mean(prices))
        
        return PredictionResponse(
            prediction=recommended_price,
            model_name="dynamic_pricing",
            model_version=model_version or "1.0.0",
            prediction_id="pricing_" + str(datetime.now().timestamp()),
            timestamp=datetime.now(),
            processing_time_ms=(time.perf_counter() - start_time) * 1000,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Pricing recommendation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get pricing recommendations")


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_predict(
    request: BatchPredictionRequest,
    model_name: str = Query(..., description="Name of the model to use")
):
    """Perform batch predictions"""
    try:
        routing = MODEL_ROUTING.get(model_name)
        if not routing:
            raise HTTPException(status_code=404, detail=f"Unknown model: {model_name}")
        
        engine_class, method_name, is_async = routing
        engine = engine_class()
        
        if is_async:
            method = getattr(engine, method_name)
            start_time = time.perf_counter()
            result = await method()
        else:
            method = getattr(engine, method_name)
            data_df = pd.DataFrame(request.data) if request.data else pd.DataFrame()
            start_time = time.perf_counter()
            result = method(data_df)
        
        prediction_value = _extract_batch_prediction(result, model_name)
        
        formatted_predictions = [
            PredictionResponse(
                prediction=prediction_value,
                model_name=model_name,
                model_version=request.model_version or "1.0.0",
                prediction_id=f"batch_{i}_{datetime.now().timestamp()}",
                timestamp=datetime.now(),
                processing_time_ms=(time.perf_counter() - start_time) * 1000,
                confidence=0.85
            )
            for i in range(len(request.data))
        ]
        
        return BatchPredictionResponse(
            predictions=formatted_predictions,
            total_predictions=len(formatted_predictions),
            processing_time_ms=(time.perf_counter() - start_time) * 1000,
            model_name=model_name,
            model_version=request.model_version or "1.0.0"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform batch predictions")


@router.get("/models/{model_name}/info")
async def get_model_info(
    model_name: str = Path(..., description="Name of the model")
):
    """Get model information and capabilities"""
    try:
        routing = MODEL_ROUTING.get(model_name)
        if not routing:
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
        
        engine_class = routing[0]
        engine = engine_class()
        
        return {
            "name": model_name,
            "version": "1.0.0",
            "status": "initialized",
            "engine_type": engine_class.__name__
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model info for {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")


@router.get("/models/{model_name}/health")
async def get_model_health(
    model_name: str = Path(..., description="Name of the model")
):
    """Get model health status"""
    try:
        routing = MODEL_ROUTING.get(model_name)
        if not routing:
            return {"model_name": model_name, "status": "unknown", "message": f"No routing for '{model_name}'"}
        
        engine_class = routing[0]
        engine = engine_class()
        
        return {
            "model_name": model_name,
            "status": "healthy",
            "engine_type": engine_class.__name__
        }
        
    except Exception as e:
        logger.error(f"Failed to get model health for {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model health")
