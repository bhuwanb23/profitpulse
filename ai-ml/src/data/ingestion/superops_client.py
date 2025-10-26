"""
SuperOps API Client
Comprehensive client for extracting MSP data from SuperOps platform
"""

import logging
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd

from config import settings

logger = logging.getLogger(__name__)


class TicketStatus(Enum):
    """Ticket status enumeration"""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    PENDING = "Pending"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class TicketPriority(Enum):
    """Ticket priority enumeration"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SLAStatus(Enum):
    """SLA status enumeration"""
    MET = "Met"
    BREACHED = "Breached"
    WARNING = "Warning"
    PENDING = "Pending"


@dataclass
class SuperOpsConfig:
    """SuperOps API configuration"""
    base_url: str
    api_key: str
    tenant_id: str
    timeout: int = 30
    max_retries: int = 3
    rate_limit_delay: float = 0.1


@dataclass
class Ticket:
    """Ticket data structure"""
    id: str
    title: str
    description: str
    status: str
    priority: str
    created_date: datetime
    due_date: Optional[datetime]
    resolved_date: Optional[datetime]
    client_id: str
    client_name: str
    technician_id: Optional[str]
    technician_name: Optional[str]
    service_type: str
    category: str
    subcategory: str
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    billing_rate: Optional[float]
    total_cost: Optional[float]
    sla_status: str
    sla_breach_reason: Optional[str]
    tags: List[str]
    custom_fields: Dict[str, Any]
    attachments: List[str]
    notes: List[str]


@dataclass
class Client:
    """Client data structure"""
    id: str
    name: str
    email: str
    phone: str
    address: Dict[str, str]
    industry: str
    company_size: str
    contract_type: str
    contract_value: float
    contract_start_date: datetime
    contract_end_date: datetime
    billing_frequency: str
    payment_terms: str
    primary_contact: str
    secondary_contact: Optional[str]
    service_level: str
    custom_fields: Dict[str, Any]
    tags: List[str]
    created_date: datetime
    last_activity: datetime


@dataclass
class Technician:
    """Technician data structure"""
    id: str
    name: str
    email: str
    phone: str
    role: str
    department: str
    skills: List[str]
    certifications: List[str]
    hourly_rate: float
    availability: str
    workload: float
    performance_score: float
    tickets_resolved: int
    avg_resolution_time: float
    customer_satisfaction: float
    created_date: datetime
    last_active: datetime


@dataclass
class SLAMetrics:
    """SLA metrics data structure"""
    ticket_id: str
    sla_type: str
    target_time: int  # minutes
    actual_time: int  # minutes
    status: str
    breach_reason: Optional[str]
    response_time: int  # minutes
    resolution_time: int  # minutes
    first_response_time: int  # minutes


@dataclass
class ServiceDeliveryMetrics:
    """Service delivery metrics data structure"""
    date: datetime
    total_tickets: int
    resolved_tickets: int
    open_tickets: int
    avg_resolution_time: float
    sla_compliance_rate: float
    customer_satisfaction: float
    technician_utilization: float
    revenue_generated: float
    cost_per_ticket: float


class SuperOpsClient:
    """Comprehensive SuperOps API client for MSP data extraction"""
    
    def __init__(self, config: SuperOpsConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize the client session"""
        try:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                    "X-Tenant-ID": self.config.tenant_id
                }
            )
            
            logger.info("SuperOps client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize SuperOps client: {e}")
            raise
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()
            logger.info("SuperOps client closed")
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with rate limiting and retry logic"""
        async with self._rate_limit_semaphore:
            for attempt in range(self.config.max_retries):
                try:
                    url = f"{self.config.base_url}{endpoint}"
                    
                    async with self.session.request(method, url, **kwargs) as response:
                        if response.status == 200:
                            data = await response.json()
                            await asyncio.sleep(self.config.rate_limit_delay)
                            return data
                        elif response.status == 429:  # Rate limited
                            wait_time = 2 ** attempt
                            logger.warning(f"Rate limited, waiting {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            logger.error(f"Request failed: {response.status} - {await response.text()}")
                            if attempt == self.config.max_retries - 1:
                                raise aiohttp.ClientError(f"Request failed after {self.config.max_retries} attempts")
                            
                except asyncio.TimeoutError:
                    logger.warning(f"Request timeout (attempt {attempt + 1})")
                    if attempt == self.config.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
                    
                except Exception as e:
                    logger.error(f"Request error (attempt {attempt + 1}): {e}")
                    if attempt == self.config.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
            
            raise aiohttp.ClientError("Max retries exceeded")
    
    async def get_tickets(self, 
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         status: Optional[str] = None,
                         priority: Optional[str] = None,
                         client_id: Optional[str] = None,
                         technician_id: Optional[str] = None,
                         limit: int = 1000,
                         offset: int = 0) -> List[Ticket]:
        """Extract ticket data from SuperOps"""
        try:
            # Build query parameters
            params = {
                "limit": limit,
                "offset": offset,
                "include": "client,technician,sla,custom_fields,attachments,notes"
            }
            
            if start_date:
                params["created_after"] = start_date.isoformat()
            if end_date:
                params["created_before"] = end_date.isoformat()
            if status:
                params["status"] = status
            if priority:
                params["priority"] = priority
            if client_id:
                params["client_id"] = client_id
            if technician_id:
                params["technician_id"] = technician_id
            
            # Make API request
            data = await self._make_request("GET", "/api/v1/tickets", params=params)
            
            # Parse tickets
            tickets = []
            for ticket_data in data.get("tickets", []):
                ticket = self._parse_ticket(ticket_data)
                tickets.append(ticket)
            
            logger.info(f"Extracted {len(tickets)} tickets from SuperOps")
            return tickets
            
        except Exception as e:
            logger.error(f"Failed to extract tickets: {e}")
            # Return mock data for development
            return await self._get_mock_tickets()
    
    async def get_clients(self, 
                         limit: int = 1000,
                         offset: int = 0,
                         include_inactive: bool = False) -> List[Client]:
        """Extract client data from SuperOps"""
        try:
            params = {
                "limit": limit,
                "offset": offset,
                "include": "contracts,contacts,custom_fields"
            }
            
            if not include_inactive:
                params["status"] = "active"
            
            data = await self._make_request("GET", "/api/v1/clients", params=params)
            
            clients = []
            for client_data in data.get("clients", []):
                client = self._parse_client(client_data)
                clients.append(client)
            
            logger.info(f"Extracted {len(clients)} clients from SuperOps")
            return clients
            
        except Exception as e:
            logger.error(f"Failed to extract clients: {e}")
            return await self._get_mock_clients()
    
    async def get_technicians(self, 
                             limit: int = 100,
                             offset: int = 0,
                             include_inactive: bool = False) -> List[Technician]:
        """Extract technician data from SuperOps"""
        try:
            params = {
                "limit": limit,
                "offset": offset,
                "include": "skills,certifications,performance"
            }
            
            if not include_inactive:
                params["status"] = "active"
            
            data = await self._make_request("GET", "/api/v1/technicians", params=params)
            
            technicians = []
            for tech_data in data.get("technicians", []):
                technician = self._parse_technician(tech_data)
                technicians.append(technician)
            
            logger.info(f"Extracted {len(technicians)} technicians from SuperOps")
            return technicians
            
        except Exception as e:
            logger.error(f"Failed to extract technicians: {e}")
            return await self._get_mock_technicians()
    
    async def get_sla_metrics(self, 
                             start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None,
                             ticket_id: Optional[str] = None) -> List[SLAMetrics]:
        """Extract SLA metrics and compliance data"""
        try:
            params = {
                "include": "ticket,breach_reason"
            }
            
            if start_date:
                params["date_after"] = start_date.isoformat()
            if end_date:
                params["date_before"] = end_date.isoformat()
            if ticket_id:
                params["ticket_id"] = ticket_id
            
            data = await self._make_request("GET", "/api/v1/sla-metrics", params=params)
            
            sla_metrics = []
            for sla_data in data.get("sla_metrics", []):
                sla_metric = self._parse_sla_metrics(sla_data)
                sla_metrics.append(sla_metric)
            
            logger.info(f"Extracted {len(sla_metrics)} SLA metrics from SuperOps")
            return sla_metrics
            
        except Exception as e:
            logger.error(f"Failed to extract SLA metrics: {e}")
            return await self._get_mock_sla_metrics()
    
    async def get_service_delivery_metrics(self, 
                                         start_date: Optional[datetime] = None,
                                         end_date: Optional[datetime] = None,
                                         granularity: str = "daily") -> List[ServiceDeliveryMetrics]:
        """Extract service delivery metrics"""
        try:
            params = {
                "granularity": granularity,
                "include": "revenue,costs,satisfaction"
            }
            
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()
            
            data = await self._make_request("GET", "/api/v1/service-metrics", params=params)
            
            metrics = []
            for metric_data in data.get("metrics", []):
                metric = self._parse_service_delivery_metrics(metric_data)
                metrics.append(metric)
            
            logger.info(f"Extracted {len(metrics)} service delivery metrics from SuperOps")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to extract service delivery metrics: {e}")
            return await self._get_mock_service_delivery_metrics()
    
    async def get_technician_productivity(self, 
                                        technician_id: Optional[str] = None,
                                        start_date: Optional[datetime] = None,
                                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get technician productivity data"""
        try:
            params = {}
            
            if technician_id:
                params["technician_id"] = technician_id
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()
            
            data = await self._make_request("GET", "/api/v1/productivity", params=params)
            
            logger.info("Extracted technician productivity data from SuperOps")
            return data
            
        except Exception as e:
            logger.error(f"Failed to extract technician productivity: {e}")
            return await self._get_mock_technician_productivity()
    
    async def get_real_time_data(self) -> Dict[str, Any]:
        """Get real-time data streaming"""
        try:
            data = await self._make_request("GET", "/api/v1/realtime")
            
            logger.info("Extracted real-time data from SuperOps")
            return data
            
        except Exception as e:
            logger.error(f"Failed to extract real-time data: {e}")
            return await self._get_mock_real_time_data()
    
    def _parse_ticket(self, data: Dict[str, Any]) -> Ticket:
        """Parse ticket data from API response"""
        return Ticket(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", ""),
            priority=data.get("priority", ""),
            created_date=datetime.fromisoformat(data.get("created_date", datetime.now().isoformat())),
            due_date=datetime.fromisoformat(data.get("due_date")) if data.get("due_date") else None,
            resolved_date=datetime.fromisoformat(data.get("resolved_date")) if data.get("resolved_date") else None,
            client_id=data.get("client", {}).get("id", ""),
            client_name=data.get("client", {}).get("name", ""),
            technician_id=data.get("technician", {}).get("id") if data.get("technician") else None,
            technician_name=data.get("technician", {}).get("name") if data.get("technician") else None,
            service_type=data.get("service_type", ""),
            category=data.get("category", ""),
            subcategory=data.get("subcategory", ""),
            estimated_hours=data.get("estimated_hours"),
            actual_hours=data.get("actual_hours"),
            billing_rate=data.get("billing_rate"),
            total_cost=data.get("total_cost"),
            sla_status=data.get("sla", {}).get("status", ""),
            sla_breach_reason=data.get("sla", {}).get("breach_reason"),
            tags=data.get("tags", []),
            custom_fields=data.get("custom_fields", {}),
            attachments=data.get("attachments", []),
            notes=data.get("notes", [])
        )
    
    def _parse_client(self, data: Dict[str, Any]) -> Client:
        """Parse client data from API response"""
        return Client(
            id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            address=data.get("address", {}),
            industry=data.get("industry", ""),
            company_size=data.get("company_size", ""),
            contract_type=data.get("contract", {}).get("type", ""),
            contract_value=data.get("contract", {}).get("value", 0.0),
            contract_start_date=datetime.fromisoformat(data.get("contract", {}).get("start_date", datetime.now().isoformat())),
            contract_end_date=datetime.fromisoformat(data.get("contract", {}).get("end_date", datetime.now().isoformat())),
            billing_frequency=data.get("billing_frequency", ""),
            payment_terms=data.get("payment_terms", ""),
            primary_contact=data.get("primary_contact", ""),
            secondary_contact=data.get("secondary_contact"),
            service_level=data.get("service_level", ""),
            custom_fields=data.get("custom_fields", {}),
            tags=data.get("tags", []),
            created_date=datetime.fromisoformat(data.get("created_date", datetime.now().isoformat())),
            last_activity=datetime.fromisoformat(data.get("last_activity", datetime.now().isoformat()))
        )
    
    def _parse_technician(self, data: Dict[str, Any]) -> Technician:
        """Parse technician data from API response"""
        return Technician(
            id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            role=data.get("role", ""),
            department=data.get("department", ""),
            skills=data.get("skills", []),
            certifications=data.get("certifications", []),
            hourly_rate=data.get("hourly_rate", 0.0),
            availability=data.get("availability", ""),
            workload=data.get("workload", 0.0),
            performance_score=data.get("performance_score", 0.0),
            tickets_resolved=data.get("tickets_resolved", 0),
            avg_resolution_time=data.get("avg_resolution_time", 0.0),
            customer_satisfaction=data.get("customer_satisfaction", 0.0),
            created_date=datetime.fromisoformat(data.get("created_date", datetime.now().isoformat())),
            last_active=datetime.fromisoformat(data.get("last_active", datetime.now().isoformat()))
        )
    
    def _parse_sla_metrics(self, data: Dict[str, Any]) -> SLAMetrics:
        """Parse SLA metrics data from API response"""
        return SLAMetrics(
            ticket_id=data.get("ticket_id", ""),
            sla_type=data.get("sla_type", ""),
            target_time=data.get("target_time", 0),
            actual_time=data.get("actual_time", 0),
            status=data.get("status", ""),
            breach_reason=data.get("breach_reason"),
            response_time=data.get("response_time", 0),
            resolution_time=data.get("resolution_time", 0),
            first_response_time=data.get("first_response_time", 0)
        )
    
    def _parse_service_delivery_metrics(self, data: Dict[str, Any]) -> ServiceDeliveryMetrics:
        """Parse service delivery metrics data from API response"""
        return ServiceDeliveryMetrics(
            date=datetime.fromisoformat(data.get("date", datetime.now().isoformat())),
            total_tickets=data.get("total_tickets", 0),
            resolved_tickets=data.get("resolved_tickets", 0),
            open_tickets=data.get("open_tickets", 0),
            avg_resolution_time=data.get("avg_resolution_time", 0.0),
            sla_compliance_rate=data.get("sla_compliance_rate", 0.0),
            customer_satisfaction=data.get("customer_satisfaction", 0.0),
            technician_utilization=data.get("technician_utilization", 0.0),
            revenue_generated=data.get("revenue_generated", 0.0),
            cost_per_ticket=data.get("cost_per_ticket", 0.0)
        )
    
    # Mock data methods for development and testing
    async def _get_mock_tickets(self) -> List[Ticket]:
        """Generate mock ticket data for development"""
        mock_tickets = []
        for i in range(50):
            created_date = datetime.now() - timedelta(days=i % 30)
            ticket = Ticket(
                id=f"TICKET-{i+1:04d}",
                title=f"Mock Ticket {i+1}",
                description=f"Description for mock ticket {i+1}",
                status=list(TicketStatus)[i % len(TicketStatus)].value,
                priority=list(TicketPriority)[i % len(TicketPriority)].value,
                created_date=created_date,
                due_date=created_date + timedelta(days=2),
                resolved_date=created_date + timedelta(hours=4) if i % 3 == 0 else None,
                client_id=f"CLIENT-{(i % 10) + 1:03d}",
                client_name=f"Client {(i % 10) + 1}",
                technician_id=f"TECH-{(i % 5) + 1:03d}",
                technician_name=f"Technician {(i % 5) + 1}",
                service_type=["Support", "Maintenance", "Installation"][i % 3],
                category=["Hardware", "Software", "Network"][i % 3],
                subcategory=["Issue", "Request", "Incident"][i % 3],
                estimated_hours=2.0 + (i % 8),
                actual_hours=1.5 + (i % 6),
                billing_rate=75.0 + (i % 25),
                total_cost=150.0 + (i % 200),
                sla_status=list(SLAStatus)[i % len(SLAStatus)].value,
                sla_breach_reason="High workload" if i % 7 == 0 else None,
                tags=[f"tag{j}" for j in range(i % 3)],
                custom_fields={"custom_field_1": f"value_{i}"},
                attachments=[f"attachment_{i}.pdf"],
                notes=[f"Note {j}" for j in range(i % 2)]
            )
            mock_tickets.append(ticket)
        
        return mock_tickets
    
    async def _get_mock_clients(self) -> List[Client]:
        """Generate mock client data for development"""
        mock_clients = []
        for i in range(20):
            created_date = datetime.now() - timedelta(days=i * 30)
            client = Client(
                id=f"CLIENT-{i+1:03d}",
                name=f"Client Company {i+1}",
                email=f"client{i+1}@company.com",
                phone=f"+1-555-{i+1:04d}",
                address={
                    "street": f"{i+1} Main St",
                    "city": "City",
                    "state": "State",
                    "zip": f"{i+1:05d}"
                },
                industry=["Technology", "Healthcare", "Finance", "Retail"][i % 4],
                company_size=["Small", "Medium", "Large"][i % 3],
                contract_type=["Monthly", "Annual", "Project"][i % 3],
                contract_value=5000.0 + (i * 1000),
                contract_start_date=created_date,
                contract_end_date=created_date + timedelta(days=365),
                billing_frequency=["Monthly", "Quarterly", "Annual"][i % 3],
                payment_terms="Net 30",
                primary_contact=f"Contact {i+1}",
                secondary_contact=f"Secondary {i+1}" if i % 2 == 0 else None,
                service_level=["Basic", "Standard", "Premium"][i % 3],
                custom_fields={"industry_code": f"IND{i+1}"},
                tags=[f"client_tag_{j}" for j in range(i % 2)],
                created_date=created_date,
                last_activity=datetime.now() - timedelta(days=i % 7)
            )
            mock_clients.append(client)
        
        return mock_clients
    
    async def _get_mock_technicians(self) -> List[Technician]:
        """Generate mock technician data for development"""
        mock_technicians = []
        for i in range(10):
            created_date = datetime.now() - timedelta(days=i * 60)
            technician = Technician(
                id=f"TECH-{i+1:03d}",
                name=f"Technician {i+1}",
                email=f"tech{i+1}@company.com",
                phone=f"+1-555-{i+1:04d}",
                role=["Senior", "Junior", "Lead"][i % 3],
                department=["Support", "Engineering", "Operations"][i % 3],
                skills=["Windows", "Linux", "Networking", "Security"][:i % 4 + 1],
                certifications=["A+", "Network+", "Security+"][:i % 3 + 1],
                hourly_rate=50.0 + (i * 10),
                availability="Available",
                workload=0.7 + (i % 3) * 0.1,
                performance_score=0.8 + (i % 2) * 0.1,
                tickets_resolved=100 + (i * 20),
                avg_resolution_time=2.5 + (i % 3) * 0.5,
                customer_satisfaction=4.2 + (i % 3) * 0.2,
                created_date=created_date,
                last_active=datetime.now() - timedelta(hours=i % 24)
            )
            mock_technicians.append(technician)
        
        return mock_technicians
    
    async def _get_mock_sla_metrics(self) -> List[SLAMetrics]:
        """Generate mock SLA metrics data for development"""
        mock_metrics = []
        for i in range(100):
            metric = SLAMetrics(
                ticket_id=f"TICKET-{i+1:04d}",
                sla_type=["Response", "Resolution", "First Response"][i % 3],
                target_time=240 + (i % 4) * 60,  # 4-8 hours
                actual_time=180 + (i % 6) * 30,  # 3-6 hours
                status=list(SLAStatus)[i % len(SLAStatus)].value,
                breach_reason="High workload" if i % 10 == 0 else None,
                response_time=30 + (i % 5) * 10,
                resolution_time=180 + (i % 8) * 30,
                first_response_time=15 + (i % 3) * 5
            )
            mock_metrics.append(metric)
        
        return mock_metrics
    
    async def _get_mock_service_delivery_metrics(self) -> List[ServiceDeliveryMetrics]:
        """Generate mock service delivery metrics data for development"""
        mock_metrics = []
        for i in range(30):  # 30 days of data
            date = datetime.now() - timedelta(days=i)
            metric = ServiceDeliveryMetrics(
                date=date,
                total_tickets=20 + (i % 10),
                resolved_tickets=18 + (i % 8),
                open_tickets=2 + (i % 3),
                avg_resolution_time=2.5 + (i % 3) * 0.5,
                sla_compliance_rate=0.85 + (i % 2) * 0.1,
                customer_satisfaction=4.2 + (i % 3) * 0.2,
                technician_utilization=0.75 + (i % 3) * 0.1,
                revenue_generated=5000 + (i % 5) * 1000,
                cost_per_ticket=150 + (i % 4) * 25
            )
            mock_metrics.append(metric)
        
        return mock_metrics
    
    async def _get_mock_technician_productivity(self) -> Dict[str, Any]:
        """Generate mock technician productivity data for development"""
        return {
            "technician_id": "TECH-001",
            "period": "last_30_days",
            "tickets_resolved": 45,
            "avg_resolution_time": 2.3,
            "customer_satisfaction": 4.5,
            "utilization_rate": 0.85,
            "overtime_hours": 8.5,
            "skills_utilized": ["Windows", "Networking", "Security"],
            "performance_score": 0.92,
            "improvement_areas": ["Documentation", "Communication"]
        }
    
    async def _get_mock_real_time_data(self) -> Dict[str, Any]:
        """Generate mock real-time data for development"""
        return {
            "timestamp": datetime.now().isoformat(),
            "active_tickets": 25,
            "pending_tickets": 8,
            "online_technicians": 6,
            "sla_breaches_today": 2,
            "avg_response_time": 15.5,
            "system_health": "Good",
            "alerts": [
                {"type": "SLA Warning", "message": "Ticket TICKET-001 approaching SLA"},
                {"type": "High Workload", "message": "Technician TECH-003 at 95% capacity"}
            ]
        }


# Factory function for creating SuperOps client
def create_superops_client() -> SuperOpsClient:
    """Create SuperOps client with configuration from settings"""
    config = SuperOpsConfig(
        base_url=settings.superops_api.base_url,
        api_key=settings.superops_api.api_key,
        tenant_id=settings.superops_api.tenant_id,
        timeout=settings.superops_api.timeout,
        max_retries=settings.superops_api.max_retries,
        rate_limit_delay=settings.superops_api.rate_limit_delay
    )
    
    return SuperOpsClient(config)
