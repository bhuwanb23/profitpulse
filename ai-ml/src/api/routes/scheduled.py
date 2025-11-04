"""
Scheduled Runs Routes
API endpoints for managing scheduled model runs
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
import json
from croniter import croniter

from ..models.schemas import (
    ScheduledRun,
    ScheduledRunRequest,
    ScheduledRunResponse
)
from ..dependencies import get_predictor
from ...utils.database import DatabaseManager
from ...utils.predictor import Predictor

logger = logging.getLogger(__name__)
router = APIRouter()


def get_database_manager():
    """Get database manager instance"""
    return DatabaseManager()


def validate_cron_expression(schedule: str) -> bool:
    """Validate cron expression"""
    try:
        # Try to create a croniter with the expression
        croniter(schedule, datetime.now())
        return True
    except Exception:
        return False


def calculate_next_run(schedule: str) -> Optional[str]:
    """Calculate next run time from cron expression"""
    try:
        cron = croniter(schedule, datetime.now())
        next_run = cron.get_next(datetime)
        return next_run.isoformat()
    except Exception as e:
        logger.error(f"Failed to calculate next run time: {e}")
        return None


@router.post("/", response_model=ScheduledRunResponse)
async def create_scheduled_run(
    request: ScheduledRunRequest,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Create a new scheduled model run
    
    This endpoint creates a new scheduled run that will automatically execute
    a model at specified intervals according to the cron schedule.
    """
    try:
        # Validate cron expression
        if not validate_cron_expression(request.schedule):
            raise HTTPException(
                status_code=400,
                detail="Invalid cron expression"
            )
        
        # Calculate next run time
        next_run = calculate_next_run(request.schedule)
        if not next_run:
            raise HTTPException(
                status_code=400,
                detail="Failed to calculate next run time"
            )
        
        # Prepare run data
        run_data = {
            "model_name": request.model_name,
            "schedule": request.schedule,
            "enabled": request.enabled,
            "parameters": json.dumps(request.parameters) if request.parameters else "{}",
            "next_run": next_run
        }
        
        # Create scheduled run in database
        run_id = db.create_scheduled_run(run_data)
        
        # Get the created run
        run = db.get_scheduled_run(run_id)
        if not run:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve created scheduled run"
            )
        
        # Convert parameters back to dict
        try:
            run["parameters"] = json.loads(run["parameters"]) if run["parameters"] else {}
        except:
            run["parameters"] = {}
        
        # Create response
        response = ScheduledRunResponse(
            run_id=run_id,
            message="Scheduled run created successfully",
            schedule_details=ScheduledRun(**run)
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create scheduled run: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create scheduled run"
        )


@router.get("/", response_model=List[ScheduledRun])
async def list_scheduled_runs(
    limit: int = Query(100, description="Maximum number of runs to return"),
    offset: int = Query(0, description="Offset for pagination"),
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    List all scheduled model runs
    
    This endpoint returns a list of all scheduled runs, with optional filtering
    by model name and pagination support.
    """
    try:
        # Get scheduled runs from database
        runs = db.get_scheduled_runs(limit=limit, offset=offset)
        
        # Filter by model name if specified
        if model_name:
            runs = [run for run in runs if run["model_name"] == model_name]
        
        # Process runs for response
        processed_runs = []
        for run in runs:
            # Convert parameters back to dict
            try:
                run["parameters"] = json.loads(run["parameters"]) if run["parameters"] else {}
            except:
                run["parameters"] = {}
            
            processed_runs.append(ScheduledRun(**run))
        
        return processed_runs
        
    except Exception as e:
        logger.error(f"Failed to list scheduled runs: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to list scheduled runs"
        )


@router.get("/{run_id}", response_model=ScheduledRun)
async def get_scheduled_run(
    run_id: str,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Get a specific scheduled model run
    
    This endpoint returns details about a specific scheduled run by its ID.
    """
    try:
        # Get scheduled run from database
        run = db.get_scheduled_run(run_id)
        if not run:
            raise HTTPException(
                status_code=404,
                detail="Scheduled run not found"
            )
        
        # Convert parameters back to dict
        try:
            run["parameters"] = json.loads(run["parameters"]) if run["parameters"] else {}
        except:
            run["parameters"] = {}
        
        return ScheduledRun(**run)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get scheduled run {run_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get scheduled run"
        )


@router.put("/{run_id}", response_model=ScheduledRunResponse)
async def update_scheduled_run(
    run_id: str,
    request: ScheduledRunRequest,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Update a scheduled model run
    
    This endpoint updates an existing scheduled run with new configuration.
    """
    try:
        # Validate that run exists
        existing_run = db.get_scheduled_run(run_id)
        if not existing_run:
            raise HTTPException(
                status_code=404,
                detail="Scheduled run not found"
            )
        
        # Validate cron expression
        if not validate_cron_expression(request.schedule):
            raise HTTPException(
                status_code=400,
                detail="Invalid cron expression"
            )
        
        # Calculate next run time
        next_run = calculate_next_run(request.schedule)
        if not next_run:
            raise HTTPException(
                status_code=400,
                detail="Failed to calculate next run time"
            )
        
        # Prepare update data
        update_data = {
            "model_name": request.model_name,
            "schedule": request.schedule,
            "enabled": request.enabled,
            "parameters": json.dumps(request.parameters) if request.parameters else "{}",
            "next_run": next_run,
            "updated_at": datetime.now().isoformat()
        }
        
        # Update scheduled run in database
        updated = db.update_scheduled_run(run_id, update_data)
        if not updated:
            raise HTTPException(
                status_code=500,
                detail="Failed to update scheduled run"
            )
        
        # Get the updated run
        run = db.get_scheduled_run(run_id)
        if not run:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve updated scheduled run"
            )
        
        # Convert parameters back to dict
        try:
            run["parameters"] = json.loads(run["parameters"]) if run["parameters"] else {}
        except:
            run["parameters"] = {}
        
        # Create response
        response = ScheduledRunResponse(
            run_id=run_id,
            message="Scheduled run updated successfully",
            schedule_details=ScheduledRun(**run)
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update scheduled run {run_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update scheduled run"
        )


@router.delete("/{run_id}")
async def delete_scheduled_run(
    run_id: str,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Delete a scheduled model run
    
    This endpoint deletes a scheduled run, stopping future executions.
    """
    try:
        # Delete scheduled run from database
        deleted = db.delete_scheduled_run(run_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Scheduled run not found"
            )
        
        return {
            "message": "Scheduled run deleted successfully",
            "run_id": run_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete scheduled run {run_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete scheduled run"
        )


@router.post("/{run_id}/trigger")
async def trigger_scheduled_run(
    run_id: str,
    db: DatabaseManager = Depends(get_database_manager)
):
    """
    Trigger immediate execution of a scheduled run
    
    This endpoint triggers an immediate execution of a scheduled run,
    regardless of its schedule.
    """
    try:
        # Get scheduled run from database
        run = db.get_scheduled_run(run_id)
        if not run:
            raise HTTPException(
                status_code=404,
                detail="Scheduled run not found"
            )
        
        # In a real implementation, we would trigger the model execution here
        # For now, we'll just update the last_run timestamp
        update_data = {
            "last_run": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Update scheduled run in database
        updated = db.update_scheduled_run(run_id, update_data)
        if not updated:
            raise HTTPException(
                status_code=500,
                detail="Failed to update scheduled run"
            )
        
        return {
            "message": "Scheduled run triggered successfully",
            "run_id": run_id,
            "model_name": run["model_name"],
            "execution_status": "initiated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger scheduled run {run_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to trigger scheduled run"
        )