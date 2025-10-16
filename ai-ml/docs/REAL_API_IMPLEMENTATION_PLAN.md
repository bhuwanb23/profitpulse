# Real API Implementation Plan

## Overview
This document outlines the step-by-step plan to replace mock data implementations with real API integrations for SuperOps (GraphQL) and QuickBooks (REST with OAuth 2.0).

## Current State Analysis

### What's Working (Mock Implementation)
✅ Basic client structure with async methods
✅ Data extraction methods defined
✅ Configuration management with Pydantic
✅ Rate limiting and retry logic structure
✅ Comprehensive data extractor orchestration

### What Needs to Change
❌ No real authentication (API keys not used)
❌ Mock data generation instead of API calls
❌ No GraphQL query construction (SuperOps)
❌ No OAuth 2.0 flow (QuickBooks)
❌ No token management and refresh
❌ No real error handling for API-specific errors
❌ No data transformation from actual API responses

## Implementation Phases

### Phase 1: Infrastructure Setup
**Duration**: 1-2 days

#### 1.1 Environment Configuration
- [ ] Create `.env.example` with all required variables
- [ ] Document how to obtain API credentials
- [ ] Set up credential validation on startup
- [ ] Add environment-specific configs (dev/staging/prod)

**Required Environment Variables**:
```bash
# SuperOps Configuration
SUPEROPS_API_BASE_URL=https://api.superops.ai/it
SUPEROPS_API_KEY=your_api_key_here
SUPEROPS_TENANT_ID=your_tenant_id_here

# QuickBooks Configuration
QUICKBOOKS_CLIENT_ID=your_client_id_here
QUICKBOOKS_CLIENT_SECRET=your_client_secret_here
QUICKBOOKS_REDIRECT_URI=http://localhost:8000/auth/quickbooks/callback
QUICKBOOKS_COMPANY_ID=your_company_id_here
QUICKBOOKS_USE_SANDBOX=true
```

#### 1.2 Dependency Installation
- [ ] Add `aiohttp` for async HTTP requests
- [ ] Add `gql` for GraphQL client (SuperOps)
- [ ] Add `authlib` for OAuth 2.0 (QuickBooks)
- [ ] Add `python-jose` for JWT token handling
- [ ] Add `cryptography` for token encryption

**Update requirements.txt**:
```txt
aiohttp==3.9.1
gql[aiohttp]==3.4.1
authlib==1.3.0
python-jose[cryptography]==3.3.0
cryptography==41.0.7
```

#### 1.3 Token Storage Setup
- [ ] Create database schema for OAuth tokens
- [ ] Implement encrypted token storage
- [ ] Add token retrieval methods
- [ ] Implement token cleanup for expired tokens

**Database Schema**:
```sql
CREATE TABLE oauth_tokens (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_type VARCHAR(50),
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Phase 2: SuperOps GraphQL Integration
**Duration**: 3-4 days

#### 2.1 GraphQL Client Implementation
- [ ] Create GraphQL client using `gql` library
- [ ] Implement query builder for common queries
- [ ] Add authentication headers
- [ ] Implement connection pooling
- [ ] Add request/response logging

**File**: `ai-ml/src/data/superops_graphql_client.py`
```python
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class SuperOpsGraphQLClient:
    def __init__(self, config):
        self.config = config
        self.transport = AIOHTTPTransport(
            url=config.base_url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "X-Tenant-Id": config.tenant_id
            }
        )
        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=True
        )
```

#### 2.2 Query Templates
- [ ] Create ticket list query
- [ ] Create SLA metrics query
- [ ] Create technician productivity query
- [ ] Create site/client data query
- [ ] Create asset data query

**File**: `ai-ml/src/data/superops_queries.py`
```python
GET_TICKETS_QUERY = gql("""
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
""")
```

#### 2.3 Response Transformation
- [ ] Create Pydantic models for API responses
- [ ] Implement transformation to internal format
- [ ] Add validation for required fields
- [ ] Handle missing/null fields gracefully

**File**: `ai-ml/src/data/superops_models.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SuperOpsTicket(BaseModel):
    ticketId: str
    displayId: str
    subject: str
    status: str
    priority: Optional[str]
    createdTime: datetime
    updatedTime: datetime
    firstResponseTime: Optional[datetime]
    resolutionTime: Optional[datetime]
    firstResponseViolated: Optional[bool]
    resolutionViolated: Optional[bool]
    technician: Optional[dict]
    requester: Optional[dict]
    site: Optional[dict]
    worklogTimespent: Optional[str]
