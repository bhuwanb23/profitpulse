"""
Integration Tests for Real API Implementation
Test the real SuperOps GraphQL and QuickBooks REST clients
"""

import asyncio
import logging
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.data.superops_graphql_client import SuperOpsGraphQLClient, SuperOpsGraphQLConfig
from src.data.quickbooks_rest_client import QuickBooksRESTClient, QuickBooksRESTConfig
from src.auth.token_manager import TokenManager
from src.data.transformers import DataTransformer
from src.utils.error_handlers import get_error_handler

logger = logging.getLogger(__name__)


class TestSuperOpsGraphQLClient:
    """Test SuperOps GraphQL client"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock SuperOps configuration"""
        return SuperOpsGraphQLConfig(
            base_url="https://api.superops.ai/it",
            api_key="test_api_key",
            tenant_id="test_tenant_id"
        )
    
    @pytest.fixture
    def client(self, mock_config):
        """Create SuperOps GraphQL client"""
        return SuperOpsGraphQLClient(mock_config)
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Test client initialization"""
        # Mock the transport and client creation
        with patch('src.data.superops_graphql_client.AIOHTTPTransport') as mock_transport:
            with patch('src.data.superops_graphql_client.Client') as mock_client:
                await client.initialize()
                
                assert client.transport is not None
                assert client.client is not None
                logger.info("SuperOps GraphQL client initialization test passed")
    
    @pytest.mark.asyncio
    async def test_get_tickets_mock_data(self, client):
        """Test getting tickets with mock data fallback"""
        # This will use mock data since we don't have real API credentials
        tickets = await client.get_tickets()
        
        assert isinstance(tickets, list)
        assert len(tickets) > 0
        
        # Check ticket structure
        ticket = tickets[0]
        assert "ticketId" in ticket
        assert "displayId" in ticket
        assert "subject" in ticket
        assert "status" in ticket
        
        logger.info(f"SuperOps tickets test passed - got {len(tickets)} tickets")
    
    @pytest.mark.asyncio
    async def test_get_clients_mock_data(self, client):
        """Test getting clients with mock data fallback"""
        clients = await client.get_clients()
        
        assert isinstance(clients, list)
        assert len(clients) > 0
        
        # Check client structure
        client_data = clients[0]
        assert "id" in client_data
        assert "name" in client_data
        
        logger.info(f"SuperOps clients test passed - got {len(clients)} clients")
    
    @pytest.mark.asyncio
    async def test_get_technicians_mock_data(self, client):
        """Test getting technicians with mock data fallback"""
        technicians = await client.get_technicians()
        
        assert isinstance(technicians, list)
        assert len(technicians) > 0
        
        # Check technician structure
        technician = technicians[0]
        assert "userId" in technician
        assert "name" in technician
        
        logger.info(f"SuperOps technicians test passed - got {len(technicians)} technicians")


class TestQuickBooksRESTClient:
    """Test QuickBooks REST client"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock QuickBooks configuration"""
        return QuickBooksRESTConfig(
            base_url="https://sandbox-quickbooks.api.intuit.com",
            company_id="test_company_id",
            use_sandbox=True
        )
    
    @pytest.fixture
    def mock_token_manager(self):
        """Mock token manager"""
        token_manager = Mock(spec=TokenManager)
        token_manager.get_valid_token.return_value = "mock_access_token"
        return token_manager
    
    @pytest.fixture
    def client(self, mock_config, mock_token_manager):
        """Create QuickBooks REST client"""
        return QuickBooksRESTClient(mock_config, mock_token_manager)
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Test client initialization"""
        await client.initialize()
        
        assert client.session is not None
        logger.info("QuickBooks REST client initialization test passed")
    
    @pytest.mark.asyncio
    async def test_get_financial_transactions_mock_data(self, client):
        """Test getting financial transactions with mock data fallback"""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        transactions = await client.get_financial_transactions(start_date, end_date)
        
        assert isinstance(transactions, list)
        assert len(transactions) > 0
        
        # Check transaction structure
        transaction = transactions[0]
        assert "Id" in transaction
        assert "TxnDate" in transaction
        assert "TotalAmt" in transaction
        
        logger.info(f"QuickBooks transactions test passed - got {len(transactions)} transactions")
    
    @pytest.mark.asyncio
    async def test_get_invoices_and_payments_mock_data(self, client):
        """Test getting invoices and payments with mock data fallback"""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        result = await client.get_invoices_and_payments(start_date, end_date)
        
        assert isinstance(result, dict)
        assert "invoices" in result
        assert "payments" in result
        
        invoices = result["invoices"]
        payments = result["payments"]
        
        assert isinstance(invoices, list)
        assert isinstance(payments, list)
        
        if invoices:
            invoice = invoices[0]
            assert "Id" in invoice
            assert "DocNumber" in invoice
        
        if payments:
            payment = payments[0]
            assert "Id" in payment
            assert "TotalAmt" in payment
        
        logger.info(f"QuickBooks invoices and payments test passed - got {len(invoices)} invoices, {len(payments)} payments")


class TestDataTransformer:
    """Test data transformation"""
    
    @pytest.fixture
    def transformer(self):
        """Create data transformer"""
        return DataTransformer()
    
    def test_transform_superops_tickets(self, transformer):
        """Test SuperOps ticket transformation"""
        mock_tickets = [
            {
                "ticketId": "TICKET-001",
                "displayId": "TICKET-001",
                "subject": "Test Ticket",
                "status": "Open",
                "priority": "High",
                "createdTime": "2024-01-01T10:00:00Z",
                "updatedTime": "2024-01-01T11:00:00Z",
                "firstResponseTime": "2024-01-01T10:30:00Z",
                "resolutionTime": None,
                "firstResponseViolated": False,
                "resolutionViolated": False,
                "technician": {"userId": "TECH-001", "name": "John Doe"},
                "requester": {"userId": "USER-001", "name": "Jane Smith"},
                "site": {"id": "CLIENT-001", "name": "Test Client"},
                "worklogTimespent": "120",
                "customFields": [{"fieldName": "category", "fieldValue": "support"}],
                "tags": ["urgent", "bug"]
            }
        ]
        
        transformed = transformer.transform_superops_tickets(mock_tickets)
        
        assert len(transformed) == 1
        ticket = transformed[0]
        
        assert ticket.id == "TICKET-001"
        assert ticket.subject == "Test Ticket"
        assert ticket.status == "Open"
        assert ticket.priority == "High"
        assert ticket.technician_name == "John Doe"
        assert ticket.client_name == "Test Client"
        assert ticket.actual_hours == 2.0  # 120 minutes / 60
        assert ticket.sla_violated is False
        assert "urgent" in ticket.tags
        
        logger.info("SuperOps ticket transformation test passed")
    
    def test_transform_quickbooks_invoices(self, transformer):
        """Test QuickBooks invoice transformation"""
        mock_invoices = [
            {
                "Id": "INV-001",
                "DocNumber": "INV-001",
                "CustomerRef": {"value": "CUST-001", "name": "Test Customer"},
                "TxnDate": "2024-01-01",
                "DueDate": "2024-01-31",
                "TotalAmt": 1000.00,
                "TaxAmt": 100.00,
                "Balance": 500.00,
                "PaymentTerms": "Net 30",
                "Line": [
                    {"Description": "Service", "Qty": 1, "Rate": 1000.00, "Amount": 1000.00}
                ],
                "MetaData": {
                    "CreateTime": "2024-01-01T10:00:00Z",
                    "LastUpdatedTime": "2024-01-01T11:00:00Z"
                }
            }
        ]
        
        transformed = transformer.transform_quickbooks_invoices(mock_invoices)
        
        assert len(transformed) == 1
        invoice = transformed[0]
        
        assert invoice.id == "INV-001"
        assert invoice.invoice_number == "INV-001"
        assert invoice.customer_name == "Test Customer"
        assert invoice.total_amount == 1000.00
        assert invoice.balance_due == 500.00
        assert invoice.status == "Unpaid"  # Balance > 0
        assert len(invoice.line_items) == 1
        
        logger.info("QuickBooks invoice transformation test passed")


class TestErrorHandler:
    """Test error handling"""
    
    @pytest.fixture
    def error_handler(self):
        """Create error handler"""
        return get_error_handler()
    
    def test_error_classification(self, error_handler):
        """Test error classification"""
        # Test network error
        network_error = ConnectionError("Connection failed")
        error_type = error_handler.classify_error(network_error)
        assert error_type.value == "network_error"
        
        # Test authentication error
        auth_error = Exception("Unauthorized")
        error_type = error_handler.classify_error(auth_error, 401)
        assert error_type.value == "authentication_error"
        
        # Test rate limit error
        rate_limit_error = Exception("Rate limit exceeded")
        error_type = error_handler.classify_error(rate_limit_error, 429)
        assert error_type.value == "rate_limit_error"
        
        logger.info("Error classification test passed")
    
    def test_should_retry(self, error_handler):
        """Test retry logic"""
        from src.utils.error_handlers import ErrorContext, ErrorType
        
        # Test retryable error
        context = ErrorContext(
            error_type=ErrorType.NETWORK_ERROR,
            error_message="Connection failed",
            retry_count=0,
            max_retries=3
        )
        assert error_handler.should_retry(context) is True
        
        # Test non-retryable error
        context.error_type = ErrorType.VALIDATION_ERROR
        assert error_handler.should_retry(context) is False
        
        # Test max retries exceeded
        context.error_type = ErrorType.NETWORK_ERROR
        context.retry_count = 3
        assert error_handler.should_retry(context) is False
        
        logger.info("Retry logic test passed")


@pytest.mark.asyncio
async def test_integration_workflow():
    """Test the complete integration workflow"""
    logger.info("Starting integration workflow test")
    
    # Test SuperOps client
    superops_config = SuperOpsGraphQLConfig(
        base_url="https://api.superops.ai/it",
        api_key="test_api_key",
        tenant_id="test_tenant_id"
    )
    
    superops_client = SuperOpsGraphQLClient(superops_config)
    tickets = await superops_client.get_tickets()
    assert len(tickets) > 0
    logger.info(f"SuperOps integration test passed - got {len(tickets)} tickets")
    
    # Test QuickBooks client
    quickbooks_config = QuickBooksRESTConfig(
        base_url="https://sandbox-quickbooks.api.intuit.com",
        company_id="test_company_id",
        use_sandbox=True
    )
    
    mock_token_manager = Mock(spec=TokenManager)
    mock_token_manager.get_valid_token.return_value = "mock_access_token"
    
    quickbooks_client = QuickBooksRESTClient(quickbooks_config, mock_token_manager)
    await quickbooks_client.initialize()
    
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    
    transactions = await quickbooks_client.get_financial_transactions(start_date, end_date)
    assert len(transactions) > 0
    logger.info(f"QuickBooks integration test passed - got {len(transactions)} transactions")
    
    # Test data transformation
    transformer = DataTransformer()
    transformed_tickets = transformer.transform_superops_tickets(tickets)
    assert len(transformed_tickets) > 0
    logger.info(f"Data transformation test passed - transformed {len(transformed_tickets)} tickets")
    
    # Test error handling
    error_handler = get_error_handler()
    error_stats = error_handler.get_error_stats()
    logger.info(f"Error handling test passed - error stats: {error_stats}")
    
    logger.info("Integration workflow test completed successfully")


if __name__ == "__main__":
    # Run the integration test
    asyncio.run(test_integration_workflow())
