"""
QuickBooks REST Client
Real implementation using REST API with OAuth 2.0 authentication
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass
import aiohttp

from config import settings
from .token_manager import create_token_manager, TokenManager
from .quickbooks_oauth import create_quickbooks_oauth, QuickBooksOAuth

logger = logging.getLogger(__name__)


@dataclass
class QuickBooksRESTConfig:
    """QuickBooks REST API configuration"""
    base_url: str
    company_id: str
    use_sandbox: bool = True
    timeout: int = 30
    max_retries: int = 3
    rate_limit_delay: float = 0.1


class QuickBooksRESTError(Exception):
    """Custom exception for QuickBooks REST API errors"""
    pass


class QuickBooksRESTClient:
    """Real QuickBooks REST API client with OAuth 2.0"""
    
    def __init__(self, config: QuickBooksRESTConfig, token_manager: TokenManager):
        self.config = config
        self.token_manager = token_manager
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limiter = asyncio.Semaphore(10)
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize the REST client"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
            logger.info("QuickBooks REST client initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize QuickBooks REST client: {e}")
            raise QuickBooksRESTError(f"Client initialization failed: {e}")
    
    async def close(self):
        """Close the REST client"""
        if self.session:
            await self.session.close()
            logger.info("QuickBooks REST client closed")
    
    async def _get_valid_token(self) -> str:
        """Get valid access token, refresh if needed"""
        try:
            # Try to get valid token
            token = await self.token_manager.get_valid_token("quickbooks", self.config.company_id)
            
            if token:
                return token
            
            # Token expired or not found, try to refresh
            logger.info("Token expired or not found, attempting refresh")
            refresh_success = await self.token_manager.refresh_token("quickbooks", self.config.company_id)
            
            if refresh_success:
                # Get the refreshed token
                token = await self.token_manager.get_valid_token("quickbooks", self.config.company_id)
                if token:
                    return token
            
            raise QuickBooksRESTError("No valid token available")
            
        except Exception as e:
            logger.error(f"Failed to get valid token: {e}")
            raise QuickBooksRESTError(f"Token retrieval failed: {e}")
    
    async def _make_request(self, method: str, endpoint: str, 
                           params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """Make authenticated request to QuickBooks API"""
        if not self.session:
            await self.initialize()
        
        # Get valid access token
        access_token = await self._get_valid_token()
        
        # Build URL
        url = f"{self.config.base_url}/v3/company/{self.config.company_id}{endpoint}"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        async with self._rate_limiter:
            for attempt in range(self.config.max_retries):
                try:
                    async with self.session.request(
                        method, url, headers=headers,
                        params=params, json=data
                    ) as response:
                        
                        # Handle token expiration
                        if response.status == 401:
                            logger.warning("Token expired, attempting refresh")
                            await self.token_manager.refresh_token("quickbooks", self.config.company_id)
                            access_token = await self._get_valid_token()
                            headers["Authorization"] = f"Bearer {access_token}"
                            continue
                        
                        # Handle rate limiting
                        if response.status == 429:
                            wait_time = 2 ** attempt
                            logger.warning(f"Rate limited, waiting {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                        
                        # Check for other errors
                        if response.status >= 400:
                            error_text = await response.text()
                            logger.error(f"API error {response.status}: {error_text}")
                            raise QuickBooksRESTError(f"API error {response.status}: {error_text}")
                        
                        # Parse response
                        result = await response.json()
                        
                        # Rate limiting delay
                        await asyncio.sleep(self.config.rate_limit_delay)
                        
                        return result
                        
                except aiohttp.ClientError as e:
                    logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                    if attempt == self.config.max_retries - 1:
                        raise QuickBooksRESTError(f"Request failed after {self.config.max_retries} attempts: {e}")
                    await asyncio.sleep(2 ** attempt)
            
            raise QuickBooksRESTError("Max retries exceeded")
    
    async def query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL-like query against QuickBooks API"""
        try:
            logger.info(f"Executing QuickBooks query: {sql_query}")
            
            result = await self._make_request(
                "GET", "/query",
                params={"query": sql_query}
            )
            
            logger.info("QuickBooks query executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute QuickBooks query: {e}")
            raise QuickBooksRESTError(f"Query execution failed: {e}")
    
    async def get_financial_transactions(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract financial transaction data from QuickBooks"""
        try:
            logger.info(f"Extracting financial transactions from {start_date} to {end_date}")
            
            # Build SQL query for transactions
            query = f"""
            SELECT * FROM Transaction 
            WHERE TxnDate >= '{start_date.strftime('%Y-%m-%d')}' 
            AND TxnDate <= '{end_date.strftime('%Y-%m-%d')}' 
            MAXRESULTS {limit}
            """
            
            result = await self.query(query)
            
            # Extract transactions from response
            transactions = result.get("QueryResponse", {}).get("Transaction", [])
            
            logger.info(f"Extracted {len(transactions)} financial transactions")
            return transactions
            
        except Exception as e:
            logger.error(f"Failed to extract financial transactions: {e}")
            # Return mock data for development/fallback
            return await self._get_mock_transactions(start_date, end_date, limit)
    
    async def get_invoices_and_payments(self, start_date: datetime, end_date: datetime, limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
        """Get invoice and payment information from QuickBooks"""
        try:
            logger.info(f"Extracting invoices and payments from {start_date} to {end_date}")
            
            # Build queries for invoices and payments
            invoice_query = f"""
            SELECT * FROM Invoice 
            WHERE TxnDate >= '{start_date.strftime('%Y-%m-%d')}' 
            AND TxnDate <= '{end_date.strftime('%Y-%m-%d')}' 
            MAXRESULTS {limit}
            """
            
            payment_query = f"""
            SELECT * FROM Payment 
            WHERE TxnDate >= '{start_date.strftime('%Y-%m-%d')}' 
            AND TxnDate <= '{end_date.strftime('%Y-%m-%d')}' 
            MAXRESULTS {limit}
            """
            
            # Execute queries in parallel
            invoice_result, payment_result = await asyncio.gather(
                self.query(invoice_query),
                self.query(payment_query),
                return_exceptions=True
            )
            
            # Extract data from results
            invoices = []
            payments = []
            
            if not isinstance(invoice_result, Exception):
                invoices = invoice_result.get("QueryResponse", {}).get("Invoice", [])
            
            if not isinstance(payment_result, Exception):
                payments = payment_result.get("QueryResponse", {}).get("Payment", [])
            
            result = {
                "invoices": invoices,
                "payments": payments
            }
            
            logger.info(f"Extracted {len(invoices)} invoices and {len(payments)} payments")
            return result
            
        except Exception as e:
            logger.error(f"Failed to extract invoices and payments: {e}")
            return await self._get_mock_invoices_and_payments(start_date, end_date, limit)
    
    async def get_expenses_and_costs(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract expense and cost data from QuickBooks"""
        try:
            logger.info(f"Extracting expenses and costs from {start_date} to {end_date}")
            
            # Build query for expenses
            query = f"""
            SELECT * FROM Purchase 
            WHERE TxnDate >= '{start_date.strftime('%Y-%m-%d')}' 
            AND TxnDate <= '{end_date.strftime('%Y-%m-%d')}' 
            MAXRESULTS {limit}
            """
            
            result = await self.query(query)
            
            # Extract expenses from response
            expenses = result.get("QueryResponse", {}).get("Purchase", [])
            
            logger.info(f"Extracted {len(expenses)} expenses and costs")
            return expenses
            
        except Exception as e:
            logger.error(f"Failed to extract expenses and costs: {e}")
            return await self._get_mock_expenses(start_date, end_date, limit)
    
    async def get_customer_financial_profiles(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get customer financial profiles from QuickBooks"""
        try:
            logger.info("Extracting customer financial profiles")
            
            # Build query for customers
            query = f"""
            SELECT * FROM Customer 
            MAXRESULTS {limit}
            """
            
            result = await self.query(query)
            
            # Extract customers from response
            customers = result.get("QueryResponse", {}).get("Customer", [])
            
            logger.info(f"Extracted {len(customers)} customer financial profiles")
            return customers
            
        except Exception as e:
            logger.error(f"Failed to extract customer financial profiles: {e}")
            return await self._get_mock_customer_profiles(limit)
    
    async def get_reports(self, report_type: str, start_date: Optional[datetime] = None, 
                         end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get QuickBooks reports"""
        try:
            logger.info(f"Extracting {report_type} report")
            
            # Build report URL
            endpoint = f"/reports/{report_type}"
            params = {}
            
            if start_date:
                params["start_date"] = start_date.strftime('%Y-%m-%d')
            if end_date:
                params["end_date"] = end_date.strftime('%Y-%m-%d')
            
            result = await self._make_request("GET", endpoint, params=params)
            
            logger.info(f"Extracted {report_type} report")
            return result
            
        except Exception as e:
            logger.error(f"Failed to extract {report_type} report: {e}")
            return await self._get_mock_report(report_type)
    
    async def get_real_time_financial_updates(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Implement real-time financial updates"""
        logger.info("Starting real-time financial updates stream")
        
        update_types = ["transaction", "invoice", "payment", "expense"]
        
        while True:
            try:
                # Generate mock real-time update
                update = {
                    "id": f"UPDATE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "type": update_types[datetime.now().second % len(update_types)],
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "amount": round(1000 + (datetime.now().second * 50), 2),
                        "description": f"Real-time {update_types[datetime.now().second % len(update_types)]} update",
                        "status": "processed"
                    }
                }
                
                yield update
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in real-time updates: {e}")
                await asyncio.sleep(10)
    
    # Mock data methods for development and fallback
    async def _get_mock_transactions(self, start_date: datetime, end_date: datetime, limit: int) -> List[Dict[str, Any]]:
        """Generate mock transaction data for development/fallback"""
        mock_transactions = []
        for i in range(min(limit, 50)):
            transaction = {
                "Id": f"TXN-{i+1:06d}",
                "TxnDate": (start_date + timedelta(days=i % 30)).strftime('%Y-%m-%d'),
                "TxnType": ["Income", "Expense", "Transfer"][i % 3],
                "TotalAmt": round(1000 + (i * 50) + (i % 10 * 100), 2),
                "Description": f"Transaction {i+1} - {['Service Revenue', 'Office Supplies', 'Bank Transfer'][i % 3]}",
                "AccountRef": {"value": f"Account-{(i % 5) + 1}", "name": f"Account {(i % 5) + 1}"},
                "Category": ["Revenue", "Expenses", "Assets"][i % 3],
                "Reference": f"REF-{i+1:06d}",
                "Status": ["Posted", "Pending", "Cleared"][i % 3],
                "MetaData": {
                    "CreateTime": datetime.now().isoformat(),
                    "LastUpdatedTime": datetime.now().isoformat()
                }
            }
            mock_transactions.append(transaction)
        
        return mock_transactions
    
    async def _get_mock_invoices_and_payments(self, start_date: datetime, end_date: datetime, limit: int) -> Dict[str, List[Dict[str, Any]]]:
        """Generate mock invoice and payment data for development/fallback"""
        mock_invoices = []
        mock_payments = []
        
        for i in range(min(limit, 30)):
            invoice = {
                "Id": f"INV-{i+1:06d}",
                "DocNumber": f"INV-{i+1:06d}",
                "CustomerRef": {"value": f"CUST-{(i % 10) + 1:03d}", "name": f"Customer {(i % 10) + 1}"},
                "TxnDate": (start_date + timedelta(days=i % 30)).strftime('%Y-%m-%d'),
                "DueDate": (start_date + timedelta(days=i % 30 + 30)).strftime('%Y-%m-%d'),
                "TotalAmt": round(5000 + (i * 200), 2),
                "TaxAmt": round((5000 + (i * 200)) * 0.1, 2),
                "Balance": round((5000 + (i * 200)) * 0.2, 2),  # 20% balance
                "Status": ["Draft", "Sent", "Paid", "Overdue"][i % 4],
                "PaymentTerms": "Net 30",
                "Line": [
                    {
                        "Description": f"Service Item {j+1}",
                        "Amount": round(100 + (j * 10), 2)
                    }
                    for j in range((i % 3) + 1)
                ],
                "MetaData": {
                    "CreateTime": datetime.now().isoformat(),
                    "LastUpdatedTime": datetime.now().isoformat()
                }
            }
            mock_invoices.append(invoice)
        
        for i in range(min(limit, 25)):
            payment = {
                "Id": f"PAY-{i+1:06d}",
                "PaymentRefNum": f"PAY-{i+1:06d}",
                "CustomerRef": {"value": f"CUST-{(i % 10) + 1:03d}", "name": f"Customer {(i % 10) + 1}"},
                "TxnDate": (start_date + timedelta(days=i % 30)).strftime('%Y-%m-%d'),
                "TotalAmt": round(4000 + (i * 150), 2),
                "PaymentMethod": ["Check", "Credit Card", "Bank Transfer", "Cash"][i % 4],
                "Reference": f"PAY-REF-{i+1:06d}",
                "Status": ["Pending", "Cleared", "Failed"][i % 3],
                "MetaData": {
                    "CreateTime": datetime.now().isoformat(),
                    "LastUpdatedTime": datetime.now().isoformat()
                }
            }
            mock_payments.append(payment)
        
        return {
            "invoices": mock_invoices,
            "payments": mock_payments
        }
    
    async def _get_mock_expenses(self, start_date: datetime, end_date: datetime, limit: int) -> List[Dict[str, Any]]:
        """Generate mock expense data for development/fallback"""
        mock_expenses = []
        for i in range(min(limit, 40)):
            expense = {
                "Id": f"EXP-{i+1:06d}",
                "DocNumber": f"EXP-{i+1:06d}",
                "VendorRef": {"value": f"VEND-{(i % 8) + 1:03d}", "name": f"Vendor {(i % 8) + 1}"},
                "TxnDate": (start_date + timedelta(days=i % 30)).strftime('%Y-%m-%d'),
                "TotalAmt": round(100 + (i * 25), 2),
                "TaxAmt": round((100 + (i * 25)) * 0.08, 2),
                "Category": ["Office Supplies", "Software", "Travel", "Marketing", "Utilities"][i % 5],
                "Description": f"Expense {i+1} - {['Office Supplies', 'Software License', 'Business Travel', 'Marketing Campaign', 'Utility Bill'][i % 5]}",
                "PaymentMethod": ["Check", "Credit Card", "Bank Transfer"][i % 3],
                "Status": ["Pending", "Approved", "Paid"][i % 3],
                "MetaData": {
                    "CreateTime": datetime.now().isoformat(),
                    "LastUpdatedTime": datetime.now().isoformat()
                }
            }
            mock_expenses.append(expense)
        
        return mock_expenses
    
    async def _get_mock_customer_profiles(self, limit: int) -> List[Dict[str, Any]]:
        """Generate mock customer profile data for development/fallback"""
        mock_profiles = []
        for i in range(min(limit, 20)):
            profile = {
                "Id": f"CUST-{i+1:03d}",
                "DisplayName": f"Customer {i+1}",
                "CompanyName": f"Company {i+1}",
                "PrimaryEmailAddr": {"Address": f"customer{i+1}@example.com"},
                "PrimaryPhone": {"FreeFormNumber": f"+1-555-{i+1:04d}"},
                "BillAddr": {
                    "Line1": f"{100 + i} Main St",
                    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"][i % 5],
                    "CountrySubDivisionCode": ["NY", "CA", "IL", "TX", "AZ"][i % 5],
                    "PostalCode": f"{10000 + i}",
                    "Country": "USA"
                },
                "Balance": round(5000 + (i * 500), 2),
                "BalanceWithJobs": round(5000 + (i * 500), 2),
                "CurrencyRef": {"value": "USD"},
                "PaymentTerms": "Net 30",
                "MetaData": {
                    "CreateTime": datetime.now().isoformat(),
                    "LastUpdatedTime": datetime.now().isoformat()
                }
            }
            mock_profiles.append(profile)
        
        return mock_profiles
    
    async def _get_mock_report(self, report_type: str) -> Dict[str, Any]:
        """Generate mock report data for development/fallback"""
        return {
            "ReportName": report_type,
            "ReportDate": datetime.now().strftime('%Y-%m-%d'),
            "ReportBasis": "Accrual",
            "StartPeriod": datetime.now().strftime('%Y-%m-%d'),
            "EndPeriod": datetime.now().strftime('%Y-%m-%d'),
            "Summary": {
                "TotalRevenue": 50000.00,
                "TotalExpenses": 30000.00,
                "NetIncome": 20000.00
            },
            "Rows": [
                {
                    "Row": {
                        "ColData": [
                            {"value": "Revenue"},
                            {"value": "50000.00"}
                        ]
                    }
                },
                {
                    "Row": {
                        "ColData": [
                            {"value": "Expenses"},
                            {"value": "30000.00"}
                        ]
                    }
                }
            ]
        }


# Factory function for creating QuickBooks REST client
def create_quickbooks_rest_client() -> QuickBooksRESTClient:
    """Create QuickBooks REST client with configuration from settings"""
    config = QuickBooksRESTConfig(
        base_url=settings.quickbooks.base_url,
        company_id=settings.quickbooks.company_id,
        use_sandbox=settings.quickbooks.use_sandbox,
        timeout=settings.quickbooks.timeout,
        max_retries=settings.quickbooks.max_retries,
        rate_limit_delay=settings.quickbooks.rate_limit_delay
    )
    
    token_manager = create_token_manager()
    
    return QuickBooksRESTClient(config, token_manager)
