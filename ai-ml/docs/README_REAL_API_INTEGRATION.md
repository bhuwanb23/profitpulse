# Real API Integration Guide

## 🎯 Purpose

This document explains the current state of the AI/ML data ingestion system and provides guidance on transitioning from **mock data** to **real API integration** with SuperOps and QuickBooks.

## 📋 Table of Contents

1. [Current Status](#current-status)
2. [Understanding the Gap](#understanding-the-gap)
3. [Quick Start (Mock Data)](#quick-start-mock-data)
4. [Real API Integration](#real-api-integration)
5. [Documentation](#documentation)
6. [FAQs](#faqs)

## 🔍 Current Status

### What Works Today ✅

The current implementation provides a **fully functional mock data system** that:

- ✅ Simulates SuperOps API (tickets, SLA metrics, technician data, etc.)
- ✅ Simulates QuickBooks API (invoices, payments, expenses, customers)
- ✅ Simulates Internal Database (client profiles, service history, satisfaction scores)
- ✅ Provides realistic mock data for development and testing
- ✅ Implements proper async/await patterns
- ✅ Includes rate limiting and retry logic
- ✅ Has comprehensive data models and transformers
- ✅ Includes pagination support
- ✅ Has error handling structure

### What Doesn't Work (Yet) ❌

The current implementation **does NOT**:

- ❌ Connect to real SuperOps API
- ❌ Connect to real QuickBooks API
- ❌ Use actual API credentials
- ❌ Implement OAuth 2.0 flow (required for QuickBooks)
- ❌ Implement GraphQL client (required for SuperOps)
- ❌ Store or refresh authentication tokens
- ❌ Transform real API responses

## 🔑 Understanding the Gap

### Why Mock Data?

The implementation uses mock data because:

1. **No API Credentials**: Real integration requires API keys and OAuth setup
2. **Complex Authentication**: QuickBooks requires OAuth 2.0 with callback endpoints
3. **Different API Types**: SuperOps uses GraphQL, QuickBooks uses REST
4. **Development Speed**: Mock data allows rapid development without external dependencies
5. **Testing**: Mock data provides consistent, predictable test scenarios

### What's the Difference?

| Feature | Mock Implementation | Real Implementation |
|---------|-------------------|---------------------|
| **Data Source** | Generated locally | Live API responses |
| **Authentication** | None | API Keys + OAuth 2.0 |
| **API Type** | Simulated REST | GraphQL + REST |
| **Setup Time** | Minutes | Days/Weeks |
| **Dependencies** | None | API credentials, OAuth setup |
| **Cost** | Free | API usage limits |
| **Reliability** | 100% | Depends on API availability |

## 🚀 Quick Start (Mock Data)

### Prerequisites

```bash
# Python 3.9+
python --version

# Install dependencies
cd ai-ml
pip install -r requirements.txt
```

### Running with Mock Data

```python
import asyncio
from src.data.comprehensive_extractor import create_comprehensive_extractor

async def main():
    # Create extractor (uses mock data by default)
    extractor = create_comprehensive_extractor()
    
    # Extract all data
    data = await extractor.extract_all_data(
        client_id="client_1",
        start_date="2024-01-01",
        end_date="2024-12-31"
    )
    
    print(f"SuperOps Tickets: {len(data['superops_tickets'])}")
    print(f"QuickBooks Transactions: {len(data['quickbooks_transactions'])}")
    print(f"Internal Client Profiles: {len(data['internal_client_profiles'])}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Testing

```bash
# Run Phase 2.1 tests
cd ai-ml
python tests/run_tests.py

# Or run specific test
python tests/test_phase_2_1_complete.py
```

## 🔌 Real API Integration

### Step 1: Understand the Requirements

Read these documents in order:

1. **`summaries/PHASE_2_1_REAL_API_ANALYSIS.md`**
   - Explains the gap between mock and real implementation
   - Lists what's needed for real integration
   - Provides technical details

2. **`docs/API_ANALYSIS.md`**
   - Detailed analysis of SuperOps and QuickBooks APIs
   - API structure and endpoints
   - Authentication methods
   - Data formats

3. **`docs/REAL_API_IMPLEMENTATION_PLAN.md`**
   - Step-by-step implementation guide
   - Timeline estimates (17-23 days)
   - Phase-by-phase breakdown
   - Testing strategy

### Step 2: Obtain API Credentials

#### SuperOps API

1. Log in to your SuperOps account
2. Navigate to Settings → API
3. Generate API key
4. Note your Tenant ID
5. Identify your data center (US or EU)

**Required Information**:
```bash
SUPEROPS_API_BASE_URL=https://api.superops.ai/it  # or EU endpoint
SUPEROPS_API_KEY=your_api_key_here
SUPEROPS_TENANT_ID=your_tenant_id_here
```

#### QuickBooks API

1. Create Intuit Developer account
2. Create new app in Intuit Developer Portal
3. Get Client ID and Client Secret
4. Set up OAuth redirect URI
5. Get Company ID from QuickBooks

**Required Information**:
```bash
QUICKBOOKS_CLIENT_ID=your_client_id_here
QUICKBOOKS_CLIENT_SECRET=your_client_secret_here
QUICKBOOKS_REDIRECT_URI=http://localhost:8000/auth/quickbooks/callback
QUICKBOOKS_COMPANY_ID=your_company_id_here
QUICKBOOKS_USE_SANDBOX=true  # Use sandbox for testing
```

### Step 3: Set Up Environment

Create `.env` file:

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env
```

Example `.env`:
```bash
# SuperOps Configuration
SUPEROPS_API_BASE_URL=https://api.superops.ai/it
SUPEROPS_API_KEY=sk_test_1234567890abcdef
SUPEROPS_TENANT_ID=tenant_abc123

# QuickBooks Configuration
QUICKBOOKS_CLIENT_ID=AB1234567890xyz
QUICKBOOKS_CLIENT_SECRET=1234567890abcdefghijklmnop
QUICKBOOKS_REDIRECT_URI=http://localhost:8000/auth/quickbooks/callback
QUICKBOOKS_COMPANY_ID=123456789
QUICKBOOKS_USE_SANDBOX=true

# Database Configuration (for token storage)
DATABASE_URL=postgresql://user:password@localhost:5432/profitpulse
```

### Step 4: Install Additional Dependencies

```bash
# Install real API dependencies
pip install aiohttp gql[aiohttp] authlib python-jose[cryptography] cryptography

# Update requirements.txt
pip freeze > requirements.txt
```

### Step 5: Follow Implementation Plan

Follow the phases in `docs/REAL_API_IMPLEMENTATION_PLAN.md`:

1. **Phase 1**: Infrastructure Setup (1-2 days)
2. **Phase 2**: SuperOps GraphQL Integration (3-4 days)
3. **Phase 3**: QuickBooks OAuth Integration (4-5 days)
4. **Phase 4**: Data Transformation Layer (2-3 days)
5. **Phase 5**: Error Handling & Resilience (2-3 days)
6. **Phase 6**: Testing & Validation (3-4 days)
7. **Phase 7**: Documentation & Deployment (2 days)

### Step 6: Test with Sandbox

```python
# Test SuperOps connection
from src.data.superops_graphql_client import SuperOpsGraphQLClient

async def test_superops():
    client = SuperOpsGraphQLClient(config)
    tickets = await client.get_tickets(page=1, page_size=10)
    print(f"Retrieved {len(tickets)} tickets")

# Test QuickBooks OAuth
from src.auth.quickbooks_oauth import QuickBooksOAuth

async def test_quickbooks():
    oauth = QuickBooksOAuth(config)
    auth_url = await oauth.get_authorization_url()
    print(f"Authorize at: {auth_url}")
    # After authorization, exchange code for tokens
    tokens = await oauth.exchange_code_for_tokens(code)
    print(f"Access token: {tokens['access_token'][:20]}...")
```

## 📚 Documentation

### Core Documents

1. **`README.md`** - Main project README
2. **`README_REAL_API_INTEGRATION.md`** (this file) - Real API integration guide
3. **`docs/PROJECT_OVERVIEW.md`** - High-level project overview
4. **`docs/PROJECT_STRUCTURE.md`** - Detailed project structure
5. **`docs/DEVELOPMENT_SETUP.md`** - Development environment setup

### API Integration Documents

1. **`summaries/PHASE_2_1_REAL_API_ANALYSIS.md`** - Gap analysis (START HERE)
2. **`docs/API_ANALYSIS.md`** - Detailed API analysis
3. **`docs/REAL_API_IMPLEMENTATION_PLAN.md`** - Implementation roadmap

### Phase Summaries

1. **`summaries/PHASE_2_1_SUMMARY.md`** - SuperOps mock implementation
2. **`summaries/PHASE_2_1_COMPLETE_SUMMARY.md`** - Full Phase 2.1 mock implementation
3. **`summaries/PHASE_2_1_REAL_API_ANALYSIS.md`** - Real API requirements

## ❓ FAQs

### Q: Can I use this system without real API credentials?

**A:** Yes! The current implementation uses mock data and works perfectly for:
- Development and testing
- Understanding the system architecture
- Building ML models with sample data
- Prototyping and demos

### Q: How long does it take to implement real API integration?

**A:** Based on the implementation plan:
- **Minimum**: 17 days (with experienced developers)
- **Maximum**: 23 days (including testing and documentation)
- **Realistic**: 20 days for production-ready implementation

### Q: What are the main challenges?

**A:** The three main challenges are:
1. **OAuth 2.0 Implementation** (QuickBooks) - Complex authentication flow
2. **GraphQL Client** (SuperOps) - Different from traditional REST APIs
3. **Token Management** - Secure storage, refresh, and validation

### Q: Do I need both APIs or can I start with one?

**A:** You can implement them independently:
- **SuperOps only**: Easier (no OAuth), provides ticket and service data
- **QuickBooks only**: More complex (OAuth), provides financial data
- **Both**: Full functionality, requires both implementations

### Q: What's the cost of using real APIs?

**A:** Costs vary:
- **SuperOps**: Typically included in subscription, check rate limits
- **QuickBooks**: Free for development, may have limits in production
- **Infrastructure**: Database for token storage, hosting for OAuth callback

### Q: Is the mock data realistic?

**A:** Yes, the mock data is designed to be realistic:
- ✅ Proper data types and formats
- ✅ Realistic relationships between entities
- ✅ Varied data patterns (different priorities, statuses, amounts)
- ✅ Time-series data with proper timestamps
- ❌ Not based on real business patterns
- ❌ No actual API response structure

### Q: Can I mix mock and real data?

**A:** Yes! You can implement a hybrid approach:
```python
# Use real SuperOps, mock QuickBooks
extractor = ComprehensiveDataExtractor(
    superops_client=RealSuperOpsClient(config),
    quickbooks_client=MockQuickBooksClient(),
    internal_db=InternalDBConnector(config)
)
```

### Q: What happens if API credentials are invalid?

**A:** The system will:
1. Attempt to authenticate
2. Receive authentication error
3. Log the error
4. Raise exception with clear error message
5. Not fall back to mock data (to avoid confusion)

### Q: How do I know if I'm using mock or real data?

**A:** Check the logs:
```python
# Mock data will show:
logger.info("Mock SuperOps API call to tickets")

# Real data will show:
logger.info("GraphQL query to SuperOps: getTicketList")
```

### Q: What's the difference between sandbox and production?

**A:**
| Aspect | Sandbox | Production |
|--------|---------|------------|
| **Data** | Test data | Real business data |
| **Credentials** | Sandbox credentials | Production credentials |
| **Rate Limits** | Usually more lenient | Stricter limits |
| **Cost** | Usually free | May have usage costs |
| **Risk** | Safe to experiment | Changes affect real data |

## 🛠️ Troubleshooting

### Mock Data Issues

**Problem**: Tests fail with import errors
```bash
# Solution: Add src to Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}"
python tests/test_phase_2_1_complete.py
```

**Problem**: Mock data doesn't match expected format
```python
# Solution: Check data transformation
from src.data.transformers import DataTransformer
transformer = DataTransformer()
transformed = transformer.transform_superops_tickets(mock_data)
```

### Real API Issues

**Problem**: Authentication fails
```bash
# Check credentials
echo $SUPEROPS_API_KEY
echo $QUICKBOOKS_CLIENT_ID

# Verify in code
print(f"API Key: {config.superops_api.api_key[:10]}...")
```

**Problem**: OAuth callback not working
```bash
# Ensure callback URL is accessible
curl http://localhost:8000/auth/quickbooks/callback

# Check redirect URI matches exactly
echo $QUICKBOOKS_REDIRECT_URI
```

**Problem**: GraphQL query errors
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check query syntax
from gql import gql
query = gql("query { getTicketList { tickets { ticketId } } }")
```

## 🎓 Learning Resources

### SuperOps API
- **Official Docs**: https://developer.superops.com/it
- **GraphQL Tutorial**: https://graphql.org/learn/
- **Python GraphQL Client**: https://github.com/graphql-python/gql

### QuickBooks API
- **Official Docs**: https://developer.intuit.com/app/developer/qbo/docs/develop
- **OAuth 2.0 Guide**: https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0
- **Python OAuth Library**: https://docs.authlib.org/en/latest/

### General
- **Async Python**: https://docs.python.org/3/library/asyncio.html
- **Pydantic**: https://docs.pydantic.dev/
- **aiohttp**: https://docs.aiohttp.org/

## 🤝 Contributing

### Adding New Data Sources

1. Create client in `src/data/`
2. Implement async methods
3. Add to `comprehensive_extractor.py`
4. Create tests in `tests/`
5. Update documentation

### Improving Mock Data

1. Edit `_generate_mock_*` methods
2. Ensure data is realistic
3. Add variety and edge cases
4. Update tests if needed

### Implementing Real APIs

1. Follow implementation plan
2. Create feature branch
3. Implement one phase at a time
4. Add comprehensive tests
5. Update documentation
6. Submit pull request

## 📞 Support

### Getting Help

1. **Read Documentation**: Start with `PHASE_2_1_REAL_API_ANALYSIS.md`
2. **Check FAQs**: This document's FAQ section
3. **Review Code**: Look at existing implementations
4. **Check Logs**: Enable debug logging for details

### Reporting Issues

When reporting issues, include:
- What you're trying to do
- Current behavior
- Expected behavior
- Error messages and logs
- Environment details (Python version, OS, etc.)
- Whether using mock or real data

## 🗺️ Roadmap

### Current (v1.0) - Mock Data ✅
- [x] Mock SuperOps client
- [x] Mock QuickBooks client
- [x] Mock Internal DB connector
- [x] Comprehensive data extractor
- [x] Basic tests
- [x] Documentation

### Next (v2.0) - Real API Integration ⏭️
- [ ] SuperOps GraphQL client
- [ ] QuickBooks OAuth flow
- [ ] Token management
- [ ] Data transformers
- [ ] Integration tests
- [ ] Production deployment

### Future (v3.0) - Advanced Features 🔮
- [ ] Real-time data streaming
- [ ] Webhook support
- [ ] Advanced caching
- [ ] Data quality monitoring
- [ ] Performance optimization
- [ ] Multi-tenant support

## 📄 License

[Your License Here]

## 👥 Authors

[Your Team Here]

---

**Last Updated**: 2025-01-15
**Version**: 1.0 (Mock Data)
**Status**: Production Ready (Mock), Planning (Real APIs)

