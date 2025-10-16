# API Analysis: SuperOps & QuickBooks Integration

## Overview
This document provides a detailed analysis of the SuperOps and QuickBooks APIs based on their official documentation, and outlines the implementation strategy for real API integration.

## SuperOps API

### Architecture
- **Type**: GraphQL API
- **Base URLs**:
  - US Data Center: `https://api.superops.ai/it`
  - EU Data Center: `https://euapi.superops.ai/it`
- **Authentication**: API Key + Tenant ID based

### Key Endpoints for Data Extraction

#### 1. Ticket Data (`getTicketList`)
**Query Structure**:
```graphql
query getTicketList($input: ListInfoInput!) {
  getTicketList(input: $input) {
    tickets {
      ticketId
      displayId
      subject
      status
      priority
      createdTime
      updatedTime
      firstResponseTime
      resolutionTime
      technician { userId, name }
      requester { userId, name }
      site { id, name }
      worklogTimespent
    }
    listInfo {
      page
      pageSize
      hasMore
      totalCount
    }
  }
}
```

**Available Data**:
- Ticket lifecycle metrics (created, updated, resolved times)
- SLA compliance (firstResponseViolated, resolutionViolated)
- Assignment data (technician, techGroup)
- Custom fields support
- Worklog time tracking

#### 2. SLA Metrics (`getSLAList`)
```graphql
query getSLAList {
  getSLAList {
    id
    name
  }
}
```

#### 3. Technician Productivity (`getTechnicianList`)
```graphql
query getTechnicianList($input: ListInfoInput!) {
  getTechnicianList(input: $input) {
    userList {
      userId
      name
      email
      department { departmentId, name }
      groups { groupId, name }
    }
    listInfo {
      page
      pageSize
      totalCount
    }
  }
}
```

#### 4. Client/Site Data (`getSiteList`)
```graphql
query getSiteList($input: ListInfoInput!) {
  getSiteList(input: $input) {
    sites {
      id
      name
      contactNumber
      address {
        line1
        city
        stateCode
        countryCode
      }
    }
    listInfo {
      page
      pageSize
      totalCount
    }
  }
}
```

#### 5. Asset Data (`getAssetList`)
```graphql
query getAssetList($input: ListInfoInput!) {
  getAssetList(input: $input) {
    assets {
      assetId
      name
      site { id, name }
      status
      lastCommunicatedTime
      platformCategory
    }
    listInfo {
      page
      pageSize
      totalCount
    }
  }
}
```

### Filtering & Pagination
SuperOps supports advanced filtering through `RuleConditionInput`:
```json
{
  "page": 1,
  "pageSize": 100,
  "condition": {
    "attribute": "status",
    "operator": "equals",
    "value": "Open"
  },
  "sort": [
    {
      "attribute": "createdTime",
      "order": "DESC"
    }
  ]
}
```

## QuickBooks API

### Architecture
- **Type**: REST API (OAuth 2.0)
- **Base URLs**:
  - Sandbox: `https://sandbox-quickbooks.api.intuit.com`
  - Production: `https://quickbooks.api.intuit.com`
- **Authentication**: OAuth 2.0 with access/refresh tokens

### Key Endpoints for Data Extraction

#### 1. Financial Transactions
**Endpoint**: `GET /v3/company/{companyId}/query`

**Query Examples**:
```sql
SELECT * FROM Invoice WHERE TxnDate >= '2024-01-01' AND TxnDate <= '2024-12-31' MAXRESULTS 1000
SELECT * FROM Payment WHERE TxnDate >= '2024-01-01' MAXRESULTS 1000
SELECT * FROM Bill WHERE TxnDate >= '2024-01-01' MAXRESULTS 1000
```

**Response Structure**:
```json
{
  "QueryResponse": {
    "Invoice": [
      {
        "Id": "123",
        "DocNumber": "INV-1001",
        "TxnDate": "2024-01-15",
        "TotalAmt": 1500.00,
        "Balance": 500.00,
        "CustomerRef": {
          "value": "1",
          "name": "Acme Corp"
        },
        "Line": [
          {
            "Description": "IT Support Services",
            "Amount": 1500.00
          }
        ]
      }
    ],
    "maxResults": 1000
  }
}
```

