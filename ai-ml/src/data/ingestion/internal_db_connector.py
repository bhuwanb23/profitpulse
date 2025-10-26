"""
Internal database connector for client data extraction
Provides access to internal database for client profiles, service history,
satisfaction scores, communication engagement, and contract data.
"""

import asyncio
import aiosqlite
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)


@dataclass
class InternalDBConfig:
    """Configuration for internal database connector"""
    database_path: str
    connection_timeout: int = 30
    max_connections: int = 10
    query_timeout: int = 60


class InternalDBConnector:
    """Asynchronous internal database connector"""
    
    def __init__(self, config: InternalDBConfig):
        self.config = config
        self.connection_pool: List[aiosqlite.Connection] = []
        self._pool_semaphore = asyncio.Semaphore(config.max_connections)
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize the database connection pool"""
        # Ensure database file exists
        db_path = Path(self.config.database_path)
        if not db_path.exists():
            await self._create_database()
        
        # Create connection pool
        for _ in range(self.config.max_connections):
            conn = await aiosqlite.connect(self.config.database_path)
            self.connection_pool.append(conn)
        
        logger.info(f"Internal database connector initialized with {len(self.connection_pool)} connections")
    
    async def close(self):
        """Close all database connections"""
        for conn in self.connection_pool:
            await conn.close()
        self.connection_pool.clear()
        logger.info("Internal database connector closed")
    
    async def _create_database(self):
        """Create database with required tables"""
        db_path = Path(self.config.database_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiosqlite.connect(self.config.database_path) as conn:
            # Create tables
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS client_profiles (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    company_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    industry TEXT,
                    company_size TEXT,
                    annual_revenue REAL,
                    contract_tier TEXT,
                    onboarding_date TEXT,
                    status TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS service_history (
                    id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    service_date TEXT NOT NULL,
                    duration_hours REAL,
                    technician_id TEXT,
                    status TEXT,
                    description TEXT,
                    cost REAL,
                    satisfaction_score REAL,
                    created_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES client_profiles (id)
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS satisfaction_scores (
                    id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    survey_date TEXT NOT NULL,
                    overall_score REAL,
                    service_quality_score REAL,
                    response_time_score REAL,
                    communication_score REAL,
                    value_score REAL,
                    comments TEXT,
                    survey_type TEXT,
                    created_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES client_profiles (id)
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS communication_engagement (
                    id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    communication_type TEXT NOT NULL,
                    communication_date TEXT NOT NULL,
                    subject TEXT,
                    direction TEXT,
                    response_time_hours REAL,
                    satisfaction_rating REAL,
                    follow_up_required BOOLEAN,
                    created_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES client_profiles (id)
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS contracts (
                    id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    contract_type TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    contract_value REAL,
                    payment_terms TEXT,
                    renewal_date TEXT,
                    auto_renewal BOOLEAN,
                    status TEXT,
                    terms TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES client_profiles (id)
                )
            """)
            
            await conn.commit()
            
            # Insert sample data
            await self._insert_sample_data(conn)
            
        logger.info("Database created with sample data")
    
    async def _insert_sample_data(self, conn: aiosqlite.Connection):
        """Insert sample data for testing"""
        # Sample client profiles
        clients = [
            ("CLIENT-001", "Acme Corporation", "Acme Corp", "contact@acme.com", "+1-555-0001", "123 Business St, New York, NY", "Technology", "Large", 10000000.0, "Enterprise", "2023-01-15", "Active"),
            ("CLIENT-002", "TechStart Inc", "TechStart", "info@techstart.com", "+1-555-0002", "456 Innovation Ave, San Francisco, CA", "Technology", "Small", 1000000.0, "Professional", "2023-02-20", "Active"),
            ("CLIENT-003", "Global Services Ltd", "Global Services", "admin@globalservices.com", "+1-555-0003", "789 Corporate Blvd, Chicago, IL", "Services", "Medium", 5000000.0, "Business", "2023-03-10", "Active"),
            ("CLIENT-004", "Local Business Co", "Local Business", "owner@localbiz.com", "+1-555-0004", "321 Main St, Austin, TX", "Retail", "Small", 500000.0, "Standard", "2023-04-05", "Active"),
            ("CLIENT-005", "Enterprise Solutions", "Enterprise Solutions", "contact@enterprise.com", "+1-555-0005", "654 Enterprise Way, Boston, MA", "Technology", "Large", 15000000.0, "Enterprise", "2023-05-12", "Active")
        ]
        
        for client in clients:
            await conn.execute("""
                INSERT OR REPLACE INTO client_profiles 
                (id, name, company_name, email, phone, address, industry, company_size, annual_revenue, contract_tier, onboarding_date, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, client + (datetime.now().isoformat(), datetime.now().isoformat()))
        
        # Sample service history
        services = [
            ("SVC-001", "CLIENT-001", "IT Support", "2023-06-01", 8.0, "TECH-001", "Completed", "Monthly IT maintenance", 2000.0, 4.5),
            ("SVC-002", "CLIENT-002", "Software Installation", "2023-06-02", 4.0, "TECH-002", "Completed", "CRM software setup", 1500.0, 4.8),
            ("SVC-003", "CLIENT-003", "Network Setup", "2023-06-03", 12.0, "TECH-001", "Completed", "Office network configuration", 3000.0, 4.2),
            ("SVC-004", "CLIENT-004", "Hardware Repair", "2023-06-04", 2.0, "TECH-003", "Completed", "Server hardware repair", 800.0, 4.7),
            ("SVC-005", "CLIENT-005", "Security Audit", "2023-06-05", 16.0, "TECH-004", "Completed", "Comprehensive security assessment", 5000.0, 4.9)
        ]
        
        for service in services:
            await conn.execute("""
                INSERT OR REPLACE INTO service_history 
                (id, client_id, service_type, service_date, duration_hours, technician_id, status, description, cost, satisfaction_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, service + (datetime.now().isoformat(),))
        
        # Sample satisfaction scores
        satisfaction = [
            ("SAT-001", "CLIENT-001", "2023-06-01", 4.5, 4.6, 4.4, 4.5, 4.5, "Excellent service as always", "Quarterly"),
            ("SAT-002", "CLIENT-002", "2023-06-02", 4.8, 4.9, 4.7, 4.8, 4.8, "Very satisfied with the support", "Monthly"),
            ("SAT-003", "CLIENT-003", "2023-06-03", 4.2, 4.3, 4.1, 4.2, 4.2, "Good service, minor delays", "Quarterly"),
            ("SAT-004", "CLIENT-004", "2023-06-04", 4.7, 4.8, 4.6, 4.7, 4.7, "Quick response and resolution", "Monthly"),
            ("SAT-005", "CLIENT-005", "2023-06-05", 4.9, 5.0, 4.8, 4.9, 4.9, "Outstanding service quality", "Quarterly")
        ]
        
        for sat in satisfaction:
            await conn.execute("""
                INSERT OR REPLACE INTO satisfaction_scores 
                (id, client_id, survey_date, overall_score, service_quality_score, response_time_score, communication_score, value_score, comments, survey_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sat + (datetime.now().isoformat(),))
        
        # Sample communication engagement
        communications = [
            ("COMM-001", "CLIENT-001", "Email", "2023-06-01", "Monthly Report", "Outbound", 0.5, 4.5, False),
            ("COMM-002", "CLIENT-002", "Phone", "2023-06-02", "Support Request", "Inbound", 2.0, 4.8, True),
            ("COMM-003", "CLIENT-003", "Meeting", "2023-06-03", "Quarterly Review", "Outbound", 1.0, 4.2, False),
            ("COMM-004", "CLIENT-004", "Email", "2023-06-04", "Invoice Question", "Inbound", 4.0, 4.7, False),
            ("COMM-005", "CLIENT-005", "Video Call", "2023-06-05", "Project Update", "Outbound", 0.5, 4.9, False)
        ]
        
        for comm in communications:
            await conn.execute("""
                INSERT OR REPLACE INTO communication_engagement 
                (id, client_id, communication_type, communication_date, subject, direction, response_time_hours, satisfaction_rating, follow_up_required, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, comm + (datetime.now().isoformat(),))
        
        # Sample contracts
        contracts = [
            ("CONTRACT-001", "CLIENT-001", "Enterprise Support", "2023-01-01", "2024-12-31", 120000.0, "Annual", "2024-10-01", True, "Active", "Comprehensive IT support package"),
            ("CONTRACT-002", "CLIENT-002", "Professional Services", "2023-02-01", "2024-01-31", 24000.0, "Monthly", "2023-12-01", False, "Active", "Monthly IT support and maintenance"),
            ("CONTRACT-003", "CLIENT-003", "Business Support", "2023-03-01", "2024-02-29", 60000.0, "Quarterly", "2024-01-01", True, "Active", "Business-level IT services"),
            ("CONTRACT-004", "CLIENT-004", "Standard Support", "2023-04-01", "2024-03-31", 12000.0, "Monthly", "2024-02-01", False, "Active", "Standard IT support package"),
            ("CONTRACT-005", "CLIENT-005", "Enterprise Plus", "2023-05-01", "2025-04-30", 200000.0, "Annual", "2025-02-01", True, "Active", "Premium enterprise support with 24/7 coverage")
        ]
        
        for contract in contracts:
            await conn.execute("""
                INSERT OR REPLACE INTO contracts 
                (id, client_id, contract_type, start_date, end_date, contract_value, payment_terms, renewal_date, auto_renewal, status, terms, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, contract + (datetime.now().isoformat(), datetime.now().isoformat()))
        
        await conn.commit()
    
    async def _get_connection(self) -> aiosqlite.Connection:
        """Get a connection from the pool"""
        async with self._pool_semaphore:
            if self.connection_pool:
                return self.connection_pool.pop()
            else:
                return await aiosqlite.connect(self.config.database_path)
    
    async def _return_connection(self, conn: aiosqlite.Connection):
        """Return a connection to the pool"""
        if len(self.connection_pool) < self.config.max_connections:
            self.connection_pool.append(conn)
        else:
            await conn.close()
    
    async def get_client_profiles(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract client profile data"""
        logger.info("Extracting client profile data")
        
        conn = await self._get_connection()
        try:
            cursor = await conn.execute("""
                SELECT * FROM client_profiles 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            profiles = []
            for row in rows:
                profile = dict(zip(columns, row))
                profiles.append(profile)
            
            logger.info(f"Extracted {len(profiles)} client profiles")
            return profiles
            
        finally:
            await self._return_connection(conn)
    
    async def get_service_history_and_preferences(self, client_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get service history and preferences"""
        logger.info(f"Extracting service history for client: {client_id or 'all'}")
        
        conn = await self._get_connection()
        try:
            if client_id:
                cursor = await conn.execute("""
                    SELECT sh.*, cp.name as client_name, cp.company_name 
                    FROM service_history sh
                    JOIN client_profiles cp ON sh.client_id = cp.id
                    WHERE sh.client_id = ?
                    ORDER BY sh.service_date DESC 
                    LIMIT ?
                """, (client_id, limit))
            else:
                cursor = await conn.execute("""
                    SELECT sh.*, cp.name as client_name, cp.company_name 
                    FROM service_history sh
                    JOIN client_profiles cp ON sh.client_id = cp.id
                    ORDER BY sh.service_date DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            services = []
            for row in rows:
                service = dict(zip(columns, row))
                services.append(service)
            
            logger.info(f"Extracted {len(services)} service history records")
            return services
            
        finally:
            await self._return_connection(conn)
    
    async def get_satisfaction_scores(self, client_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract satisfaction scores"""
        logger.info(f"Extracting satisfaction scores for client: {client_id or 'all'}")
        
        conn = await self._get_connection()
        try:
            if client_id:
                cursor = await conn.execute("""
                    SELECT ss.*, cp.name as client_name, cp.company_name 
                    FROM satisfaction_scores ss
                    JOIN client_profiles cp ON ss.client_id = cp.id
                    WHERE ss.client_id = ?
                    ORDER BY ss.survey_date DESC 
                    LIMIT ?
                """, (client_id, limit))
            else:
                cursor = await conn.execute("""
                    SELECT ss.*, cp.name as client_name, cp.company_name 
                    FROM satisfaction_scores ss
                    JOIN client_profiles cp ON ss.client_id = cp.id
                    ORDER BY ss.survey_date DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            scores = []
            for row in rows:
                score = dict(zip(columns, row))
                scores.append(score)
            
            logger.info(f"Extracted {len(scores)} satisfaction scores")
            return scores
            
        finally:
            await self._return_connection(conn)
    
    async def get_communication_engagement_data(self, client_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get communication engagement data"""
        logger.info(f"Extracting communication engagement data for client: {client_id or 'all'}")
        
        conn = await self._get_connection()
        try:
            if client_id:
                cursor = await conn.execute("""
                    SELECT ce.*, cp.name as client_name, cp.company_name 
                    FROM communication_engagement ce
                    JOIN client_profiles cp ON ce.client_id = cp.id
                    WHERE ce.client_id = ?
                    ORDER BY ce.communication_date DESC 
                    LIMIT ?
                """, (client_id, limit))
            else:
                cursor = await conn.execute("""
                    SELECT ce.*, cp.name as client_name, cp.company_name 
                    FROM communication_engagement ce
                    JOIN client_profiles cp ON ce.client_id = cp.id
                    ORDER BY ce.communication_date DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            communications = []
            for row in rows:
                communication = dict(zip(columns, row))
                communications.append(communication)
            
            logger.info(f"Extracted {len(communications)} communication engagement records")
            return communications
            
        finally:
            await self._return_connection(conn)
    
    async def get_contract_and_renewal_data(self, client_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract contract and renewal data"""
        logger.info(f"Extracting contract and renewal data for client: {client_id or 'all'}")
        
        conn = await self._get_connection()
        try:
            if client_id:
                cursor = await conn.execute("""
                    SELECT c.*, cp.name as client_name, cp.company_name 
                    FROM contracts c
                    JOIN client_profiles cp ON c.client_id = cp.id
                    WHERE c.client_id = ?
                    ORDER BY c.start_date DESC 
                    LIMIT ?
                """, (client_id, limit))
            else:
                cursor = await conn.execute("""
                    SELECT c.*, cp.name as client_name, cp.company_name 
                    FROM contracts c
                    JOIN client_profiles cp ON c.client_id = cp.id
                    ORDER BY c.start_date DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            contracts = []
            for row in rows:
                contract = dict(zip(columns, row))
                contracts.append(contract)
            
            logger.info(f"Extracted {len(contracts)} contract records")
            return contracts
            
        finally:
            await self._return_connection(conn)
    
    async def get_all_internal_data(self, client_id: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get all internal data for a client or all clients"""
        logger.info(f"Extracting all internal data for client: {client_id or 'all'}")
        
        all_data = {}
        
        # Extract all data types
        all_data["client_profiles"] = await self.get_client_profiles(limit=1000)
        all_data["service_history"] = await self.get_service_history_and_preferences(client_id, limit=1000)
        all_data["satisfaction_scores"] = await self.get_satisfaction_scores(client_id, limit=1000)
        all_data["communication_engagement"] = await self.get_communication_engagement_data(client_id, limit=1000)
        all_data["contracts"] = await self.get_contract_and_renewal_data(client_id, limit=1000)
        
        # Add metadata
        all_data["extraction_metadata"] = {
            "extraction_timestamp": datetime.now().isoformat(),
            "client_id": client_id,
            "total_records": sum(len(data) for data in all_data.values() if isinstance(data, list)),
            "data_types": list(all_data.keys())
        }
        
        logger.info(f"Extracted all internal data: {all_data['extraction_metadata']['total_records']} total records")
        return all_data


# Factory function for creating internal database connector
def create_internal_db_connector() -> InternalDBConnector:
    """Create internal database connector with configuration from settings"""
    config = InternalDBConfig(
        database_path=settings.database.url.replace("sqlite:///", ""),
        connection_timeout=30,
        max_connections=10,
        query_timeout=60
    )
    
    return InternalDBConnector(config)
