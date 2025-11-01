"""
Budget Optimization Routes
Budget optimization and resource allocation endpoints
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ..models.schemas import (
    BudgetOptimizationRequest, 
    BudgetOptimizationResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from ..dependencies import get_predictor
from ...models.budget_optimizer.budget_optimizer import BudgetOptimizer
from ...utils.predictor import Predictor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=BudgetOptimizationResponse)
async def optimize_budget(
    request: BudgetOptimizationRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use"),
    return_confidence: bool = Query(False, description="Return confidence intervals")
):
    """
    Optimize budget allocation across departments or services
    
    This endpoint analyzes current budget data, department information, and constraints
    to recommend optimal budget allocation with expected ROI improvements.
    """
    try:
        # Initialize budget optimizer
        budget_optimizer = BudgetOptimizer()
        
        # Prepare data for budget optimization
        optimization_data = {
            "current_budget": request.current_budget,
            "departments": request.departments,
            "constraints": request.constraints
        }
        
        # In a real implementation, we would use the budget optimizer's optimize method
        # For now, we'll use the generic predictor with mock data
        
        # Make budget optimization using generic predictor
        predictor = Predictor()
        optimization_result = await predictor.predict(
            model_name="budget_optimizer",
            data=optimization_data,
            model_version=model_version,
            return_confidence=return_confidence
        )
        
        # Extract optimized allocation
        optimized_allocation = optimization_result["prediction"]
        
        # Estimate ROI improvement (mock calculation)
        confidence = optimization_result.get("confidence", 0.85)
        expected_roi_improvement = confidence * 0.25  # 25% max improvement at 100% confidence
        
        # Estimate efficiency gains (mock calculation)
        efficiency_gains = confidence * 0.15  # 15% max efficiency gain at 100% confidence
        
        # Build response
        response = BudgetOptimizationResponse(
            prediction=optimized_allocation,
            model_name="budget_optimizer",
            model_version=model_version or optimization_result.get("model_version", "1.0.0"),
            prediction_id=optimization_result.get("prediction_id", "mock_id"),
            timestamp=optimization_result.get("timestamp", datetime.now()),
            processing_time_ms=optimization_result.get("processing_time_ms", 50.0),
            confidence=confidence if return_confidence else None,
            optimized_allocation=optimized_allocation if isinstance(optimized_allocation, dict) else {},
            expected_roi_improvement=expected_roi_improvement,
            efficiency_gains=efficiency_gains
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Budget optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to optimize budget")


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_optimize_budgets(
    request: BatchPredictionRequest,
    model_version: Optional[str] = Query(None, description="Specific model version to use")
):
    """
    Perform batch budget optimizations for multiple scenarios
    
    This endpoint allows processing multiple budget optimizations in a single request.
    """
    try:
        # Initialize predictor
        predictor = Predictor()
        
        # Prepare data for batch optimizations
        if request.data:
            optimization_data_list = request.data
        else:
            # In a real implementation, we would fetch data from the provided URL
            raise HTTPException(status_code=400, detail="Batch data is required")
        
        # Make batch optimizations
        optimizations = await predictor.batch_predict(
            model_name="budget_optimizer",
            data_list=optimization_data_list,
            model_version=model_version,
            return_confidence=True
        )
        
        # Convert optimizations to proper format
        formatted_optimizations = []
        for opt in optimizations:
            optimized_allocation = opt["prediction"]
            
            # Estimate ROI improvement (mock calculation)
            confidence = opt.get("confidence", 0.85)
            expected_roi_improvement = confidence * 0.25  # 25% max improvement at 100% confidence
            
            # Estimate efficiency gains (mock calculation)
            efficiency_gains = confidence * 0.15  # 15% max efficiency gain at 100% confidence
            
            formatted_opt = BudgetOptimizationResponse(
                prediction=optimized_allocation,
                model_name="budget_optimizer",
                model_version=model_version or opt.get("model_version", "1.0.0"),
                prediction_id=opt.get("prediction_id", "mock_id"),
                timestamp=opt.get("timestamp", datetime.now()),
                processing_time_ms=opt.get("processing_time_ms", 50.0),
                confidence=confidence,
                optimized_allocation=optimized_allocation if isinstance(optimized_allocation, dict) else {},
                expected_roi_improvement=expected_roi_improvement,
                efficiency_gains=efficiency_gains
            )
            formatted_optimizations.append(formatted_opt)
        
        # Build batch response
        response = BatchPredictionResponse(
            predictions=formatted_optimizations,
            total_predictions=len(formatted_optimizations),
            processing_time_ms=sum(opt.processing_time_ms for opt in formatted_optimizations),
            model_name="budget_optimizer",
            model_version=model_version or "1.0.0"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch budget optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform batch budget optimizations")


@router.get("/models/{model_name}/info")
async def get_budget_model_info(
    model_name: str = "budget_optimizer"
):
    """
    Get budget optimization model information and capabilities
    """
    try:
        predictor = Predictor()
        model_info = await predictor.get_model_info(model_name)
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return model_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get budget model info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")


@router.get("/models/{model_name}/health")
async def get_budget_model_health(
    model_name: str = "budget_optimizer"
):
    """
    Get budget optimization model health status
    """
    try:
        predictor = Predictor()
        health_status = await predictor.get_model_health(model_name)
        
        return health_status
        
    except Exception as e:
        logger.error(f"Failed to get budget model health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model health")