#### 2. Customer Financial Profiles
**Endpoint**: `GET /v3/company/{companyId}/customer/{customerId}`

**Response**:
```json
{
  "Customer": {
    "Id": "1",
    "DisplayName": "Acme Corp",
    "Balance": 5000.00,
    "BalanceWithJobs": 5000.00,
    "CurrencyRef": {
      "value": "USD"
    },
    "BillAddr": {
      "Line1": "123 Main St",
      "City": "Austin",
      "CountrySubDivisionCode": "TX"
    }
  }
}
```

#### 3. Expense Data
**Endpoint**: `GET /v3/company/{companyId}/query`

```sql
SELECT * FROM Purchase WHERE TxnDate >= '2024-01-01' MAXRESULTS 1000
SELECT * FROM Expense WHERE TxnDate >= '2024-01-01' MAXRESULTS 1000
```

#### 4. Reports API
**Endpoint**: `GET /v3/company/{companyId}/reports/{reportType}`

Available Reports:
- `ProfitAndLoss`
- `BalanceSheet`
- `CashFlow`
- `AgedReceivables`
- `AgedPayables`

### OAuth 2.0 Flow
1. **Authorization**: Redirect user to Intuit OAuth page
2. **Token Exchange**: Exchange authorization code for access/refresh tokens
3. **Token Refresh**: Refresh access token using refresh token (expires in 100 days)

## Implementation Strategy

### Phase 1: Authentication Setup

#### SuperOps Authentication
```python
class SuperOpsAuthConfig:
    base_url: str  # From env
    api_key: str   # From env
    tenant_id: str # From env
    
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-Tenant-Id": self.tenant_id,
            "Content-Type": "application/json"
        }
```

#### QuickBooks OAuth 2.0
```python
class QuickBooksOAuth:
    client_id: str
    client_secret: str
    redirect_uri: str
    
    def get_authorization_url(self):
        # Generate OAuth URL
        pass
    
    def exchange_code_for_tokens(self, code: str):
        # Exchange authorization code for tokens
        pass
    
    def refresh_access_token(self, refresh_token: str):
        # Refresh expired access token
        pass
```

### Phase 2: GraphQL Client for SuperOps

```python
import aiohttp
from typing import Dict, Any, List

class SuperOpsGraphQLClient:
    def __init__(self, config: SuperOpsAuthConfig):
        self.config = config
        self.session = None
    
    async def execute_query(self, query: str, variables: Dict = None):
        """Execute GraphQL query"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.config.base_url,
                headers=self.config.get_headers(),
                json={
                    "query": query,
                    "variables": variables or {}
                }
            ) as response:
                return await response.json()
    
    async def get_tickets(self, page: int = 1, page_size: int = 100, 
                          filters: Dict = None):
        """Fetch tickets with pagination and filtering"""
        query = """
        query getTicketList($input: ListInfoInput!) {
          getTicketList(input: $input) {
            tickets {
              ticketId
              displayId
              subject
              status
              priority
              createdTime
              updatedTime
              firstResponseTime
              resolutionTime
              firstResponseViolated
              resolutionViolated
              technician { userId name }
              requester { userId name }
              site { id name }
              worklogTimespent
            }
            listInfo {
              page
              pageSize
              hasMore
              totalCount
            }
          }
        }
        """
        
        variables = {
            "input": {
                "page": page,
                "pageSize": page_size,
                "condition": filters
            }
        }
        
        return await self.execute_query(query, variables)
```

### Phase 3: REST Client for QuickBooks

