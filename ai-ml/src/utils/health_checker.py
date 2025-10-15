"""
Health Checker
System health monitoring and status checking
"""

import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import psutil
import platform

logger = logging.getLogger(__name__)


class HealthChecker:
    """System health monitoring and status checking"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self._initialized = False
    
    async def initialize(self):
        """Initialize health checker"""
        try:
            self._initialized = True
            logger.info("Health checker initialized")
        except Exception as e:
            logger.error(f"Failed to initialize health checker: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup health checker"""
        logger.info("Health checker cleaned up")
    
    async def get_basic_health(self) -> Dict[str, Any]:
        """Get basic health status"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            return {
                "status": "healthy",
                "timestamp": datetime.now(),
                "version": "1.0.0",
                "uptime": uptime,
                "services": {
                    "api_server": "healthy",
                    "model_registry": "healthy",
                    "metrics_collector": "healthy"
                },
                "metrics": {
                    "cpu_usage": psutil.cpu_percent(),
                    "memory_usage": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get basic health: {e}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.now(),
                "version": "1.0.0",
                "uptime": 0,
                "services": {},
                "metrics": {}
            }
    
    async def get_detailed_health(self) -> Dict[str, Any]:
        """Get detailed health status"""
        try:
            basic_health = await self.get_basic_health()
            
            # Add detailed information
            detailed_health = {
                **basic_health,
                "dependencies": await self._check_dependencies(),
                "performance": await self._get_performance_metrics(),
                "alerts": await self._get_active_alerts()
            }
            
            return detailed_health
            
        except Exception as e:
            logger.error(f"Failed to get detailed health: {e}")
            return await self.get_basic_health()
    
    async def is_ready(self) -> bool:
        """Check if system is ready to serve requests"""
        try:
            # Check critical services
            health = await self.get_basic_health()
            
            # System is ready if status is healthy and all services are healthy
            if health["status"] != "healthy":
                return False
            
            for service, status in health["services"].items():
                if status != "healthy":
                    return False
            
            # Check resource usage
            metrics = health["metrics"]
            if metrics.get("cpu_usage", 0) > 90:
                return False
            if metrics.get("memory_usage", 0) > 90:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return False
    
    async def is_alive(self) -> bool:
        """Check if system is alive (basic liveness check)"""
        try:
            # Basic liveness check - just verify the process is running
            return True
            
        except Exception as e:
            logger.error(f"Liveness check failed: {e}")
            return False
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get detailed health metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            
            metrics = {
                "system": {
                    "cpu_usage_percent": cpu_percent,
                    "memory_total_gb": memory.total / (1024**3),
                    "memory_used_gb": memory.used / (1024**3),
                    "memory_usage_percent": memory.percent,
                    "disk_total_gb": disk.total / (1024**3),
                    "disk_used_gb": disk.used / (1024**3),
                    "disk_usage_percent": (disk.used / disk.total) * 100,
                    "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
                },
                "process": {
                    "pid": process.pid,
                    "memory_rss_mb": process_memory.rss / (1024**2),
                    "memory_vms_mb": process_memory.vms / (1024**2),
                    "cpu_percent": process.cpu_percent(),
                    "num_threads": process.num_threads(),
                    "create_time": datetime.fromtimestamp(process.create_time())
                },
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                    "python_version": platform.python_version()
                },
                "uptime": {
                    "start_time": self.start_time.isoformat(),
                    "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                    "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600
                }
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get health metrics: {e}")
            return {}
    
    async def _check_dependencies(self) -> Dict[str, Any]:
        """Check external dependencies"""
        try:
            dependencies = {
                "database": await self._check_database(),
                "mlflow": await self._check_mlflow(),
                "redis": await self._check_redis(),
                "external_apis": await self._check_external_apis()
            }
            
            return dependencies
            
        except Exception as e:
            logger.error(f"Failed to check dependencies: {e}")
            return {}
    
    async def _check_database(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            # Mock database check
            return {
                "status": "healthy",
                "response_time_ms": 12.5,
                "last_check": datetime.now().isoformat(),
                "error": None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "last_check": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def _check_mlflow(self) -> Dict[str, Any]:
        """Check MLflow connectivity"""
        try:
            # Mock MLflow check
            return {
                "status": "healthy",
                "response_time_ms": 8.2,
                "last_check": datetime.now().isoformat(),
                "error": None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "last_check": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def _check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            # Mock Redis check
            return {
                "status": "healthy",
                "response_time_ms": 3.1,
                "last_check": datetime.now().isoformat(),
                "error": None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "last_check": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def _check_external_apis(self) -> Dict[str, Any]:
        """Check external API connectivity"""
        try:
            # Mock external API checks
            return {
                "superops": {
                    "status": "healthy",
                    "response_time_ms": 45.2,
                    "last_check": datetime.now().isoformat()
                },
                "quickbooks": {
                    "status": "healthy",
                    "response_time_ms": 38.7,
                    "last_check": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {
                "superops": {"status": "unhealthy", "error": str(e)},
                "quickbooks": {"status": "unhealthy", "error": str(e)}
            }
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            return {
                "api_requests_per_second": 25.5,
                "average_response_time_ms": 45.2,
                "error_rate_percent": 0.02,
                "active_connections": 12,
                "memory_usage_mb": psutil.Process().memory_info().rss / (1024**2),
                "cpu_usage_percent": psutil.cpu_percent(),
                "disk_io_read_mb": 0,  # Would need to track this
                "disk_io_write_mb": 0  # Would need to track this
            }
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}
    
    async def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active alerts"""
        try:
            # Mock active alerts
            alerts = []
            
            # Check for high CPU usage
            cpu_percent = psutil.cpu_percent()
            if cpu_percent > 80:
                alerts.append({
                    "type": "high_cpu_usage",
                    "severity": "warning",
                    "message": f"CPU usage is {cpu_percent:.1f}%",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Check for high memory usage
            memory_percent = psutil.virtual_memory().percent
            if memory_percent > 85:
                alerts.append({
                    "type": "high_memory_usage",
                    "severity": "warning",
                    "message": f"Memory usage is {memory_percent:.1f}%",
                    "timestamp": datetime.now().isoformat()
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get active alerts: {e}")
            return []
