"""
Metrics Collector
System and model performance metrics collection
"""

import logging
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = None


class MetricsCollector:
    """Collects and stores system and model metrics"""
    
    def __init__(self):
        self.metrics_store: Dict[str, List[MetricPoint]] = {}
        self._initialized = False
        self._collection_task = None
    
    async def initialize(self):
        """Initialize metrics collector"""
        try:
            self._initialized = True
            # Start background metrics collection
            self._collection_task = asyncio.create_task(self._collect_metrics_loop())
            logger.info("Metrics collector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize metrics collector: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup metrics collector"""
        if self._collection_task:
            self._collection_task.cancel()
            try:
                await self._collection_task
            except asyncio.CancelledError:
                pass
        logger.info("Metrics collector cleaned up")
    
    async def _collect_metrics_loop(self):
        """Background metrics collection loop"""
        while True:
            try:
                await self._collect_system_metrics()
                await asyncio.sleep(60)  # Collect every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                await asyncio.sleep(60)
    
    async def _collect_system_metrics(self):
        """Collect system-level metrics"""
        try:
            # CPU usage (mock)
            cpu_usage = 45.2 + (time.time() % 10) * 2
            
            # Memory usage (mock)
            memory_usage = 68.5 + (time.time() % 15) * 1.5
            
            # Request count (mock)
            request_count = 150 + int(time.time() % 50)
            
            # Record metrics
            await self.record_metric("system.cpu_usage", cpu_usage, {"type": "system"})
            await self.record_metric("system.memory_usage", memory_usage, {"type": "system"})
            await self.record_metric("system.request_count", request_count, {"type": "system"})
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
    
    async def record_metric(self, metric_name: str, value: float, tags: Dict[str, str] = None):
        """Record a metric value"""
        try:
            if metric_name not in self.metrics_store:
                self.metrics_store[metric_name] = []
            
            metric_point = MetricPoint(
                timestamp=datetime.now(),
                value=value,
                tags=tags or {}
            )
            
            self.metrics_store[metric_name].append(metric_point)
            
            # Keep only last 1000 points per metric
            if len(self.metrics_store[metric_name]) > 1000:
                self.metrics_store[metric_name] = self.metrics_store[metric_name][-1000:]
            
        except Exception as e:
            logger.error(f"Failed to record metric {metric_name}: {e}")
    
    async def get_metrics(self, metric_name: str = None, 
                         time_range: str = "1h") -> Dict[str, Any]:
        """Get metrics for a specific metric or all metrics"""
        try:
            # Parse time range
            time_delta = self._parse_time_range(time_range)
            cutoff_time = datetime.now() - time_delta
            
            if metric_name:
                # Get specific metric
                if metric_name not in self.metrics_store:
                    return {}
                
                points = [
                    point for point in self.metrics_store[metric_name]
                    if point.timestamp >= cutoff_time
                ]
                
                return {
                    "metric_name": metric_name,
                    "points": [
                        {
                            "timestamp": point.timestamp.isoformat(),
                            "value": point.value,
                            "tags": point.tags
                        }
                        for point in points
                    ],
                    "count": len(points)
                }
            else:
                # Get all metrics
                all_metrics = {}
                for name, points in self.metrics_store.items():
                    filtered_points = [
                        point for point in points
                        if point.timestamp >= cutoff_time
                    ]
                    
                    if filtered_points:
                        all_metrics[name] = {
                            "points": [
                                {
                                    "timestamp": point.timestamp.isoformat(),
                                    "value": point.value,
                                    "tags": point.tags
                                }
                                for point in filtered_points
                            ],
                            "count": len(filtered_points)
                        }
                
                return all_metrics
                
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {}
    
    async def get_model_metrics(self, model_name: str, 
                               time_range: str = "24h") -> Dict[str, Any]:
        """Get metrics for a specific model"""
        try:
            time_delta = self._parse_time_range(time_range)
            cutoff_time = datetime.now() - time_delta
            
            model_metrics = {}
            
            # Get model-specific metrics
            for metric_name, points in self.metrics_store.items():
                if f"model.{model_name}" in metric_name:
                    filtered_points = [
                        point for point in points
                        if point.timestamp >= cutoff_time
                    ]
                    
                    if filtered_points:
                        model_metrics[metric_name] = {
                            "points": [
                                {
                                    "timestamp": point.timestamp.isoformat(),
                                    "value": point.value,
                                    "tags": point.tags
                                }
                                for point in filtered_points
                            ],
                            "count": len(filtered_points)
                        }
            
            return model_metrics
            
        except Exception as e:
            logger.error(f"Failed to get model metrics for {model_name}: {e}")
            return {}
    
    async def record_model_metric(self, model_name: str, metric_name: str, 
                                 value: float, tags: Dict[str, str] = None):
        """Record a model-specific metric"""
        full_metric_name = f"model.{model_name}.{metric_name}"
        await self.record_metric(full_metric_name, value, tags)
    
    def _parse_time_range(self, time_range: str) -> timedelta:
        """Parse time range string to timedelta"""
        time_ranges = {
            "1h": timedelta(hours=1),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30)
        }
        return time_ranges.get(time_range, timedelta(hours=1))
    
    async def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for all metrics"""
        try:
            summary = {}
            
            for metric_name, points in self.metrics_store.items():
                if not points:
                    continue
                
                values = [point.value for point in points]
                summary[metric_name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "latest": values[-1] if values else None,
                    "latest_timestamp": points[-1].timestamp.isoformat() if points else None
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get summary stats: {e}")
            return {}