```python
import aiohttp
from typing import Dict, Any, List

class QuickBooksRESTClient:
    def __init__(self, config: QuickBooksConfig, oauth: QuickBooksOAuth):
        self.config = config
        self.oauth = oauth
        self.access_token = None
    
    async def _ensure_valid_token(self):
        """Ensure we have a valid access token"""
        if not self.access_token or self._is_token_expired():
            self.access_token = await self.oauth.refresh_access_token()
    
    async def _make_request(self, method: str, endpoint: str, 
                           params: Dict = None, data: Dict = None):
        """Make authenticated request to QuickBooks API"""
        await self._ensure_valid_token()
        
        url = f"{self.config.base_url}/v3/company/{self.config.company_id}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, headers=headers, 
                params=params, json=data
            ) as response:
                return await response.json()
    
    async def query(self, sql_query: str):
        """Execute SQL-like query"""
        return await self._make_request(
            "GET", "/query",
            params={"query": sql_query}
        )
    
    async def get_invoices(self, start_date: str, end_date: str):
        """Fetch invoices within date range"""
        query = f"""
        SELECT * FROM Invoice 
        WHERE TxnDate >= '{start_date}' 
        AND TxnDate <= '{end_date}' 
        MAXRESULTS 1000
        """
        return await self.query(query)
```

### Phase 4: Data Transformation Layer

```python
class DataTransformer:
    """Transform API responses to unified format"""
    
    @staticmethod
    def transform_superops_tickets(raw_data: Dict) -> List[Dict]:
        """Transform SuperOps ticket data to standard format"""
        tickets = raw_data.get("data", {}).get("getTicketList", {}).get("tickets", [])
        
        transformed = []
        for ticket in tickets:
            transformed.append({
                "id": ticket["ticketId"],
                "display_id": ticket["displayId"],
                "subject": ticket["subject"],
                "status": ticket["status"],
                "priority": ticket["priority"],
                "created_at": ticket["createdTime"],
                "updated_at": ticket["updatedTime"],
                "first_response_time": ticket.get("firstResponseTime"),
                "resolution_time": ticket.get("resolutionTime"),
                "sla_violated": ticket.get("firstResponseViolated") or ticket.get("resolutionViolated"),
                "technician": ticket.get("technician", {}).get("name"),
                "requester": ticket.get("requester", {}).get("name"),
                "site": ticket.get("site", {}).get("name"),
                "time_spent_minutes": float(ticket.get("worklogTimespent", 0))
            })
        
        return transformed
    
    @staticmethod
    def transform_quickbooks_invoices(raw_data: Dict) -> List[Dict]:
        """Transform QuickBooks invoice data to standard format"""
        invoices = raw_data.get("QueryResponse", {}).get("Invoice", [])
        
        transformed = []
        for invoice in invoices:
            transformed.append({
                "id": invoice["Id"],
                "invoice_number": invoice["DocNumber"],
                "date": invoice["TxnDate"],
                "total_amount": invoice["TotalAmt"],
                "balance_due": invoice["Balance"],
                "customer_id": invoice["CustomerRef"]["value"],
                "customer_name": invoice["CustomerRef"]["name"],
                "status": "Paid" if invoice["Balance"] == 0 else "Unpaid",
                "line_items": [
                    {
                        "description": line.get("Description", ""),
                        "amount": line.get("Amount", 0)
                    }
                    for line in invoice.get("Line", [])
                ]
            })
        
        return transformed
```

### Phase 5: Unified Data Extractor

