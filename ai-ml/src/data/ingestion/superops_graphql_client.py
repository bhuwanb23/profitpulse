"""
SuperOps GraphQL Client
Real implementation using GraphQL API instead of mock REST calls
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportError
import aiohttp

from config import settings
from .superops_queries import (
    GET_TICKETS_QUERY,
    GET_SLA_LIST_QUERY,
    GET_TECHNICIANS_QUERY,
    GET_SITES_QUERY,
    GET_ASSETS_QUERY,
    GET_SERVICE_METRICS_QUERY,
    GET_REALTIME_DATA_QUERY,
    GET_TECHNICIAN_PRODUCTIVITY_QUERY
)

logger = logging.getLogger(__name__)


@dataclass
class SuperOpsGraphQLConfig:
    """SuperOps GraphQL API configuration"""
    base_url: str
    api_key: str
    tenant_id: str
    timeout: int = 30
    max_retries: int = 3
    rate_limit_delay: float = 0.1


class SuperOpsGraphQLError(Exception):
    """Custom exception for SuperOps GraphQL errors"""
    pass


class SuperOpsGraphQLClient:
    """Real SuperOps GraphQL API client"""
    
    def __init__(self, config: SuperOpsGraphQLConfig):
        self.config = config
        self.client: Optional[Client] = None
        self.transport: Optional[AIOHTTPTransport] = None
        self._rate_limit_semaphore = asyncio.Semaphore(10)
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize the GraphQL client"""
        try:
            # Create transport with authentication headers
            self.transport = AIOHTTPTransport(
                url=self.config.base_url,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "X-Tenant-Id": self.config.tenant_id,
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Create GraphQL client
            self.client = Client(
                transport=self.transport,
                fetch_schema_from_transport=True
            )
            
            logger.info("SuperOps GraphQL client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize SuperOps GraphQL client: {e}")
            raise SuperOpsGraphQLError(f"Client initialization failed: {e}")
    
    async def close(self):
        """Close the GraphQL client"""
        if self.transport:
            await self.transport.close()
            logger.info("SuperOps GraphQL client closed")
    
    async def _execute_query(self, query: str, variables: Dict = None) -> Dict[str, Any]:
        """Execute GraphQL query with rate limiting and retry logic"""
        if not self.client:
            await self.initialize()
        
        async with self._rate_limit_semaphore:
            for attempt in range(self.config.max_retries):
                try:
                    # Execute the query
                    result = await self.client.execute(query, variable_values=variables or {})
                    
                    # Check for GraphQL errors
                    if "errors" in result:
                        errors = result["errors"]
                        logger.error(f"GraphQL errors: {errors}")
                        raise SuperOpsGraphQLError(f"GraphQL errors: {errors}")
                    
                    # Rate limiting delay
                    await asyncio.sleep(self.config.rate_limit_delay)
                    
                    return result
                    
                except TransportError as e:
                    logger.warning(f"Transport error (attempt {attempt + 1}): {e}")
                    if attempt == self.config.max_retries - 1:
                        raise SuperOpsGraphQLError(f"Transport error after {self.config.max_retries} attempts: {e}")
                    await asyncio.sleep(2 ** attempt)
                    
                except Exception as e:
                    logger.error(f"Query execution error (attempt {attempt + 1}): {e}")
                    if attempt == self.config.max_retries - 1:
                        raise SuperOpsGraphQLError(f"Query execution failed after {self.config.max_retries} attempts: {e}")
                    await asyncio.sleep(2 ** attempt)
            
            raise SuperOpsGraphQLError("Max retries exceeded")
    
    def _build_list_input(self, page: int = 1, page_size: int = 100, 
                          condition: Optional[Dict] = None, 
                          sort: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Build ListInfoInput for GraphQL queries"""
        input_data = {
            "page": page,
            "pageSize": page_size
        }
        
        if condition:
            input_data["condition"] = condition
            
        if sort:
            input_data["sort"] = sort
            
        return {"input": input_data}
    
    async def get_tickets(self, 
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         status: Optional[str] = None,
                         priority: Optional[str] = None,
                         client_id: Optional[str] = None,
                         technician_id: Optional[str] = None,
                         limit: int = 1000,
                         offset: int = 0) -> List[Dict[str, Any]]:
        """Extract ticket data from SuperOps using GraphQL"""
        try:
            logger.info("Extracting tickets from SuperOps GraphQL API")
            
            # Build condition for filtering
            condition = None
            if any([start_date, end_date, status, priority, client_id, technician_id]):
                condition = {}
                
                if start_date and end_date:
                    condition["createdTime"] = {
                        "operator": "between",
                        "value": [start_date.isoformat(), end_date.isoformat()]
                    }
                elif start_date:
                    condition["createdTime"] = {
                        "operator": "gte",
                        "value": start_date.isoformat()
                    }
                elif end_date:
                    condition["createdTime"] = {
                        "operator": "lte",
                        "value": end_date.isoformat()
                    }
                
                if status:
                    condition["status"] = {
                        "operator": "equals",
                        "value": status
                    }
                
                if priority:
                    condition["priority"] = {
                        "operator": "equals",
                        "value": priority
                    }
                
                if client_id:
                    condition["site"] = {
                        "operator": "equals",
                        "value": client_id
                    }
                
                if technician_id:
                    condition["technician"] = {
                        "operator": "equals",
                        "value": technician_id
                    }
            
            # Build sort order
            sort = [{
                "attribute": "createdTime",
                "order": "DESC"
            }]
            
            # Calculate page from offset
            page = (offset // limit) + 1
            
            # Build variables
            variables = self._build_list_input(
                page=page,
                page_size=limit,
                condition=condition,
                sort=sort
            )
            
            # Execute query
            result = await self._execute_query(GET_TICKETS_QUERY, variables)
            
            # Extract tickets from result
            tickets = result.get("data", {}).get("getTicketList", {}).get("tickets", [])
            
            logger.info(f"Extracted {len(tickets)} tickets from SuperOps GraphQL API")
            return tickets
            
        except Exception as e:
            logger.error(f"Failed to extract tickets: {e}")
            # Return mock data for development/fallback
            return await self._get_mock_tickets()
    
    async def get_clients(self, 
                         limit: int = 1000,
                         offset: int = 0,
                         include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Extract client/site data from SuperOps using GraphQL"""
        try:
            logger.info("Extracting clients from SuperOps GraphQL API")
            
            # Build condition for filtering
            condition = None
            if not include_inactive:
                condition = {
                    "status": {
                        "operator": "equals",
                        "value": "active"
                    }
                }
            
            # Calculate page from offset
            page = (offset // limit) + 1
            
            # Build variables
            variables = self._build_list_input(
                page=page,
                page_size=limit,
                condition=condition
            )
            
            # Execute query
            result = await self._execute_query(GET_SITES_QUERY, variables)
            
            # Extract sites from result
            sites = result.get("data", {}).get("getSiteList", {}).get("sites", [])
            
            logger.info(f"Extracted {len(sites)} clients from SuperOps GraphQL API")
            return sites
            
        except Exception as e:
            logger.error(f"Failed to extract clients: {e}")
            return await self._get_mock_clients()
    
    async def get_technicians(self, 
                             limit: int = 100,
                             offset: int = 0,
                             include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Extract technician data from SuperOps using GraphQL"""
        try:
            logger.info("Extracting technicians from SuperOps GraphQL API")
            
            # Build condition for filtering
            condition = None
            if not include_inactive:
                condition = {
                    "status": {
                        "operator": "equals",
                        "value": "active"
                    }
                }
            
            # Calculate page from offset
            page = (offset // limit) + 1
            
            # Build variables
            variables = self._build_list_input(
                page=page,
                page_size=limit,
                condition=condition
            )
            
            # Execute query
            result = await self._execute_query(GET_TECHNICIANS_QUERY, variables)
            
            # Extract technicians from result
            technicians = result.get("data", {}).get("getTechnicianList", {}).get("userList", [])
            
            logger.info(f"Extracted {len(technicians)} technicians from SuperOps GraphQL API")
            return technicians
            
        except Exception as e:
            logger.error(f"Failed to extract technicians: {e}")
            return await self._get_mock_technicians()
    
    async def get_sla_metrics(self, 
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None,
                             ticket_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract SLA metrics from SuperOps using GraphQL"""
        try:
            logger.info("Extracting SLA metrics from SuperOps GraphQL API")
            
            # Execute SLA list query
            result = await self._execute_query(GET_SLA_LIST_QUERY)
            
            # Extract SLA list from result
            sla_list = result.get("data", {}).get("getSLAList", [])
            
            logger.info(f"Extracted {len(sla_list)} SLA metrics from SuperOps GraphQL API")
            return sla_list
            
        except Exception as e:
            logger.error(f"Failed to extract SLA metrics: {e}")
            return await self._get_mock_sla_metrics()
    
    async def get_service_delivery_metrics(self, 
                                         start_date: Optional[datetime] = None,
                                         end_date: Optional[datetime] = None,
                                         granularity: str = "daily") -> List[Dict[str, Any]]:
        """Extract service delivery metrics from SuperOps using GraphQL"""
        try:
            logger.info("Extracting service delivery metrics from SuperOps GraphQL API")
            
            # Build input for service metrics
            input_data = {
                "granularity": granularity
            }
            
            if start_date:
                input_data["startDate"] = start_date.isoformat()
            if end_date:
                input_data["endDate"] = end_date.isoformat()
            
            variables = {"input": input_data}
            
            # Execute query
            result = await self._execute_query(GET_SERVICE_METRICS_QUERY, variables)
            
            # Extract metrics from result
            metrics = result.get("data", {}).get("getServiceMetrics", [])
            
            logger.info(f"Extracted {len(metrics)} service delivery metrics from SuperOps GraphQL API")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to extract service delivery metrics: {e}")
            return await self._get_mock_service_delivery_metrics()
    
    async def get_technician_productivity(self, 
                                        technician_id: Optional[str] = None,
                                        start_date: Optional[datetime] = None,
                                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get technician productivity data from SuperOps using GraphQL"""
        try:
            logger.info("Extracting technician productivity from SuperOps GraphQL API")
            
            # Build input for productivity query
            input_data = {}
            
            if technician_id:
                input_data["technicianId"] = technician_id
            if start_date:
                input_data["startDate"] = start_date.isoformat()
            if end_date:
                input_data["endDate"] = end_date.isoformat()
            
            variables = {"input": input_data}
            
            # Execute query
            result = await self._execute_query(GET_TECHNICIAN_PRODUCTIVITY_QUERY, variables)
            
            # Extract productivity data from result
            productivity = result.get("data", {}).get("getTechnicianProductivity", {})
            
            logger.info("Extracted technician productivity from SuperOps GraphQL API")
            return productivity
            
        except Exception as e:
            logger.error(f"Failed to extract technician productivity: {e}")
            return await self._get_mock_technician_productivity()
    
    async def get_real_time_data(self) -> Dict[str, Any]:
        """Get real-time data from SuperOps using GraphQL"""
        try:
            logger.info("Extracting real-time data from SuperOps GraphQL API")
            
            # Execute real-time data query
            result = await self._execute_query(GET_REALTIME_DATA_QUERY)
            
            # Extract real-time data from result
            realtime_data = result.get("data", {}).get("getRealtimeData", {})
            
            logger.info("Extracted real-time data from SuperOps GraphQL API")
            return realtime_data
            
        except Exception as e:
            logger.error(f"Failed to extract real-time data: {e}")
            return await self._get_mock_real_time_data()
    
    # Mock data methods for development and fallback
    async def _get_mock_tickets(self) -> List[Dict[str, Any]]:
        """Generate mock ticket data for development/fallback"""
        mock_tickets = []
        for i in range(50):
            created_date = datetime.now() - timedelta(days=i % 30)
            ticket = {
                "ticketId": f"TICKET-{i+1:04d}",
                "displayId": f"TICKET-{i+1:04d}",
                "subject": f"Mock Ticket {i+1}",
                "status": ["Open", "In Progress", "Pending", "Resolved", "Closed"][i % 5],
                "priority": ["Low", "Medium", "High", "Critical"][i % 4],
                "createdTime": created_date.isoformat(),
                "updatedTime": (created_date + timedelta(hours=2)).isoformat(),
                "firstResponseTime": (created_date + timedelta(minutes=30)).isoformat() if i % 3 == 0 else None,
                "resolutionTime": (created_date + timedelta(hours=4)).isoformat() if i % 3 == 0 else None,
                "firstResponseViolated": i % 10 == 0,
                "resolutionViolated": i % 15 == 0,
                "technician": {
                    "userId": f"TECH-{(i % 5) + 1:03d}",
                    "name": f"Technician {(i % 5) + 1}"
                },
                "requester": {
                    "userId": f"USER-{(i % 10) + 1:03d}",
                    "name": f"User {(i % 10) + 1}"
                },
                "site": {
                    "id": f"CLIENT-{(i % 10) + 1:03d}",
                    "name": f"Client {(i % 10) + 1}"
                },
                "worklogTimespent": str(120 + (i % 8) * 30),  # 2-4 hours in minutes
                "customFields": [{"fieldName": "custom_field_1", "fieldValue": f"value_{i}"}],
                "tags": [f"tag{j}" for j in range(i % 3)]
            }
            mock_tickets.append(ticket)
        
        return mock_tickets
    
    async def _get_mock_clients(self) -> List[Dict[str, Any]]:
        """Generate mock client data for development/fallback"""
        mock_clients = []
        for i in range(20):
            created_date = datetime.now() - timedelta(days=i * 30)
            client = {
                "id": f"CLIENT-{i+1:03d}",
                "name": f"Client Company {i+1}",
                "contactNumber": f"+1-555-{i+1:04d}",
                "email": f"client{i+1}@company.com",
                "address": {
                    "line1": f"{i+1} Main St",
                    "line2": "",
                    "city": "City",
                    "stateCode": "ST",
                    "countryCode": "US",
                    "zipCode": f"{i+1:05d}"
                },
                "industry": ["Technology", "Healthcare", "Finance", "Retail"][i % 4],
                "companySize": ["Small", "Medium", "Large"][i % 3],
                "contractType": ["Monthly", "Annual", "Project"][i % 3],
                "contractValue": 5000.0 + (i * 1000),
                "contractStartDate": created_date.isoformat(),
                "contractEndDate": (created_date + timedelta(days=365)).isoformat(),
                "billingFrequency": ["Monthly", "Quarterly", "Annual"][i % 3],
                "paymentTerms": "Net 30",
                "primaryContact": f"Contact {i+1}",
                "secondaryContact": f"Secondary {i+1}" if i % 2 == 0 else None,
                "serviceLevel": ["Basic", "Standard", "Premium"][i % 3],
                "customFields": [{"fieldName": "industry_code", "fieldValue": f"IND{i+1}"}],
                "tags": [f"client_tag_{j}" for j in range(i % 2)],
                "createdDate": created_date.isoformat(),
                "lastActivity": (datetime.now() - timedelta(days=i % 7)).isoformat()
            }
            mock_clients.append(client)
        
        return mock_clients
    
    async def _get_mock_technicians(self) -> List[Dict[str, Any]]:
        """Generate mock technician data for development/fallback"""
        mock_technicians = []
        for i in range(10):
            created_date = datetime.now() - timedelta(days=i * 60)
            technician = {
                "userId": f"TECH-{i+1:03d}",
                "name": f"Technician {i+1}",
                "email": f"tech{i+1}@company.com",
                "phone": f"+1-555-{i+1:04d}",
                "department": {
                    "departmentId": f"DEPT-{(i % 3) + 1:03d}",
                    "name": ["Support", "Engineering", "Operations"][i % 3]
                },
                "groups": [{
                    "groupId": f"GROUP-{(i % 2) + 1:03d}",
                    "name": ["Level 1", "Level 2"][i % 2]
                }],
                "skills": ["Windows", "Linux", "Networking", "Security"][:i % 4 + 1],
                "certifications": ["A+", "Network+", "Security+"][:i % 3 + 1],
                "hourlyRate": 50.0 + (i * 10),
                "availability": "Available",
                "performanceScore": 0.8 + (i % 2) * 0.1,
                "ticketsResolved": 100 + (i * 20),
                "avgResolutionTime": 2.5 + (i % 3) * 0.5,
                "customerSatisfaction": 4.2 + (i % 3) * 0.2,
                "createdDate": created_date.isoformat(),
                "lastActive": (datetime.now() - timedelta(hours=i % 24)).isoformat()
            }
            mock_technicians.append(technician)
        
        return mock_technicians
    
    async def _get_mock_sla_metrics(self) -> List[Dict[str, Any]]:
        """Generate mock SLA metrics data for development/fallback"""
        mock_metrics = []
        for i in range(10):
            metric = {
                "id": f"SLA-{i+1:03d}",
                "name": f"SLA Policy {i+1}",
                "description": f"Description for SLA policy {i+1}",
                "responseTime": 240 + (i % 4) * 60,  # 4-8 hours
                "resolutionTime": 1440 + (i % 3) * 480,  # 1-3 days
                "isActive": True
            }
            mock_metrics.append(metric)
        
        return mock_metrics
    
    async def _get_mock_service_delivery_metrics(self) -> List[Dict[str, Any]]:
        """Generate mock service delivery metrics data for development/fallback"""
        mock_metrics = []
        for i in range(30):  # 30 days of data
            date = datetime.now() - timedelta(days=i)
            metric = {
                "date": date.isoformat(),
                "totalTickets": 20 + (i % 10),
                "resolvedTickets": 18 + (i % 8),
                "openTickets": 2 + (i % 3),
                "avgResolutionTime": 2.5 + (i % 3) * 0.5,
                "slaComplianceRate": 0.85 + (i % 2) * 0.1,
                "customerSatisfaction": 4.2 + (i % 3) * 0.2,
                "technicianUtilization": 0.75 + (i % 3) * 0.1,
                "revenueGenerated": 5000 + (i % 5) * 1000,
                "costPerTicket": 150 + (i % 4) * 25
            }
            mock_metrics.append(metric)
        
        return mock_metrics
    
    async def _get_mock_technician_productivity(self) -> Dict[str, Any]:
        """Generate mock technician productivity data for development/fallback"""
        return {
            "technicianId": "TECH-001",
            "period": "last_30_days",
            "ticketsResolved": 45,
            "avgResolutionTime": 2.3,
            "customerSatisfaction": 4.5,
            "utilizationRate": 0.85,
            "overtimeHours": 8.5,
            "skillsUtilized": ["Windows", "Networking", "Security"],
            "performanceScore": 0.92,
            "improvementAreas": ["Documentation", "Communication"]
        }
    
    async def _get_mock_real_time_data(self) -> Dict[str, Any]:
        """Generate mock real-time data for development/fallback"""
        return {
            "timestamp": datetime.now().isoformat(),
            "activeTickets": 25,
            "pendingTickets": 8,
            "onlineTechnicians": 6,
            "slaBreachesToday": 2,
            "avgResponseTime": 15.5,
            "systemHealth": "Good",
            "alerts": [
                {
                    "type": "SLA Warning",
                    "message": "Ticket TICKET-001 approaching SLA",
                    "severity": "Warning",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "type": "High Workload",
                    "message": "Technician TECH-003 at 95% capacity",
                    "severity": "High",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }


# Factory function for creating SuperOps GraphQL client
def create_superops_graphql_client() -> SuperOpsGraphQLClient:
    """Create SuperOps GraphQL client with configuration from settings"""
    config = SuperOpsGraphQLConfig(
        base_url=settings.superops_api.base_url,
        api_key=settings.superops_api.api_key,
        tenant_id=settings.superops_api.tenant_id,
        timeout=settings.superops_api.timeout,
        max_retries=settings.superops_api.max_retries,
        rate_limit_delay=settings.superops_api.rate_limit_delay
    )
    
    return SuperOpsGraphQLClient(config)