```

#### 2.4 Update SuperOps Client
- [ ] Replace mock methods with real GraphQL calls
- [ ] Implement pagination handling
- [ ] Add filtering support
- [ ] Implement error handling for GraphQL errors
- [ ] Add retry logic for failed queries

### Phase 3: QuickBooks OAuth 2.0 Integration
**Duration**: 4-5 days

#### 3.1 OAuth Flow Implementation
- [ ] Create OAuth authorization endpoint
- [ ] Implement authorization URL generation
- [ ] Create callback endpoint
- [ ] Implement token exchange
- [ ] Add token refresh mechanism
- [ ] Implement token revocation

**File**: `ai-ml/src/auth/quickbooks_oauth.py`
```python
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client import OAuthError

class QuickBooksOAuth:
    def __init__(self, config):
        self.config = config
        self.oauth = OAuth()
        self.oauth.register(
            name='quickbooks',
            client_id=config.client_id,
            client_secret=config.client_secret,
            authorize_url='https://appcenter.intuit.com/connect/oauth2',
            access_token_url='https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer',
            redirect_uri=config.redirect_uri,
            client_kwargs={'scope': 'com.intuit.quickbooks.accounting'}
        )
    
    async def get_authorization_url(self):
        """Generate OAuth authorization URL"""
        pass
    
    async def exchange_code_for_tokens(self, code: str):
        """Exchange authorization code for tokens"""
        pass
    
    async def refresh_access_token(self, refresh_token: str):
        """Refresh expired access token"""
        pass
```

#### 3.2 Token Management
- [ ] Implement token storage in database
- [ ] Add token encryption/decryption
- [ ] Create token refresh scheduler
- [ ] Add token validation
- [ ] Implement token cleanup job

**File**: `ai-ml/src/auth/token_manager.py`
```python
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self, encryption_key: str):
        self.cipher = Fernet(encryption_key.encode())
    
    async def store_token(self, provider: str, access_token: str, 
                         refresh_token: str, expires_in: int):
        """Store encrypted tokens in database"""
        pass
    
    async def get_valid_token(self, provider: str):
        """Get valid access token, refresh if needed"""
        pass
    
    async def refresh_token(self, provider: str):
        """Refresh access token using refresh token"""
        pass
```

#### 3.3 REST Client Implementation
- [ ] Create authenticated HTTP client
- [ ] Implement query method for SQL-like queries
- [ ] Add entity-specific methods (invoices, payments, etc.)
- [ ] Implement pagination handling
- [ ] Add error handling for API errors

**File**: `ai-ml/src/data/quickbooks_rest_client.py`
```python
import aiohttp
from typing import Dict, Any

class QuickBooksRESTClient:
    def __init__(self, config, token_manager):
        self.config = config
        self.token_manager = token_manager
    
    async def _make_request(self, method: str, endpoint: str, 
                           params: Dict = None, data: Dict = None):
        """Make authenticated request"""
        token = await self.token_manager.get_valid_token('quickbooks')
        
        url = f"{self.config.base_url}/v3/company/{self.config.company_id}{endpoint}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, headers=headers,
                params=params, json=data
            ) as response:
                if response.status == 401:
                    # Token expired, refresh and retry
                    await self.token_manager.refresh_token('quickbooks')
                    return await self._make_request(method, endpoint, params, data)
                
                response.raise_for_status()
                return await response.json()
```

#### 3.4 Update QuickBooks Client
- [ ] Replace mock methods with real API calls
- [ ] Implement SQL query construction
- [ ] Add response parsing
- [ ] Implement error handling
- [ ] Add retry logic

### Phase 4: Data Transformation Layer
**Duration**: 2-3 days

#### 4.1 Create Transformation Models
- [ ] Define internal data models
- [ ] Create transformation functions
- [ ] Add validation logic
- [ ] Handle data type conversions
- [ ] Implement null/missing value handling

**File**: `ai-ml/src/data/transformers.py`
```python
from typing import List, Dict, Any
from datetime import datetime

