"""
Data Extractor Service
Comprehensive data extraction from SuperOps with real-time streaming capabilities
"""

import logging
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import asdict
import pandas as pd

from .superops_client import (
    SuperOpsClient, create_superops_client,
    Ticket, Client, Technician, SLAMetrics, ServiceDeliveryMetrics
)
from config import settings

logger = logging.getLogger(__name__)


class DataExtractor:
    """Comprehensive data extraction service for SuperOps"""
    
    def __init__(self):
        self.superops_client: Optional[SuperOpsClient] = None
        self._extraction_stats = {
            "tickets_extracted": 0,
            "clients_extracted": 0,
            "technicians_extracted": 0,
            "sla_metrics_extracted": 0,
            "service_metrics_extracted": 0,
            "last_extraction": None,
            "extraction_duration": 0.0
        }
    
    async def initialize(self):
        """Initialize the data extractor"""
        try:
            self.superops_client = create_superops_client()
            await self.superops_client.initialize()
            logger.info("Data extractor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize data extractor: {e}")
            raise
    
    async def close(self):
        """Close the data extractor"""
        if self.superops_client:
            await self.superops_client.close()
        logger.info("Data extractor closed")
    
    async def extract_ticket_data(self, 
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None,
                                 filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract comprehensive ticket data"""
        try:
            logger.info("Starting ticket data extraction...")
            
            # Set default date range if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Extract tickets from SuperOps
            tickets = await self.superops_client.get_tickets(
                start_date=start_date,
                end_date=end_date,
                status=filters.get("status") if filters else None,
                priority=filters.get("priority") if filters else None,
                client_id=filters.get("client_id") if filters else None,
                technician_id=filters.get("technician_id") if filters else None
            )
            
            # Convert to dictionaries for easier processing
            ticket_data = [asdict(ticket) for ticket in tickets]
            
            # Add derived metrics
            for ticket in ticket_data:
                ticket = self._add_ticket_derived_metrics(ticket)
            
            self._extraction_stats["tickets_extracted"] = len(ticket_data)
            logger.info(f"Extracted {len(ticket_data)} tickets")
            
            return ticket_data
            
        except Exception as e:
            logger.error(f"Failed to extract ticket data: {e}")
            return []
    
    async def extract_client_data(self, 
                                 include_inactive: bool = False,
                                 filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract comprehensive client data"""
        try:
            logger.info("Starting client data extraction...")
            
            # Extract clients from SuperOps
            clients = await self.superops_client.get_clients(
                include_inactive=include_inactive
            )
            
            # Convert to dictionaries
            client_data = [asdict(client) for client in clients]
            
            # Add derived metrics
            for client in client_data:
                client = self._add_client_derived_metrics(client)
            
            # Apply filters if provided
            if filters:
                client_data = self._apply_client_filters(client_data, filters)
            
            self._extraction_stats["clients_extracted"] = len(client_data)
            logger.info(f"Extracted {len(client_data)} clients")
            
            return client_data
            
        except Exception as e:
            logger.error(f"Failed to extract client data: {e}")
            return []
    
    async def extract_technician_data(self, 
                                    include_inactive: bool = False,
                                    filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract comprehensive technician data"""
        try:
            logger.info("Starting technician data extraction...")
            
            # Extract technicians from SuperOps
            technicians = await self.superops_client.get_technicians(
                include_inactive=include_inactive
            )
            
            # Convert to dictionaries
            technician_data = [asdict(technician) for technician in technicians]
            
            # Add derived metrics
            for technician in technician_data:
                technician = self._add_technician_derived_metrics(technician)
            
            # Apply filters if provided
            if filters:
                technician_data = self._apply_technician_filters(technician_data, filters)
            
            self._extraction_stats["technicians_extracted"] = len(technician_data)
            logger.info(f"Extracted {len(technician_data)} technicians")
            
            return technician_data
            
        except Exception as e:
            logger.error(f"Failed to extract technician data: {e}")
            return []
    
    async def extract_sla_metrics(self, 
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None,
                                 ticket_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract SLA metrics and compliance data"""
        try:
            logger.info("Starting SLA metrics extraction...")
            
            # Set default date range if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Extract SLA metrics from SuperOps
            sla_metrics = await self.superops_client.get_sla_metrics(
                start_date=start_date,
                end_date=end_date,
                ticket_id=ticket_id
            )
            
            # Convert to dictionaries
            sla_data = [asdict(metric) for metric in sla_metrics]
            
            # Add derived metrics
            for metric in sla_data:
                metric = self._add_sla_derived_metrics(metric)
            
            self._extraction_stats["sla_metrics_extracted"] = len(sla_data)
            logger.info(f"Extracted {len(sla_data)} SLA metrics")
            
            return sla_data
            
        except Exception as e:
            logger.error(f"Failed to extract SLA metrics: {e}")
            return []
    
    async def extract_service_delivery_metrics(self, 
                                             start_date: Optional[datetime] = None,
                                             end_date: Optional[datetime] = None,
                                             granularity: str = "daily") -> List[Dict[str, Any]]:
        """Extract service delivery metrics"""
        try:
            logger.info("Starting service delivery metrics extraction...")
            
            # Set default date range if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Extract service delivery metrics from SuperOps
            service_metrics = await self.superops_client.get_service_delivery_metrics(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity
            )
            
            # Convert to dictionaries
            service_data = [asdict(metric) for metric in service_metrics]
            
            # Add derived metrics
            for metric in service_data:
                metric = self._add_service_delivery_derived_metrics(metric)
            
            self._extraction_stats["service_metrics_extracted"] = len(service_data)
            logger.info(f"Extracted {len(service_data)} service delivery metrics")
            
            return service_data
            
        except Exception as e:
            logger.error(f"Failed to extract service delivery metrics: {e}")
            return []
    
    async def extract_technician_productivity(self, 
                                            technician_id: Optional[str] = None,
                                            start_date: Optional[datetime] = None,
                                            end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Extract technician productivity data"""
        try:
            logger.info("Starting technician productivity extraction...")
            
            # Extract productivity data from SuperOps
            productivity_data = await self.superops_client.get_technician_productivity(
                technician_id=technician_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Add derived metrics
            productivity_data = self._add_productivity_derived_metrics(productivity_data)
            
            logger.info("Extracted technician productivity data")
            return productivity_data
            
        except Exception as e:
            logger.error(f"Failed to extract technician productivity: {e}")
            return {}
    
    async def extract_all_data(self, 
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None,
                              include_inactive: bool = False) -> Dict[str, Any]:
        """Extract all data types in one operation"""
        try:
            logger.info("Starting comprehensive data extraction...")
            start_time = datetime.now()
            
            # Set default date range if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Extract all data types concurrently
            tasks = [
                self.extract_ticket_data(start_date, end_date),
                self.extract_client_data(include_inactive),
                self.extract_technician_data(include_inactive),
                self.extract_sla_metrics(start_date, end_date),
                self.extract_service_delivery_metrics(start_date, end_date)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            all_data = {
                "tickets": results[0] if not isinstance(results[0], Exception) else [],
                "clients": results[1] if not isinstance(results[1], Exception) else [],
                "technicians": results[2] if not isinstance(results[2], Exception) else [],
                "sla_metrics": results[3] if not isinstance(results[3], Exception) else [],
                "service_delivery_metrics": results[4] if not isinstance(results[4], Exception) else [],
                "extraction_metadata": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "extraction_timestamp": datetime.now().isoformat(),
                    "total_records": sum(len(data) for data in all_data.values() if isinstance(data, list)),
                    "extraction_duration": (datetime.now() - start_time).total_seconds()
                }
            }
            
            # Update extraction stats
            self._extraction_stats["last_extraction"] = datetime.now()
            self._extraction_stats["extraction_duration"] = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"Comprehensive data extraction completed in {self._extraction_stats['extraction_duration']:.2f}s")
            return all_data
            
        except Exception as e:
            logger.error(f"Failed to extract all data: {e}")
            return {}
    
    async def stream_real_time_data(self, interval_seconds: int = 60) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream real-time data at specified intervals"""
        try:
            logger.info(f"Starting real-time data streaming (interval: {interval_seconds}s)")
            
            while True:
                try:
                    # Get real-time data
                    real_time_data = await self.superops_client.get_real_time_data()
                    
                    # Add streaming metadata
                    real_time_data["stream_metadata"] = {
                        "timestamp": datetime.now().isoformat(),
                        "interval_seconds": interval_seconds,
                        "stream_id": f"stream_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    }
                    
                    yield real_time_data
                    
                    # Wait for next interval
                    await asyncio.sleep(interval_seconds)
                    
                except Exception as e:
                    logger.error(f"Error in real-time streaming: {e}")
                    await asyncio.sleep(interval_seconds)  # Continue streaming despite errors
                    
        except asyncio.CancelledError:
            logger.info("Real-time data streaming cancelled")
        except Exception as e:
            logger.error(f"Real-time streaming failed: {e}")
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get extraction statistics"""
        return self._extraction_stats.copy()
    
    def _add_ticket_derived_metrics(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics to ticket data"""
        try:
            # Calculate ticket age
            if ticket.get("created_date"):
                created_date = datetime.fromisoformat(ticket["created_date"])
                ticket["ticket_age_days"] = (datetime.now() - created_date).days
            
            # Calculate resolution time
            if ticket.get("resolved_date") and ticket.get("created_date"):
                created_date = datetime.fromisoformat(ticket["created_date"])
                resolved_date = datetime.fromisoformat(ticket["resolved_date"])
                ticket["resolution_time_hours"] = (resolved_date - created_date).total_seconds() / 3600
            
            # Calculate efficiency ratio
            if ticket.get("estimated_hours") and ticket.get("actual_hours"):
                ticket["efficiency_ratio"] = ticket["estimated_hours"] / ticket["actual_hours"]
            
            # Calculate revenue per hour
            if ticket.get("total_cost") and ticket.get("actual_hours"):
                ticket["revenue_per_hour"] = ticket["total_cost"] / ticket["actual_hours"]
            
            # Add priority score
            priority_scores = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
            ticket["priority_score"] = priority_scores.get(ticket.get("priority", "Low"), 1)
            
            # Add status score
            status_scores = {"Open": 1, "In Progress": 2, "Pending": 3, "Resolved": 4, "Closed": 5}
            ticket["status_score"] = status_scores.get(ticket.get("status", "Open"), 1)
            
        except Exception as e:
            logger.warning(f"Failed to add derived metrics to ticket: {e}")
        
        return ticket
    
    def _add_client_derived_metrics(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics to client data"""
        try:
            # Calculate contract duration
            if client.get("contract_start_date") and client.get("contract_end_date"):
                start_date = datetime.fromisoformat(client["contract_start_date"])
                end_date = datetime.fromisoformat(client["contract_end_date"])
                client["contract_duration_days"] = (end_date - start_date).days
            
            # Calculate days since last activity
            if client.get("last_activity"):
                last_activity = datetime.fromisoformat(client["last_activity"])
                client["days_since_last_activity"] = (datetime.now() - last_activity).days
            
            # Add contract value tier
            contract_value = client.get("contract_value", 0)
            if contract_value < 5000:
                client["contract_tier"] = "Small"
            elif contract_value < 20000:
                client["contract_tier"] = "Medium"
            else:
                client["contract_tier"] = "Large"
            
            # Add service level score
            service_levels = {"Basic": 1, "Standard": 2, "Premium": 3}
            client["service_level_score"] = service_levels.get(client.get("service_level", "Basic"), 1)
            
        except Exception as e:
            logger.warning(f"Failed to add derived metrics to client: {e}")
        
        return client
    
    def _add_technician_derived_metrics(self, technician: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics to technician data"""
        try:
            # Calculate days since last active
            if technician.get("last_active"):
                last_active = datetime.fromisoformat(technician["last_active"])
                technician["days_since_last_active"] = (datetime.now() - last_active).days
            
            # Calculate productivity score
            tickets_resolved = technician.get("tickets_resolved", 0)
            avg_resolution_time = technician.get("avg_resolution_time", 1)
            customer_satisfaction = technician.get("customer_satisfaction", 3.0)
            
            # Simple productivity calculation
            technician["productivity_score"] = (
                (tickets_resolved / 100) * 0.4 +
                (5 / avg_resolution_time) * 0.3 +
                (customer_satisfaction / 5) * 0.3
            )
            
            # Add skill level
            skills_count = len(technician.get("skills", []))
            certifications_count = len(technician.get("certifications", []))
            
            if skills_count >= 5 and certifications_count >= 3:
                technician["skill_level"] = "Expert"
            elif skills_count >= 3 and certifications_count >= 2:
                technician["skill_level"] = "Advanced"
            elif skills_count >= 2:
                technician["skill_level"] = "Intermediate"
            else:
                technician["skill_level"] = "Beginner"
            
        except Exception as e:
            logger.warning(f"Failed to add derived metrics to technician: {e}")
        
        return technician
    
    def _add_sla_derived_metrics(self, sla_metric: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics to SLA data"""
        try:
            # Calculate SLA compliance
            target_time = sla_metric.get("target_time", 0)
            actual_time = sla_metric.get("actual_time", 0)
            
            if target_time > 0:
                sla_metric["sla_compliance_ratio"] = target_time / actual_time if actual_time > 0 else 1.0
                sla_metric["sla_breach_minutes"] = max(0, actual_time - target_time)
            else:
                sla_metric["sla_compliance_ratio"] = 1.0
                sla_metric["sla_breach_minutes"] = 0
            
            # Add SLA performance category
            compliance_ratio = sla_metric["sla_compliance_ratio"]
            if compliance_ratio >= 1.0:
                sla_metric["performance_category"] = "Met"
            elif compliance_ratio >= 0.8:
                sla_metric["performance_category"] = "Warning"
            else:
                sla_metric["performance_category"] = "Breached"
            
        except Exception as e:
            logger.warning(f"Failed to add derived metrics to SLA metric: {e}")
        
        return sla_metric
    
    def _add_service_delivery_derived_metrics(self, service_metric: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics to service delivery data"""
        try:
            # Calculate resolution rate
            total_tickets = service_metric.get("total_tickets", 0)
            resolved_tickets = service_metric.get("resolved_tickets", 0)
            
            if total_tickets > 0:
                service_metric["resolution_rate"] = resolved_tickets / total_tickets
            else:
                service_metric["resolution_rate"] = 0.0
            
            # Calculate efficiency metrics
            revenue = service_metric.get("revenue_generated", 0)
            cost_per_ticket = service_metric.get("cost_per_ticket", 0)
            
            if cost_per_ticket > 0:
                service_metric["profit_margin"] = (revenue - (cost_per_ticket * total_tickets)) / revenue if revenue > 0 else 0
            else:
                service_metric["profit_margin"] = 0.0
            
            # Add performance category
            sla_compliance = service_metric.get("sla_compliance_rate", 0)
            customer_satisfaction = service_metric.get("customer_satisfaction", 0)
            
            if sla_compliance >= 0.9 and customer_satisfaction >= 4.0:
                service_metric["performance_category"] = "Excellent"
            elif sla_compliance >= 0.8 and customer_satisfaction >= 3.5:
                service_metric["performance_category"] = "Good"
            elif sla_compliance >= 0.7 and customer_satisfaction >= 3.0:
                service_metric["performance_category"] = "Average"
            else:
                service_metric["performance_category"] = "Needs Improvement"
            
        except Exception as e:
            logger.warning(f"Failed to add derived metrics to service delivery metric: {e}")
        
        return service_metric
    
    def _add_productivity_derived_metrics(self, productivity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add derived metrics to productivity data"""
        try:
            # Calculate efficiency score
            tickets_resolved = productivity_data.get("tickets_resolved", 0)
            avg_resolution_time = productivity_data.get("avg_resolution_time", 1)
            utilization_rate = productivity_data.get("utilization_rate", 0)
            
            productivity_data["efficiency_score"] = (
                (tickets_resolved / 50) * 0.4 +
                (5 / avg_resolution_time) * 0.3 +
                utilization_rate * 0.3
            )
            
            # Add productivity category
            efficiency_score = productivity_data["efficiency_score"]
            if efficiency_score >= 0.8:
                productivity_data["productivity_category"] = "High"
            elif efficiency_score >= 0.6:
                productivity_data["productivity_category"] = "Medium"
            else:
                productivity_data["productivity_category"] = "Low"
            
        except Exception as e:
            logger.warning(f"Failed to add derived metrics to productivity data: {e}")
        
        return productivity_data
    
    def _apply_client_filters(self, clients: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filters to client data"""
        filtered_clients = clients
        
        if "industry" in filters:
            filtered_clients = [c for c in filtered_clients if c.get("industry") == filters["industry"]]
        
        if "contract_tier" in filters:
            filtered_clients = [c for c in filtered_clients if c.get("contract_tier") == filters["contract_tier"]]
        
        if "service_level" in filters:
            filtered_clients = [c for c in filtered_clients if c.get("service_level") == filters["service_level"]]
        
        return filtered_clients
    
    def _apply_technician_filters(self, technicians: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filters to technician data"""
        filtered_technicians = technicians
        
        if "department" in filters:
            filtered_technicians = [t for t in filtered_technicians if t.get("department") == filters["department"]]
        
        if "skill_level" in filters:
            filtered_technicians = [t for t in filtered_technicians if t.get("skill_level") == filters["skill_level"]]
        
        if "role" in filters:
            filtered_technicians = [t for t in filtered_technicians if t.get("role") == filters["role"]]
        
        return filtered_technicians


# Factory function for creating data extractor
def create_data_extractor() -> DataExtractor:
    """Create data extractor instance"""
    return DataExtractor()
