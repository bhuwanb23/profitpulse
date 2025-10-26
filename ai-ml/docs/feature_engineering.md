# Feature Engineering System

## Overview

The Feature Engineering System is a comprehensive module designed to extract meaningful features from raw MSP data for use in AI/ML models. The system is organized into three specialized engines:

1. **Financial Features Engine** - Extracts financial metrics and ratios
2. **Operational Features Engine** - Extracts operational performance metrics
3. **Behavioral Features Engine** - Extracts client behavioral patterns

## System Architecture

```
feature_engineering/
├── __init__.py
├── financial_features.py      # Financial Features Engine
├── operational_features.py    # Operational Features Engine
├── behavioral_features.py     # Behavioral Features Engine
└── orchestrator.py           # Main Feature Engineering Orchestrator
```

## Financial Features Engine

### Functions

#### `calculate_revenue_per_client()`
Calculates revenue per client on monthly or quarterly basis.

**Parameters:**
- `df`: Input DataFrame with client, revenue, and date information
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `revenue_col`: Column name for revenue values (default: 'revenue')
- `date_col`: Column name for date information (default: 'date')
- `frequency`: 'monthly' or 'quarterly' aggregation (default: 'monthly')

#### `calculate_profit_margins_by_service()`
Calculates profit margins by service type.

**Parameters:**
- `df`: Input DataFrame with service type, revenue, and cost information
- `service_type_col`: Column name for service type (default: 'service_type')
- `revenue_col`: Column name for revenue values (default: 'revenue')
- `cost_col`: Column name for cost values (default: 'cost')

#### `calculate_billing_efficiency()`
Calculates billing efficiency metrics.

**Parameters:**
- `df`: Input DataFrame with billing data
- `billed_amount_col`: Column name for billed amounts (default: 'billed_amount')
- `actual_cost_col`: Column name for actual costs (default: 'actual_cost')
- `expected_amount_col`: Column name for expected billing amounts (default: 'expected_amount')

#### `calculate_cost_per_ticket_resolution()`
Calculates cost per ticket resolution.

**Parameters:**
- `df`: Input DataFrame with ticket data
- `ticket_id_col`: Column name for ticket identifier (default: 'ticket_id')
- `cost_col`: Column name for cost values (default: 'cost')
- `resolution_time_col`: Column name for resolution time in hours (default: 'resolution_time_hours')

#### `calculate_service_utilization_rates()`
Calculates service utilization rates.

**Parameters:**
- `df`: Input DataFrame with service usage data
- `service_id_col`: Column name for service identifier (default: 'service_id')
- `usage_col`: Column name for actual usage hours (default: 'usage_hours')
- `available_hours_col`: Column name for available hours (default: 'available_hours')

#### `analyze_payment_behavior()`
Analyzes payment behavior patterns.

**Parameters:**
- `df`: Input DataFrame with payment data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `payment_date_col`: Column name for payment date (default: 'payment_date')
- `payment_amount_col`: Column name for payment amount (default: 'payment_amount')
- `due_date_col`: Column name for due date (default: 'due_date')

#### `calculate_revenue_growth_trends()`
Calculates revenue growth trends.

**Parameters:**
- `df`: Input DataFrame with revenue data over time
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `revenue_col`: Column name for revenue values (default: 'revenue')
- `date_col`: Column name for date information (default: 'date')
- `period`: Time period for growth calculation ('month', 'quarter', 'year') (default: 'month')

#### `calculate_profitability_ratios()`
Calculates various profitability ratios.

**Parameters:**
- `df`: Input DataFrame with financial data
- `revenue_col`: Column name for revenue values (default: 'revenue')
- `cost_col`: Column name for cost values (default: 'cost')
- `expense_col`: Column name for expense values (default: 'expenses')
- `asset_col`: Column name for asset values (default: 'total_assets')

## Operational Features Engine

### Functions

#### `calculate_ticket_resolution_time()`
Calculates average ticket resolution time.

**Parameters:**
- `df`: Input DataFrame with ticket data
- `ticket_id_col`: Column name for ticket identifier (default: 'ticket_id')
- `created_date_col`: Column name for ticket creation date (default: 'created_date')
- `resolved_date_col`: Column name for ticket resolution date (default: 'resolved_date')