class DataTransformer:
    @staticmethod
    def transform_superops_tickets(raw_data: Dict) -> List[Dict]:
        """Transform SuperOps ticket data"""
        tickets = raw_data.get("data", {}).get("getTicketList", {}).get("tickets", [])
        
        transformed = []
        for ticket in tickets:
            transformed.append({
                "id": ticket["ticketId"],
                "display_id": ticket["displayId"],
                "subject": ticket["subject"],
                "status": ticket["status"],
                "priority": ticket.get("priority"),
                "created_at": datetime.fromisoformat(ticket["createdTime"]),
                "updated_at": datetime.fromisoformat(ticket["updatedTime"]),
                "first_response_time": datetime.fromisoformat(ticket["firstResponseTime"]) if ticket.get("firstResponseTime") else None,
                "resolution_time": datetime.fromisoformat(ticket["resolutionTime"]) if ticket.get("resolutionTime") else None,
                "sla_violated": ticket.get("firstResponseViolated") or ticket.get("resolutionViolated"),
                "technician": ticket.get("technician", {}).get("name"),
                "requester": ticket.get("requester", {}).get("name"),
                "site": ticket.get("site", {}).get("name"),
                "time_spent_minutes": float(ticket.get("worklogTimespent", 0))
            })
        
        return transformed
    
    @staticmethod
    def transform_quickbooks_invoices(raw_data: Dict) -> List[Dict]:
        """Transform QuickBooks invoice data"""
        invoices = raw_data.get("QueryResponse", {}).get("Invoice", [])
        
        transformed = []
        for invoice in invoices:
            transformed.append({
                "id": invoice["Id"],
                "invoice_number": invoice["DocNumber"],
                "date": datetime.strptime(invoice["TxnDate"], "%Y-%m-%d"),
                "total_amount": float(invoice["TotalAmt"]),
                "balance_due": float(invoice["Balance"]),
                "customer_id": invoice["CustomerRef"]["value"],
                "customer_name": invoice["CustomerRef"]["name"],
                "status": "Paid" if float(invoice["Balance"]) == 0 else "Unpaid",
                "line_items": [
                    {
                        "description": line.get("Description", ""),
                        "amount": float(line.get("Amount", 0))
                    }
                    for line in invoice.get("Line", [])
                ]
            })
        
        return transformed
```

#### 4.2 Update Comprehensive Extractor
- [ ] Integrate real clients
- [ ] Update data extraction methods
- [ ] Add transformation calls
- [ ] Implement error aggregation
- [ ] Add data quality checks

### Phase 5: Error Handling & Resilience
**Duration**: 2-3 days

#### 5.1 API-Specific Error Handling
- [ ] Handle GraphQL errors (SuperOps)
- [ ] Handle OAuth errors (QuickBooks)
- [ ] Handle rate limiting
- [ ] Implement circuit breaker pattern
- [ ] Add fallback mechanisms

**File**: `ai-ml/src/utils/error_handlers.py`
```python
from typing import Callable
import asyncio

class APIErrorHandler:
    @staticmethod
    async def with_retry(func: Callable, max_retries: int = 3, 
                        backoff_factor: float = 2.0):
        """Execute function with exponential backoff retry"""
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                wait_time = backoff_factor ** attempt
                await asyncio.sleep(wait_time)
    
    @staticmethod
    def handle_graphql_errors(response: Dict):
        """Handle GraphQL-specific errors"""
        if "errors" in response:
            errors = response["errors"]
            # Log and handle errors
            raise GraphQLError(errors)
    
    @staticmethod
    def handle_oauth_errors(response: Dict):
        """Handle OAuth-specific errors"""
        if "error" in response:
            error_code = response["error"]
            # Handle different OAuth error codes
            raise OAuthError(error_code)
