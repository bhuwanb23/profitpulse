"""
Data Ingestion Module
Handles data extraction from various sources (SuperOps, QuickBooks, Internal DB)
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import httpx
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

from config import settings

logger = logging.getLogger(__name__)


class DataIngestionError(Exception):
    """Custom exception for data ingestion errors"""
    pass


class BaseDataIngestion:
    """Base class for data ingestion from different sources"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.logger = logging.getLogger(f"{__name__}.{source_name}")
    
    async def extract_data(self, **kwargs) -> pd.DataFrame:
        """Extract data from the source"""
        raise NotImplementedError
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate extracted data"""
        if data.empty:
            self.logger.warning(f"No data extracted from {self.source_name}")
            return False
        
        self.logger.info(f"Extracted {len(data)} records from {self.source_name}")
        return True
    
    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data to standard format"""
        # Add common transformations here
        data['extracted_at'] = datetime.utcnow()
        data['source'] = self.source_name
        return data


class SuperOpsIngestion(BaseDataIngestion):
    """SuperOps API data ingestion"""
    
    def __init__(self):
        super().__init__("superops")
        self.api_url = settings.superops.api_url
        self.api_key = settings.superops.api_key
        self.org_id = settings.superops.organization_id
        self.timeout = settings.superops.timeout
        
        if not self.api_key:
            self.logger.warning("SuperOps API key not configured")
    
    async def extract_tickets(self, start_date: Optional[datetime] = None, 
                            end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Extract ticket data from SuperOps"""
        if not self.api_key:
            return pd.DataFrame()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # Mock data for now - replace with actual API calls
                mock_tickets = [
                    {
                        "id": f"SO-{i:06d}",
                        "title": f"Ticket {i}",
                        "status": "Open" if i % 3 == 0 else "Closed",
                        "priority": ["Low", "Medium", "High", "Critical"][i % 4],
                        "created_at": (datetime.now() - timedelta(days=i)).isoformat(),
                        "resolved_at": (datetime.now() - timedelta(days=i-1)).isoformat() if i % 3 != 0 else None,
                        "client_id": f"client_{i % 10}",
                        "technician_id": f"tech_{i % 5}",
                        "service_type": ["Support", "Maintenance", "Installation"][i % 3],
                        "hours_logged": round(2.5 + (i % 3) * 1.5, 2),
                        "billing_amount": round(150 + (i % 5) * 50, 2)
                    }
                    for i in range(1, 101)
                ]
                
                self.logger.info(f"Extracted {len(mock_tickets)} tickets from SuperOps")
                return pd.DataFrame(mock_tickets)
                
        except Exception as e:
            self.logger.error(f"Error extracting tickets from SuperOps: {e}")
            raise DataIngestionError(f"SuperOps ticket extraction failed: {e}")
    
    async def extract_clients(self) -> pd.DataFrame:
        """Extract client data from SuperOps"""
        if not self.api_key:
            return pd.DataFrame()
        
        try:
            # Mock client data
            mock_clients = [
                {
                    "id": f"client_{i}",
                    "name": f"Client Company {i}",
                    "email": f"contact{i}@client{i}.com",
                    "phone": f"+1-555-{i:04d}",
                    "address": f"{i} Business St, City, State {i:05d}",
                    "created_at": (datetime.now() - timedelta(days=i*30)).isoformat(),
                    "status": "Active" if i % 4 != 0 else "Inactive",
                    "contract_value": round(5000 + (i % 10) * 2000, 2),
                    "last_contact": (datetime.now() - timedelta(days=i*7)).isoformat()
                }
                for i in range(1, 21)
            ]
            
            self.logger.info(f"Extracted {len(mock_clients)} clients from SuperOps")
            return pd.DataFrame(mock_clients)
            
        except Exception as e:
            self.logger.error(f"Error extracting clients from SuperOps: {e}")
            raise DataIngestionError(f"SuperOps client extraction failed: {e}")
    
    async def extract_technicians(self) -> pd.DataFrame:
        """Extract technician data from SuperOps"""
        if not self.api_key:
            return pd.DataFrame()
        
        try:
            # Mock technician data
            mock_technicians = [
                {
                    "id": f"tech_{i}",
                    "name": f"Technician {i}",
                    "email": f"tech{i}@superhack.com",
                    "role": ["Senior", "Junior", "Lead"][i % 3],
                    "hourly_rate": round(75 + (i % 3) * 25, 2),
                    "specialization": ["Network", "Security", "Cloud", "General"][i % 4],
                    "active": True,
                    "created_at": (datetime.now() - timedelta(days=i*100)).isoformat()
                }
                for i in range(1, 11)
            ]
            
            self.logger.info(f"Extracted {len(mock_technicians)} technicians from SuperOps")
            return pd.DataFrame(mock_technicians)
            
        except Exception as e:
            self.logger.error(f"Error extracting technicians from SuperOps: {e}")
            raise DataIngestionError(f"SuperOps technician extraction failed: {e}")


class QuickBooksIngestion(BaseDataIngestion):
    """QuickBooks API data ingestion"""
    
    def __init__(self):
        super().__init__("quickbooks")
        self.client_id = settings.quickbooks.client_id
        self.client_secret = settings.quickbooks.client_secret
        self.redirect_uri = settings.quickbooks.redirect_uri
        self.sandbox_url = settings.quickbooks.sandbox_url
        self.production_url = settings.quickbooks.production_url
        self.use_sandbox = settings.quickbooks.use_sandbox
        
        if not self.client_id:
            self.logger.warning("QuickBooks API credentials not configured")
    
    async def extract_invoices(self, start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Extract invoice data from QuickBooks"""
        if not self.client_id:
            return pd.DataFrame()
        
        try:
            # Mock invoice data
            mock_invoices = [
                {
                    "id": f"QB-INV-{i:06d}",
                    "client_id": f"client_{i % 20}",
                    "invoice_number": f"INV-{i:06d}",
                    "amount": round(1000 + (i % 10) * 500, 2),
                    "status": ["Draft", "Sent", "Paid", "Overdue"][i % 4],
                    "created_date": (datetime.now() - timedelta(days=i*7)).isoformat(),
                    "due_date": (datetime.now() - timedelta(days=i*7-30)).isoformat(),
                    "paid_date": (datetime.now() - timedelta(days=i*7-15)).isoformat() if i % 4 == 2 else None,
                    "payment_method": ["Check", "Credit Card", "Bank Transfer", "Cash"][i % 4],
                    "tax_amount": round((1000 + (i % 10) * 500) * 0.08, 2),
                    "total_amount": round((1000 + (i % 10) * 500) * 1.08, 2)
                }
                for i in range(1, 51)
            ]
            
            self.logger.info(f"Extracted {len(mock_invoices)} invoices from QuickBooks")
            return pd.DataFrame(mock_invoices)
            
        except Exception as e:
            self.logger.error(f"Error extracting invoices from QuickBooks: {e}")
            raise DataIngestionError(f"QuickBooks invoice extraction failed: {e}")
    
    async def extract_payments(self, start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Extract payment data from QuickBooks"""
        if not self.client_id:
            return pd.DataFrame()
        
        try:
            # Mock payment data
            mock_payments = [
                {
                    "id": f"QB-PAY-{i:06d}",
                    "invoice_id": f"QB-INV-{i:06d}",
                    "client_id": f"client_{i % 20}",
                    "amount": round(1000 + (i % 10) * 500, 2),
                    "payment_date": (datetime.now() - timedelta(days=i*5)).isoformat(),
                    "payment_method": ["Check", "Credit Card", "Bank Transfer"][i % 3],
                    "reference_number": f"REF-{i:08d}",
                    "status": "Completed" if i % 5 != 0 else "Pending"
                }
                for i in range(1, 31)
            ]
            
            self.logger.info(f"Extracted {len(mock_payments)} payments from QuickBooks")
            return pd.DataFrame(mock_payments)
            
        except Exception as e:
            self.logger.error(f"Error extracting payments from QuickBooks: {e}")
            raise DataIngestionError(f"QuickBooks payment extraction failed: {e}")


class InternalDatabaseIngestion(BaseDataIngestion):
    """Internal database data ingestion"""
    
    def __init__(self):
        super().__init__("internal_db")
        self.database_url = settings.database.url
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    async def extract_clients(self) -> pd.DataFrame:
        """Extract client data from internal database"""
        try:
            with self.Session() as session:
                # Query clients from internal database
                query = text("""
                    SELECT 
                        id,
                        name,
                        email,
                        phone,
                        address,
                        created_at,
                        updated_at,
                        status,
                        contract_value,
                        last_contact
                    FROM clients
                    WHERE organization_id = :org_id
                """)
                
                result = session.execute(query, {"org_id": "f4e806f0-8201-43d3-a80b-ca3bd051497b"})
                clients = result.fetchall()
                
                if not clients:
                    self.logger.warning("No clients found in internal database")
                    return pd.DataFrame()
                
                # Convert to DataFrame
                columns = [desc[0] for desc in result.description]
                df = pd.DataFrame(clients, columns=columns)
                
                self.logger.info(f"Extracted {len(df)} clients from internal database")
                return df
                
        except Exception as e:
            self.logger.error(f"Error extracting clients from internal database: {e}")
            # Return mock data if database query fails
            return self._get_mock_clients()
    
    async def extract_tickets(self, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Extract ticket data from internal database"""
        try:
            with self.Session() as session:
                # Query tickets from internal database
                query = text("""
                    SELECT 
                        id,
                        title,
                        description,
                        status,
                        priority,
                        created_at,
                        updated_at,
                        resolved_at,
                        client_id,
                        assigned_to,
                        service_id,
                        hours_logged,
                        billing_amount
                    FROM tickets
                    WHERE organization_id = :org_id
                """)
                
                result = session.execute(query, {"org_id": "f4e806f0-8201-43d3-a80b-ca3bd051497b"})
                tickets = result.fetchall()
                
                if not tickets:
                    self.logger.warning("No tickets found in internal database")
                    return pd.DataFrame()
                
                # Convert to DataFrame
                columns = [desc[0] for desc in result.description]
                df = pd.DataFrame(tickets, columns=columns)
                
                self.logger.info(f"Extracted {len(df)} tickets from internal database")
                return df
                
        except Exception as e:
            self.logger.error(f"Error extracting tickets from internal database: {e}")
            # Return mock data if database query fails
            return self._get_mock_tickets()
    
    def _get_mock_clients(self) -> pd.DataFrame:
        """Get mock client data when database is unavailable"""
        mock_clients = [
            {
                "id": f"internal_client_{i}",
                "name": f"Internal Client {i}",
                "email": f"client{i}@internal.com",
                "phone": f"+1-555-{i:04d}",
                "address": f"{i} Internal St, City, State {i:05d}",
                "created_at": (datetime.now() - timedelta(days=i*30)).isoformat(),
                "updated_at": (datetime.now() - timedelta(days=i*7)).isoformat(),
                "status": "Active" if i % 4 != 0 else "Inactive",
                "contract_value": round(3000 + (i % 8) * 1500, 2),
                "last_contact": (datetime.now() - timedelta(days=i*5)).isoformat()
            }
            for i in range(1, 16)
        ]
        
        self.logger.info(f"Using mock data: {len(mock_clients)} clients")
        return pd.DataFrame(mock_clients)
    
    def _get_mock_tickets(self) -> pd.DataFrame:
        """Get mock ticket data when database is unavailable"""
        mock_tickets = [
            {
                "id": f"internal_ticket_{i}",
                "title": f"Internal Ticket {i}",
                "description": f"Description for internal ticket {i}",
                "status": ["Open", "In Progress", "Closed"][i % 3],
                "priority": ["Low", "Medium", "High", "Critical"][i % 4],
                "created_at": (datetime.now() - timedelta(days=i*2)).isoformat(),
                "updated_at": (datetime.now() - timedelta(days=i)).isoformat(),
                "resolved_at": (datetime.now() - timedelta(days=i-1)).isoformat() if i % 3 == 2 else None,
                "client_id": f"internal_client_{i % 15}",
                "assigned_to": f"tech_{i % 8}",
                "service_id": f"service_{i % 5}",
                "hours_logged": round(1.5 + (i % 4) * 0.5, 2),
                "billing_amount": round(100 + (i % 6) * 25, 2)
            }
            for i in range(1, 76)
        ]
        
        self.logger.info(f"Using mock data: {len(mock_tickets)} tickets")
        return pd.DataFrame(mock_tickets)


class DataIngestionManager:
    """Manages data ingestion from all sources"""
    
    def __init__(self):
        self.superops = SuperOpsIngestion()
        self.quickbooks = QuickBooksIngestion()
        self.internal_db = InternalDatabaseIngestion()
        self.logger = logging.getLogger(__name__)
    
    async def extract_all_data(self, start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """Extract data from all sources"""
        results = {}
        
        try:
            # Extract from SuperOps
            self.logger.info("Extracting data from SuperOps...")
            results['superops_tickets'] = await self.superops.extract_tickets(start_date, end_date)
            results['superops_clients'] = await self.superops.extract_clients()
            results['superops_technicians'] = await self.superops.extract_technicians()
            
            # Extract from QuickBooks
            self.logger.info("Extracting data from QuickBooks...")
            results['quickbooks_invoices'] = await self.quickbooks.extract_invoices(start_date, end_date)
            results['quickbooks_payments'] = await self.quickbooks.extract_payments(start_date, end_date)
            
            # Extract from Internal Database
            self.logger.info("Extracting data from internal database...")
            results['internal_clients'] = await self.internal_db.extract_clients()
            results['internal_tickets'] = await self.internal_db.extract_tickets(start_date, end_date)
            
            self.logger.info("Data extraction completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in data extraction: {e}")
            raise DataIngestionError(f"Data extraction failed: {e}")
    
    async def extract_specific_data(self, source: str, data_type: str, 
                                  start_date: Optional[datetime] = None,
                                  end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Extract specific data from a specific source"""
        try:
            if source == "superops":
                if data_type == "tickets":
                    return await self.superops.extract_tickets(start_date, end_date)
                elif data_type == "clients":
                    return await self.superops.extract_clients()
                elif data_type == "technicians":
                    return await self.superops.extract_technicians()
                else:
                    raise ValueError(f"Unknown data type for SuperOps: {data_type}")
            
            elif source == "quickbooks":
                if data_type == "invoices":
                    return await self.quickbooks.extract_invoices(start_date, end_date)
                elif data_type == "payments":
                    return await self.quickbooks.extract_payments(start_date, end_date)
                else:
                    raise ValueError(f"Unknown data type for QuickBooks: {data_type}")
            
            elif source == "internal":
                if data_type == "clients":
                    return await self.internal_db.extract_clients()
                elif data_type == "tickets":
                    return await self.internal_db.extract_tickets(start_date, end_date)
                else:
                    raise ValueError(f"Unknown data type for internal database: {data_type}")
            
            else:
                raise ValueError(f"Unknown source: {source}")
                
        except Exception as e:
            self.logger.error(f"Error extracting {data_type} from {source}: {e}")
            raise DataIngestionError(f"Failed to extract {data_type} from {source}: {e}")


# Convenience function for easy usage
async def extract_data(source: Optional[str] = None, data_type: Optional[str] = None,
                      start_date: Optional[datetime] = None, 
                      end_date: Optional[datetime] = None) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
    """
    Extract data from specified source and type, or all sources if not specified
    
    Args:
        source: Source to extract from ('superops', 'quickbooks', 'internal', or None for all)
        data_type: Type of data to extract ('tickets', 'clients', 'invoices', etc.)
        start_date: Start date for data extraction
        end_date: End date for data extraction
    
    Returns:
        DataFrame if specific source and type, or dict of DataFrames if all sources
    """
    manager = DataIngestionManager()
    
    if source and data_type:
        return await manager.extract_specific_data(source, data_type, start_date, end_date)
    else:
        return await manager.extract_all_data(start_date, end_date)
