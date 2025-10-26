"""
QuickBooks API client for financial data extraction
Provides comprehensive access to QuickBooks financial data including transactions,
invoices, payments, expenses, and customer financial profiles.
"""

import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass
from config import settings

logger = logging.getLogger(__name__)


@dataclass
class QuickBooksConfig:
    """Configuration for QuickBooks API client"""
    base_url: str
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    company_id: str
    timeout: int = 30
    max_retries: int = 3
    rate_limit_delay: float = 0.1


class QuickBooksClient:
    """Asynchronous QuickBooks API client"""
    
    def __init__(self, config: QuickBooksConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limiter = asyncio.Semaphore(10)  # Limit concurrent requests
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize the client session"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
            logger.info("QuickBooks client initialized")
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("QuickBooks client closed")
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to QuickBooks API"""
        if not self.session:
            await self.initialize()
        
        url = f"{self.config.base_url}/v3/company/{self.config.company_id}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        async with self._rate_limiter:
            for attempt in range(self.config.max_retries):
                try:
                    async with self.session.request(method, url, headers=headers, **kwargs) as response:
                        if response.status == 401:
                            # Token expired, try to refresh
                            await self._refresh_token()
                            headers["Authorization"] = f"Bearer {self.config.access_token}"
                            continue
                        
                        response.raise_for_status()
                        data = await response.json()
                        
                        # Rate limiting
                        await asyncio.sleep(self.config.rate_limit_delay)
                        return data
                        
                except aiohttp.ClientError as e:
                    logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                    if attempt == self.config.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def _refresh_token(self):
        """Refresh the access token"""
        # This would typically call QuickBooks OAuth refresh endpoint
        # For now, we'll use mock token refresh
        logger.info("Refreshing QuickBooks access token")
        self.config.access_token = "refreshed_mock_token"
    
    async def get_financial_transactions(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract financial transaction data"""
        logger.info(f"Extracting financial transactions from {start_date} to {end_date}")
        
        # Mock data for demonstration
        mock_transactions = []
        for i in range(min(limit, 50)):
            transaction = {
                "id": f"TXN-{i+1:06d}",
                "date": (start_date + timedelta(days=i % 30)).isoformat(),
                "type": ["Income", "Expense", "Transfer"][i % 3],
                "amount": round(1000 + (i * 50) + (i % 10 * 100), 2),
                "description": f"Transaction {i+1} - {['Service Revenue', 'Office Supplies', 'Bank Transfer'][i % 3]}",
                "account": f"Account-{(i % 5) + 1}",
                "category": ["Revenue", "Expenses", "Assets"][i % 3],
                "reference": f"REF-{i+1:06d}",
                "status": ["Posted", "Pending", "Cleared"][i % 3],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            mock_transactions.append(transaction)
        
        logger.info(f"Extracted {len(mock_transactions)} financial transactions")
        return mock_transactions
    
    async def get_invoices_and_payments(self, start_date: datetime, end_date: datetime, limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
        """Get invoice and payment information"""
        logger.info(f"Extracting invoices and payments from {start_date} to {end_date}")
        
        # Mock invoices
        mock_invoices = []
        for i in range(min(limit, 30)):
            invoice = {
                "id": f"INV-{i+1:06d}",
                "invoice_number": f"INV-{i+1:06d}",
                "customer_id": f"CUST-{(i % 10) + 1:03d}",
                "customer_name": f"Customer {(i % 10) + 1}",
                "date": (start_date + timedelta(days=i % 30)).isoformat(),
                "due_date": (start_date + timedelta(days=i % 30 + 30)).isoformat(),
                "amount": round(5000 + (i * 200), 2),
                "tax_amount": round((5000 + (i * 200)) * 0.1, 2),
                "total_amount": round((5000 + (i * 200)) * 1.1, 2),
                "status": ["Draft", "Sent", "Paid", "Overdue"][i % 4],
                "payment_terms": "Net 30",
                "items": [
                    {
                        "description": f"Service Item {j+1}",
                        "quantity": 1,
                        "rate": round(100 + (j * 10), 2),
                        "amount": round(100 + (j * 10), 2)
                    }
                    for j in range((i % 3) + 1)
                ],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            mock_invoices.append(invoice)
        
        # Mock payments
        mock_payments = []
        for i in range(min(limit, 25)):
            payment = {
                "id": f"PAY-{i+1:06d}",
                "payment_number": f"PAY-{i+1:06d}",
                "invoice_id": f"INV-{(i % 30) + 1:06d}",
                "customer_id": f"CUST-{(i % 10) + 1:03d}",
                "customer_name": f"Customer {(i % 10) + 1}",
                "date": (start_date + timedelta(days=i % 30)).isoformat(),
                "amount": round(4000 + (i * 150), 2),
                "payment_method": ["Check", "Credit Card", "Bank Transfer", "Cash"][i % 4],
                "reference": f"PAY-REF-{i+1:06d}",
                "status": ["Pending", "Cleared", "Failed"][i % 3],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            mock_payments.append(payment)
        
        result = {
            "invoices": mock_invoices,
            "payments": mock_payments
        }
        
        logger.info(f"Extracted {len(mock_invoices)} invoices and {len(mock_payments)} payments")
        return result
    
    async def get_expenses_and_costs(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract expense and cost data"""
        logger.info(f"Extracting expenses and costs from {start_date} to {end_date}")
        
        # Mock expenses
        mock_expenses = []
        for i in range(min(limit, 40)):
            expense = {
                "id": f"EXP-{i+1:06d}",
                "expense_number": f"EXP-{i+1:06d}",
                "vendor_id": f"VEND-{(i % 8) + 1:03d}",
                "vendor_name": f"Vendor {(i % 8) + 1}",
                "date": (start_date + timedelta(days=i % 30)).isoformat(),
                "amount": round(100 + (i * 25), 2),
                "tax_amount": round((100 + (i * 25)) * 0.08, 2),
                "total_amount": round((100 + (i * 25)) * 1.08, 2),
                "category": ["Office Supplies", "Software", "Travel", "Marketing", "Utilities"][i % 5],
                "description": f"Expense {i+1} - {['Office Supplies', 'Software License', 'Business Travel', 'Marketing Campaign', 'Utility Bill'][i % 5]}",
                "payment_method": ["Check", "Credit Card", "Bank Transfer"][i % 3],
                "status": ["Pending", "Approved", "Paid"][i % 3],
                "receipt_url": f"https://receipts.example.com/exp-{i+1:06d}.pdf",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            mock_expenses.append(expense)
        
        logger.info(f"Extracted {len(mock_expenses)} expenses and costs")
        return mock_expenses
    
    async def get_customer_financial_profiles(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get customer financial profiles"""
        logger.info("Extracting customer financial profiles")
        
        # Mock customer profiles
        mock_profiles = []
        for i in range(min(limit, 20)):
            profile = {
                "customer_id": f"CUST-{i+1:03d}",
                "customer_name": f"Customer {i+1}",
                "company_name": f"Company {i+1}",
                "email": f"customer{i+1}@example.com",
                "phone": f"+1-555-{i+1:04d}",
                "address": {
                    "street": f"{100 + i} Main St",
                    "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"][i % 5],
                    "state": ["NY", "CA", "IL", "TX", "AZ"][i % 5],
                    "zip": f"{10000 + i}",
                    "country": "USA"
                },
                "financial_summary": {
                    "total_invoiced": round(50000 + (i * 5000), 2),
                    "total_paid": round(45000 + (i * 4500), 2),
                    "outstanding_balance": round(5000 + (i * 500), 2),
                    "average_payment_days": 25 + (i % 15),
                    "credit_limit": round(100000 + (i * 10000), 2),
                    "payment_terms": "Net 30"
                },
                "transaction_history": {
                    "total_transactions": 50 + (i * 5),
                    "last_transaction_date": (datetime.now() - timedelta(days=i % 30)).isoformat(),
                    "average_transaction_amount": round(1000 + (i * 100), 2),
                    "payment_frequency": ["Monthly", "Quarterly", "Annual"][i % 3]
                },
                "risk_assessment": {
                    "credit_score": 700 + (i % 100),
                    "payment_reliability": round(0.85 + (i % 15) * 0.01, 2),
                    "risk_level": ["Low", "Medium", "High"][i % 3],
                    "notes": f"Customer {i+1} risk assessment notes"
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            mock_profiles.append(profile)
        
        logger.info(f"Extracted {len(mock_profiles)} customer financial profiles")
        return mock_profiles
    
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


# Factory function for creating QuickBooks client
def create_quickbooks_client() -> QuickBooksClient:
    """Create QuickBooks client with configuration from settings"""
    config = QuickBooksConfig(
        base_url=settings.quickbooks.base_url,
        client_id=settings.quickbooks.client_id,
        client_secret=settings.quickbooks.client_secret,
        access_token=settings.quickbooks.access_token,
        refresh_token=settings.quickbooks.refresh_token,
        company_id=settings.quickbooks.company_id,
        timeout=settings.quickbooks.timeout,
        max_retries=settings.quickbooks.max_retries,
        rate_limit_delay=settings.quickbooks.rate_limit_delay
    )
    
    return QuickBooksClient(config)