```

#### 5.2 Logging & Monitoring
- [ ] Add structured logging
- [ ] Implement request/response logging
- [ ] Add performance metrics
- [ ] Create error tracking
- [ ] Add alerting for critical errors

### Phase 6: Testing & Validation
**Duration**: 3-4 days

#### 6.1 Unit Tests
- [ ] Test GraphQL client
- [ ] Test OAuth flow
- [ ] Test token management
- [ ] Test data transformation
- [ ] Test error handling

#### 6.2 Integration Tests
- [ ] Test end-to-end data extraction
- [ ] Test with real sandbox APIs
- [ ] Test pagination
- [ ] Test error scenarios
- [ ] Test token refresh

#### 6.3 Performance Tests
- [ ] Test with large datasets
- [ ] Test concurrent requests
- [ ] Test rate limiting
- [ ] Measure response times
- [ ] Optimize slow queries

### Phase 7: Documentation & Deployment
**Duration**: 2 days

#### 7.1 Documentation
- [ ] Update API documentation
- [ ] Create setup guide
- [ ] Document OAuth flow
- [ ] Add troubleshooting guide
- [ ] Create API usage examples

#### 7.2 Deployment
- [ ] Set up production environment
- [ ] Configure production credentials
- [ ] Deploy OAuth callback endpoint
- [ ] Set up monitoring
- [ ] Create deployment checklist

## Testing Strategy

### Sandbox Testing
1. **SuperOps Sandbox**
   - Request sandbox access from SuperOps
   - Create test tenant
   - Generate test data

2. **QuickBooks Sandbox**
   - Use QuickBooks sandbox environment
   - Create test company
   - Generate test transactions

### Test Scenarios
1. **Happy Path**
   - Successful data extraction
   - Proper pagination
   - Correct data transformation

2. **Error Scenarios**
   - Invalid credentials
   - Expired tokens
   - Rate limiting
   - Network failures
   - Invalid queries

3. **Edge Cases**
   - Empty responses
   - Large datasets
   - Missing fields
   - Null values

## Rollout Plan

### Phase 1: Development Environment
- Set up with sandbox credentials
- Test all functionality
- Fix bugs and issues

### Phase 2: Staging Environment
- Deploy to staging
- Test with production-like data
- Performance testing
- Security audit

### Phase 3: Production Rollout
- Deploy to production
- Monitor closely
- Gradual rollout
- Rollback plan ready

## Success Criteria

### Functional Requirements
✅ Successfully authenticate with both APIs
✅ Extract all required data types
✅ Transform data correctly
✅ Handle pagination properly
✅ Manage tokens automatically

### Non-Functional Requirements
✅ Response time < 5 seconds for typical queries
✅ Handle 1000+ records efficiently
✅ 99.9% uptime
✅ Proper error logging
✅ Secure credential storage

## Risk Mitigation

### Technical Risks
1. **API Changes**
   - Mitigation: Version pinning, monitoring for deprecations

2. **Rate Limiting**
   - Mitigation: Implement queuing, caching, batch requests

3. **Token Expiration**
   - Mitigation: Proactive refresh, fallback mechanisms

4. **Data Quality**
   - Mitigation: Validation, data quality checks, alerts

### Operational Risks
1. **Credential Leakage**
   - Mitigation: Encryption, access controls, audit logging

2. **Service Downtime**
   - Mitigation: Circuit breakers, fallbacks, monitoring

3. **Data Loss**
   - Mitigation: Backups, transaction logs, recovery procedures

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Infrastructure Setup | 1-2 days | None |
| SuperOps Integration | 3-4 days | Phase 1 |
| QuickBooks Integration | 4-5 days | Phase 1 |
| Data Transformation | 2-3 days | Phase 2, 3 |
| Error Handling | 2-3 days | Phase 2, 3, 4 |
| Testing | 3-4 days | All previous |
| Documentation | 2 days | All previous |

**Total Estimated Time**: 17-23 days

## Next Immediate Steps

1. ✅ Create API analysis document (DONE)
2. ✅ Create implementation plan (DONE)
3. ⏭️ Set up environment variables
4. ⏭️ Install required dependencies
5. ⏭️ Implement SuperOps GraphQL client
6. ⏭️ Implement QuickBooks OAuth flow
7. ⏭️ Update comprehensive extractor
8. ⏭️ Add comprehensive testing

## Conclusion

This implementation plan provides a structured approach to replacing mock implementations with real API integrations. The phased approach allows for incremental development and testing, reducing risk and ensuring quality at each step.

The key challenges are:
- OAuth 2.0 implementation for QuickBooks
- GraphQL query construction for SuperOps
- Token management and refresh
- Error handling for API-specific errors
- Data transformation from diverse API formats

By following this plan systematically, we can achieve a robust, production-ready integration with both SuperOps and QuickBooks APIs.

