"""
Comprehensive data extractor that integrates all data sources
Combines SuperOps, QuickBooks, and internal database data extraction
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass

from .superops_graphql_client import create_superops_graphql_client
from .quickbooks_rest_client import create_quickbooks_rest_client
from .transformers import DataTransformer
from ..utils.error_handlers import get_error_handler
from .internal_db_connector import create_internal_db_connector

logger = logging.getLogger(__name__)


@dataclass
class ExtractionConfig:
    """Configuration for comprehensive data extraction"""
    start_date: datetime
    end_date: datetime
    include_superops: bool = True
    include_quickbooks: bool = True
    include_internal: bool = True
    max_records_per_source: int = 1000
    parallel_extraction: bool = True


class ComprehensiveDataExtractor:
    """Comprehensive data extractor for all data sources"""
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.superops_client = None
        self.quickbooks_client = None
        self.internal_db_connector = None
        self.transformer = DataTransformer()
        self.error_handler = get_error_handler()
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize all data source clients"""
        logger.info("Initializing comprehensive data extractor")
        
        if self.config.include_superops:
            self.superops_client = create_superops_graphql_client()
            await self.superops_client.initialize()
            logger.info("SuperOps GraphQL client initialized")
        
        if self.config.include_quickbooks:
            self.quickbooks_client = create_quickbooks_rest_client()
            await self.quickbooks_client.initialize()
            logger.info("QuickBooks REST client initialized")
        
        if self.config.include_internal:
            self.internal_db_connector = create_internal_db_connector()
            await self.internal_db_connector.initialize()
            logger.info("Internal database connector initialized")
    
    async def close(self):
        """Close all data source clients"""
        if self.superops_client:
            await self.superops_client.close()
        if self.quickbooks_client:
            await self.quickbooks_client.close()
        if self.internal_db_connector:
            await self.internal_db_connector.close()
        logger.info("Comprehensive data extractor closed")
    
    async def extract_all_data(self) -> Dict[str, Any]:
        """Extract data from all configured sources"""
        logger.info("Starting comprehensive data extraction")
        start_time = datetime.now()
        
        all_data = {
            "extraction_metadata": {
                "start_time": start_time.isoformat(),
                "config": {
                    "start_date": self.config.start_date.isoformat(),
                    "end_date": self.config.end_date.isoformat(),
                    "sources": {
                        "superops": self.config.include_superops,
                        "quickbooks": self.config.include_quickbooks,
                        "internal": self.config.include_internal
                    }
                }
            }
        }
        
        if self.config.parallel_extraction:
            # Extract from all sources in parallel
            tasks = []
            
            if self.config.include_superops:
                tasks.append(self._extract_superops_data())
            
            if self.config.include_quickbooks:
                tasks.append(self._extract_quickbooks_data())
            
            if self.config.include_internal:
                tasks.append(self._extract_internal_data())
            
            # Wait for all extractions to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Extraction task {i} failed: {result}")
                else:
                    all_data.update(result)
        else:
            # Extract from sources sequentially
            if self.config.include_superops:
                try:
                    superops_data = await self._extract_superops_data()
                    all_data.update(superops_data)
                except Exception as e:
                    logger.error(f"SuperOps extraction failed: {e}")
            
            if self.config.include_quickbooks:
                try:
                    quickbooks_data = await self._extract_quickbooks_data()
                    all_data.update(quickbooks_data)
                except Exception as e:
                    logger.error(f"QuickBooks extraction failed: {e}")
            
            if self.config.include_internal:
                try:
                    internal_data = await self._extract_internal_data()
                    all_data.update(internal_data)
                except Exception as e:
                    logger.error(f"Internal database extraction failed: {e}")
        
        # Add final metadata
        end_time = datetime.now()
        all_data["extraction_metadata"]["end_time"] = end_time.isoformat()
        all_data["extraction_metadata"]["duration_seconds"] = (end_time - start_time).total_seconds()
        all_data["extraction_metadata"]["total_records"] = sum(
            len(data) for data in all_data.values() 
            if isinstance(data, list)
        )
        
        # Calculate metrics from transformed data
        metrics = self.transformer.calculate_metrics(all_data)
        all_data["metrics"] = metrics
        
        logger.info(f"Comprehensive data extraction completed in {(end_time - start_time).total_seconds():.2f}s")
        logger.info(f"Total records extracted: {all_data['extraction_metadata']['total_records']}")
        
        return all_data
    
    async def _extract_superops_data(self) -> Dict[str, Any]:
        """Extract data from SuperOps using GraphQL client"""
        logger.info("Extracting SuperOps data")
        
        superops_data = {}
        
        try:
            # Extract tickets with error handling
            tickets_raw = await self.error_handler.with_retry(
                self.superops_client.get_tickets,
                "superops",
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                limit=self.config.max_records_per_source
            )
            
            # Transform tickets to internal format
            tickets = self.transformer.transform_superops_tickets(tickets_raw)
            superops_data["superops_tickets"] = tickets
            
            # Extract clients
            clients_raw = await self.error_handler.with_retry(
                self.superops_client.get_clients,
                "superops",
                limit=self.config.max_records_per_source
            )
            
            # Transform clients to internal format
            clients = self.transformer.transform_superops_clients(clients_raw)
            superops_data["superops_clients"] = clients
            
            # Extract technicians
            technicians_raw = await self.error_handler.with_retry(
                self.superops_client.get_technicians,
                "superops",
                limit=self.config.max_records_per_source
            )
            
            # Transform technicians to internal format
            technicians = self.transformer.transform_superops_technicians(technicians_raw)
            superops_data["superops_technicians"] = technicians
            
            # Extract SLA metrics
            sla_metrics_raw = await self.error_handler.with_retry(
                self.superops_client.get_sla_metrics,
                "superops",
                start_date=self.config.start_date,
                end_date=self.config.end_date
            )
            superops_data["superops_sla_metrics"] = sla_metrics_raw
            
        except Exception as e:
            logger.error(f"SuperOps data extraction failed: {e}")
            # Return empty data structure
            superops_data = {
                "superops_tickets": [],
                "superops_clients": [],
                "superops_technicians": [],
                "superops_sla_metrics": []
            }
        
        logger.info(f"SuperOps data extracted: {sum(len(data) for data in superops_data.values() if isinstance(data, list))} records")
        return superops_data
    
    async def _extract_quickbooks_data(self) -> Dict[str, Any]:
        """Extract data from QuickBooks using REST client with OAuth"""
        logger.info("Extracting QuickBooks data")
        
        quickbooks_data = {}
        
        try:
            # Extract financial transactions with error handling
            transactions_raw = await self.error_handler.with_retry(
                self.quickbooks_client.get_financial_transactions,
                "quickbooks",
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                limit=self.config.max_records_per_source
            )
            quickbooks_data["quickbooks_transactions"] = transactions_raw
            
            # Extract invoices and payments
            invoices_payments_raw = await self.error_handler.with_retry(
                self.quickbooks_client.get_invoices_and_payments,
                "quickbooks",
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                limit=self.config.max_records_per_source
            )
            
            # Transform invoices and payments to internal format
            invoices = self.transformer.transform_quickbooks_invoices(invoices_payments_raw.get("invoices", []))
            payments = self.transformer.transform_quickbooks_payments(invoices_payments_raw.get("payments", []))
            
            quickbooks_data["quickbooks_invoices"] = invoices
            quickbooks_data["quickbooks_payments"] = payments
            
            # Extract expenses
            expenses_raw = await self.error_handler.with_retry(
                self.quickbooks_client.get_expenses_and_costs,
                "quickbooks",
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                limit=self.config.max_records_per_source
            )
            
            # Transform expenses to internal format
            expenses = self.transformer.transform_quickbooks_expenses(expenses_raw)
            quickbooks_data["quickbooks_expenses"] = expenses
            
            # Extract customer profiles
            customers_raw = await self.error_handler.with_retry(
                self.quickbooks_client.get_customer_financial_profiles,
                "quickbooks",
                limit=self.config.max_records_per_source
            )
            
            # Transform customers to internal format
            customers = self.transformer.transform_quickbooks_customers(customers_raw)
            quickbooks_data["quickbooks_customers"] = customers
            
        except Exception as e:
            logger.error(f"QuickBooks data extraction failed: {e}")
            # Return empty data structure
            quickbooks_data = {
                "quickbooks_transactions": [],
                "quickbooks_invoices": [],
                "quickbooks_payments": [],
                "quickbooks_expenses": [],
                "quickbooks_customers": []
            }
        
        logger.info(f"QuickBooks data extracted: {sum(len(data) for data in quickbooks_data.values() if isinstance(data, list))} records")
        return quickbooks_data
    
    async def _extract_internal_data(self) -> Dict[str, Any]:
        """Extract data from internal database"""
        logger.info("Extracting internal database data")
        
        internal_data = await self.internal_db_connector.get_all_internal_data()
        
        # Rename keys to avoid conflicts
        renamed_data = {}
        for key, value in internal_data.items():
            if key != "extraction_metadata":
                renamed_data[f"internal_{key}"] = value
            else:
                renamed_data[key] = value
        
        logger.info(f"Internal database data extracted: {sum(len(data) for data in renamed_data.values() if isinstance(data, list))} records")
        return renamed_data
    
    async def extract_client_specific_data(self, client_id: str) -> Dict[str, Any]:
        """Extract all data for a specific client"""
        logger.info(f"Extracting client-specific data for: {client_id}")
        
        client_data = {
            "client_id": client_id,
            "extraction_timestamp": datetime.now().isoformat()
        }
        
        # Extract from SuperOps (if client exists there)
        if self.config.include_superops:
            try:
                # Filter SuperOps data by client
                tickets = await self.superops_client.get_tickets(
                    start_date=self.config.start_date,
                    end_date=self.config.end_date,
                    limit=self.config.max_records_per_source
                )
                client_tickets = [t for t in tickets if t.get("client_id") == client_id]
                client_data["superops_tickets"] = client_tickets
                
                clients = await self.superops_client.get_clients(limit=self.config.max_records_per_source)
                client_info = next((c for c in clients if c.get("id") == client_id), None)
                if client_info:
                    client_data["superops_client"] = client_info
                    
            except Exception as e:
                logger.error(f"SuperOps client data extraction failed: {e}")
        
        # Extract from QuickBooks (if client exists there)
        if self.config.include_quickbooks:
            try:
                # Filter QuickBooks data by client
                invoices_payments = await self.quickbooks_client.get_invoices_and_payments(
                    start_date=self.config.start_date,
                    end_date=self.config.end_date,
                    limit=self.config.max_records_per_source
                )
                
                client_invoices = [inv for inv in invoices_payments.get("invoices", []) 
                                 if inv.get("customer_id") == client_id]
                client_payments = [pay for pay in invoices_payments.get("payments", []) 
                                 if pay.get("customer_id") == client_id]
                
                client_data["quickbooks_invoices"] = client_invoices
                client_data["quickbooks_payments"] = client_payments
                
            except Exception as e:
                logger.error(f"QuickBooks client data extraction failed: {e}")
        
        # Extract from internal database
        if self.config.include_internal:
            try:
                internal_data = await self.internal_db_connector.get_all_internal_data(client_id)
                client_data.update(internal_data)
            except Exception as e:
                logger.error(f"Internal database client data extraction failed: {e}")
        
        logger.info(f"Client-specific data extracted for {client_id}: {sum(len(data) for data in client_data.values() if isinstance(data, list))} records")
        return client_data
    
    async def get_real_time_updates(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Get real-time updates from all sources"""
        logger.info("Starting real-time updates from all sources")
        
        # Create async generators for each source
        generators = []
        
        if self.config.include_superops and self.superops_client:
            generators.append(self.superops_client.get_real_time_updates())
        
        if self.config.include_quickbooks and self.quickbooks_client:
            generators.append(self.quickbooks_client.get_real_time_financial_updates())
        
        # Combine all generators
        while True:
            try:
                # Get updates from all sources
                for generator in generators:
                    try:
                        update = await generator.__anext__()
                        yield {
                            "source": "combined",
                            "timestamp": datetime.now().isoformat(),
                            "data": update
                        }
                    except StopAsyncIteration:
                        continue
                
                await asyncio.sleep(1)  # Small delay between updates
                
            except Exception as e:
                logger.error(f"Error in real-time updates: {e}")
                await asyncio.sleep(5)


# Factory function for creating comprehensive extractor
def create_comprehensive_extractor(
    start_date: datetime,
    end_date: datetime,
    include_superops: bool = True,
    include_quickbooks: bool = True,
    include_internal: bool = True,
    max_records_per_source: int = 1000,
    parallel_extraction: bool = True
) -> ComprehensiveDataExtractor:
    """Create comprehensive data extractor with specified configuration"""
    config = ExtractionConfig(
        start_date=start_date,
        end_date=end_date,
        include_superops=include_superops,
        include_quickbooks=include_quickbooks,
        include_internal=include_internal,
        max_records_per_source=max_records_per_source,
        parallel_extraction=parallel_extraction
    )
    
    return ComprehensiveDataExtractor(config)