#### `calculate_sla_compliance()`
Calculates SLA compliance percentage.

**Parameters:**
- `df`: Input DataFrame with SLA data
- `ticket_id_col`: Column name for ticket identifier (default: 'ticket_id')
- `sla_target_hours_col`: Column name for SLA target hours (default: 'sla_target_hours')
- `actual_resolution_hours_col`: Column name for actual resolution hours (default: 'actual_resolution_hours')

#### `calculate_technician_productivity()`
Calculates technician productivity scores.

**Parameters:**
- `df`: Input DataFrame with technician data
- `technician_id_col`: Column name for technician identifier (default: 'technician_id')
- `tickets_handled_col`: Column name for number of tickets handled (default: 'tickets_handled')
- `total_hours_col`: Column name for total hours worked (default: 'total_hours_worked')
- `tickets_resolved_col`: Column name for tickets resolved (default: 'tickets_resolved')

#### `assess_service_delivery_quality()`
Assesses service delivery quality metrics.

**Parameters:**
- `df`: Input DataFrame with service delivery data
- `service_id_col`: Column name for service identifier (default: 'service_id')
- `quality_score_col`: Column name for quality scores (default: 'quality_score')
- `customer_rating_col`: Column name for customer ratings (default: 'customer_rating')
- `first_time_fix_col`: Column name for first time fix indicator (default: 'first_time_fix')

#### `calculate_client_satisfaction()`
Calculates client satisfaction scores.

**Parameters:**
- `df`: Input DataFrame with client satisfaction data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `satisfaction_score_col`: Column name for satisfaction scores (default: 'satisfaction_score')
- `feedback_count_col`: Column name for total feedback count (default: 'feedback_count')
- `positive_feedback_col`: Column name for positive feedback count (default: 'positive_feedback_count')

#### `analyze_ticket_frequency()`
Analyzes support ticket frequency patterns.

**Parameters:**
- `df`: Input DataFrame with ticket data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `ticket_date_col`: Column name for ticket date (default: 'ticket_date')
- `ticket_type_col`: Column name for ticket type (default: 'ticket_type')

#### `track_service_level_trends()`
Tracks service level trends over time.

**Parameters:**
- `df`: Input DataFrame with service performance data
- `service_id_col`: Column name for service identifier (default: 'service_id')
- `date_col`: Column name for date information (default: 'date')
- `performance_metric_col`: Column name for performance metrics (default: 'performance_score')

#### `calculate_resource_utilization()`
Calculates resource utilization metrics.

**Parameters:**
- `df`: Input DataFrame with resource data
- `resource_id_col`: Column name for resource identifier (default: 'resource_id')
- `allocated_hours_col`: Column name for allocated hours (default: 'allocated_hours')
- `used_hours_col`: Column name for used hours (default: 'used_hours')
- `capacity_hours_col`: Column name for capacity hours (default: 'capacity_hours')

## Behavioral Features Engine

### Functions

#### `measure_client_engagement()`
Measures client engagement levels.

**Parameters:**
- `df`: Input DataFrame with client engagement data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `login_count_col`: Column name for login count (default: 'login_count')
- `support_request_count_col`: Column name for support request count (default: 'support_request_count')
- `feature_usage_col`: Column name for feature usage count (default: 'feature_usage_count')

#### `analyze_communication_patterns()`
Analyzes communication patterns.

**Parameters:**
- `df`: Input DataFrame with communication data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `communication_date_col`: Column name for communication date (default: 'communication_date')
- `communication_type_col`: Column name for communication type (default: 'communication_type')
- `response_time_col`: Column name for response time in hours (default: 'response_time_hours')

#### `track_service_changes()`
Tracks service upgrade/downgrade history.

**Parameters:**
- `df`: Input DataFrame with service change data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `service_type_col`: Column name for service type (default: 'service_type')
- `change_type_col`: Column name for change type (upgrade/downgrade) (default: 'change_type')
- `change_date_col`: Column name for change date (default: 'change_date')

#### `predict_contract_renewal()`
Predicts contract renewal likelihood.