```python
class UnifiedDataExtractor:
    """Unified interface for extracting data from all sources"""
    
    def __init__(self):
        self.superops_client = SuperOpsGraphQLClient(superops_config)
        self.quickbooks_client = QuickBooksRESTClient(qb_config, qb_oauth)
        self.internal_db = InternalDBConnector(db_config)
        self.transformer = DataTransformer()
    
    async def extract_ticket_metrics(self, start_date: str, end_date: str):
        """Extract ticket metrics from SuperOps"""
        # Fetch tickets
        raw_tickets = await self.superops_client.get_tickets(
            filters={
                "attribute": "createdTime",
                "operator": "between",
                "value": [start_date, end_date]
            }
        )
        
        # Transform to standard format
        tickets = self.transformer.transform_superops_tickets(raw_tickets)
        
        # Calculate metrics
        metrics = {
            "total_tickets": len(tickets),
            "avg_resolution_time": self._calculate_avg_resolution_time(tickets),
            "sla_compliance_rate": self._calculate_sla_compliance(tickets),
            "tickets_by_priority": self._group_by_priority(tickets)
        }
        
        return metrics
    
    async def extract_financial_data(self, start_date: str, end_date: str):
        """Extract financial data from QuickBooks"""
        # Fetch invoices and payments in parallel
        invoices_task = self.quickbooks_client.get_invoices(start_date, end_date)
        payments_task = self.quickbooks_client.get_payments(start_date, end_date)
        
        invoices_raw, payments_raw = await asyncio.gather(
            invoices_task, payments_task
        )
        
        # Transform data
        invoices = self.transformer.transform_quickbooks_invoices(invoices_raw)
        payments = self.transformer.transform_quickbooks_payments(payments_raw)
        
        # Calculate metrics
        metrics = {
            "total_revenue": sum(inv["total_amount"] for inv in invoices),
            "outstanding_balance": sum(inv["balance_due"] for inv in invoices),
            "payment_collection_rate": self._calculate_collection_rate(invoices, payments)
        }
        
        return metrics
```

## Key Differences from Mock Implementation

### 1. Authentication
- **Mock**: No authentication required
- **Real**: 
  - SuperOps: API Key + Tenant ID in headers
  - QuickBooks: OAuth 2.0 with token refresh

### 2. API Structure
- **Mock**: Simple REST-like calls
- **Real**:
  - SuperOps: GraphQL with complex query structure
  - QuickBooks: REST with SQL-like query language

### 3. Pagination
- **Mock**: Simple limit/offset
- **Real**:
  - SuperOps: Page-based with hasMore indicator
  - QuickBooks: MAXRESULTS in query + startPosition

### 4. Error Handling
- **Mock**: Basic try-catch
- **Real**: Need to handle:
  - Token expiration (QuickBooks)
  - Rate limiting (both APIs)
  - GraphQL errors (SuperOps)
  - Network timeouts
  - Invalid queries

### 5. Data Validation
- **Mock**: Minimal validation
- **Real**: Need comprehensive validation:
  - Schema validation for GraphQL responses
  - OAuth token validation
  - Date format validation
  - Company ID validation (QuickBooks)
  - Tenant ID validation (SuperOps)

## Next Steps

1. **Environment Setup**
   - Create `.env` file with real API credentials
   - Set up OAuth callback endpoint for QuickBooks
   - Configure tenant ID for SuperOps

2. **Update Configuration**
   - Add OAuth-specific config fields
   - Add GraphQL endpoint configuration
   - Add token storage mechanism

3. **Implement Real Clients**
   - Replace mock SuperOps client with GraphQL client
   - Replace mock QuickBooks client with OAuth-enabled REST client
   - Update internal DB connector if needed

4. **Add OAuth Flow**
   - Create OAuth authorization endpoint
   - Implement token exchange
   - Implement token refresh mechanism
   - Add token storage (database or secure cache)

5. **Update Data Transformers**
   - Map actual API response fields to internal schema
   - Handle missing/optional fields
   - Add data validation

6. **Testing**
   - Test with real API credentials in sandbox
   - Verify OAuth flow
   - Test pagination with large datasets
   - Test error scenarios

## Security Considerations

1. **Credential Storage**
   - Store API keys in environment variables
   - Encrypt tokens in database
   - Use secure token storage mechanism

2. **Token Management**
   - Implement token rotation
   - Handle token expiration gracefully
   - Log token refresh events

3. **API Rate Limiting**
   - Implement exponential backoff
   - Add request queuing
   - Monitor rate limit headers

4. **Data Privacy**
   - Mask sensitive data in logs
   - Implement data retention policies
   - Add audit logging

## Conclusion

The real API integration requires significant changes from the mock implementation:
- GraphQL client for SuperOps instead of simple REST
- OAuth 2.0 flow for QuickBooks authentication
- Complex query structures and pagination
- Robust error handling and token management

This document serves as the blueprint for implementing the real API integration.