**Parameters:**
- `df`: Input DataFrame with contract data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `contract_end_date_col`: Column name for contract end date (default: 'contract_end_date')
- `renewal_probability_col`: Column name for renewal probability (default: 'renewal_probability')
- `engagement_score_col`: Column name for engagement score (default: 'engagement_score')

#### `analyze_support_requests()`
Analyzes support request patterns.

**Parameters:**
- `df`: Input DataFrame with support request data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `request_date_col`: Column name for request date (default: 'request_date')
- `request_type_col`: Column name for request type (default: 'request_type')
- `resolution_satisfaction_col`: Column name for resolution satisfaction score (default: 'resolution_satisfaction')

#### `analyze_feedback_sentiment()`
Analyzes feedback sentiment.

**Parameters:**
- `df`: Input DataFrame with feedback data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `feedback_date_col`: Column name for feedback date (default: 'feedback_date')
- `sentiment_score_col`: Column name for sentiment score (default: 'sentiment_score')
- `feedback_category_col`: Column name for feedback category (default: 'feedback_category')

#### `identify_usage_patterns()`
Identifies usage pattern analysis.

**Parameters:**
- `df`: Input DataFrame with usage data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `usage_date_col`: Column name for usage date (default: 'usage_date')
- `feature_name_col`: Column name for feature name (default: 'feature_name')
- `usage_duration_col`: Column name for usage duration in minutes (default: 'usage_duration_minutes')

#### `calculate_churn_risk()`
Calculates churn risk indicators.

**Parameters:**
- `df`: Input DataFrame with client data
- `client_id_col`: Column name for client identifier (default: 'client_id')
- `engagement_score_col`: Column name for engagement score (default: 'engagement_score')
- `support_ticket_count_col`: Column name for support ticket count (default: 'support_ticket_count')
- `contract_renewal_likelihood_col`: Column name for contract renewal likelihood (default: 'contract_renewal_likelihood')
- `payment_delinquency_col`: Column name for payment delinquency rate (default: 'payment_delinquency_rate')

## Usage Examples

### Basic Usage

```python
import pandas as pd
from src.data.preprocessing.feature_engineering.financial_features import calculate_revenue_per_client

# Load your data
df = pd.read_csv('your_data.csv')

# Calculate revenue per client
revenue_features = calculate_revenue_per_client(df, frequency='monthly')
```

### Using the Orchestrator

```python
import pandas as pd
from src.data.preprocessing.modular_feature_engineering.orchestrator import extract_all_features

# Load your data
df = pd.read_csv('your_data.csv')

# Configure feature extraction
feature_config = {
    'financial_features': True,
    'operational_features': True,
    'behavioral_features': True,
    'financial_config': {
        'revenue_per_client': True,
        'profit_margins_by_service': True
    },
    'operational_config': {
        'ticket_resolution_time': True,
        'sla_compliance': True
    },
    'behavioral_config': {
        'client_engagement': True,
        'churn_risk': True
    }
}

# Extract all features
enhanced_df = extract_all_features(df, feature_config)
```

### Integration with Main Feature Engineering Pipeline

```python
import pandas as pd
from src.data.preprocessing.feature_engineering import engineer_features

# Load your data
df = pd.read_csv('your_data.csv')

# Configure the modular system
config = {
    'use_modular_system': True,
    'financial_features': True,
    'operational_features': True,
    'behavioral_features': True,
    'financial_config': {
        'revenue_per_client': True,
        'revenue_per_client_config': {
            'frequency': 'monthly'
        }
    }
}

# Engineer features using the new modular system
engineered_df = engineer_features(df, config)
```

## Integration with AI/ML Models

The features extracted by this system are designed to feed directly into the AI/ML models:

- **Profit Predictor**: Uses financial features like profit margins and revenue growth trends
- **Revenue Anomaly Detector**: Uses billing efficiency and payment behavior features
- **Client Churn Predictor**: Uses behavioral features like engagement scores and churn risk indicators
- **Dynamic Pricing Engine**: Uses financial features like profitability ratios
- **Budget Optimization Model**: Uses operational features like resource utilization rates

Each feature function is designed to be modular and reusable, allowing for easy integration with different parts of the AI/ML pipeline.