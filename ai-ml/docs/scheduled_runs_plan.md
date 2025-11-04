# Scheduled Model Runs Implementation Plan

## Overview
This document outlines the implementation plan for adding scheduled model runs functionality to the AI/ML API. This feature will allow users to schedule automated execution of machine learning models at predefined intervals.

## Requirements Analysis

### Functional Requirements
1. Create scheduled runs with cron-like syntax
2. Enable/disable scheduled runs
3. View all scheduled runs
4. View details of specific scheduled runs
5. Delete scheduled runs
6. Trigger immediate execution of scheduled runs
7. View execution history of scheduled runs

### Technical Requirements
1. Integration with existing FastAPI application
2. Persistent storage of scheduled run configurations
3. Cron expression parsing and validation
4. Background task execution
5. Error handling and logging
6. API endpoint security (authentication/authorization)

## Implementation Approach

### 1. Data Models
Create Pydantic models for scheduled runs in `src/api/models/schemas.py`:
- ScheduledRun (for storing run configurations)
- ScheduledRunRequest (for creating new scheduled runs)
- ScheduledRunResponse (for API responses)

### 2. Database Integration
Since we're using SQLite, we'll add scheduled run storage to the existing database:
- Create scheduled_runs table
- Add CRUD operations for scheduled runs

### 3. Cron Expression Handling
Implement cron expression parsing:
- Use croniter library for cron expression parsing
- Validate cron expressions on creation
- Calculate next execution times

### 4. Scheduler Implementation
Create a background scheduler:
- Use asyncio for asynchronous task scheduling
- Implement a scheduler service that runs in the background
- Check for scheduled runs that need execution
- Execute model predictions for due scheduled runs

### 5. API Endpoints
Add new endpoints to `src/api/routes/scheduled.py`:
- POST /api/scheduled - Create new scheduled run
- GET /api/scheduled - List all scheduled runs
- GET /api/scheduled/{run_id} - Get specific scheduled run
- PUT /api/scheduled/{run_id} - Update scheduled run
- DELETE /api/scheduled/{run_id} - Delete scheduled run
- POST /api/scheduled/{run_id}/trigger - Trigger immediate execution

### 6. Execution Engine
Implement the execution logic:
- Load model configuration from scheduled run
- Execute model prediction with specified parameters
- Store results in database
- Handle execution errors and logging

## Implementation Steps

### Phase 1: Data Models and Database Integration
1. Add ScheduledRun models to schemas.py
2. Create scheduled_runs database table
3. Implement CRUD operations for scheduled runs

### Phase 2: Cron Expression Handling
1. Add croniter dependency
2. Implement cron expression validation
3. Create utility functions for calculating next execution times

### Phase 3: Scheduler Implementation
1. Create scheduler service class
2. Implement background task execution
3. Add scheduler to application lifecycle management

### Phase 4: API Endpoints
1. Create scheduled.py route file
2. Implement all scheduled run API endpoints
3. Add authentication and authorization checks
4. Add input validation and error handling

### Phase 5: Execution Engine
1. Implement model execution logic
2. Add result storage functionality
3. Implement error handling and logging

### Phase 6: Testing and Documentation
1. Create unit tests for all components
2. Test API endpoints with various scenarios
3. Document API usage with examples

## Technical Details

### Database Schema
```sql
CREATE TABLE scheduled_runs (
    id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    schedule TEXT NOT NULL,  -- cron expression
    enabled BOOLEAN DEFAULT TRUE,
    parameters TEXT,  -- JSON string of parameters
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_run TIMESTAMP,
    next_run TIMESTAMP
);
```

### API Endpoints
1. `POST /api/scheduled`
   - Create new scheduled run
   - Request body: model_name, schedule (cron), parameters, enabled
   - Response: ScheduledRunResponse

2. `GET /api/scheduled`
   - List all scheduled runs
   - Query parameters: limit, offset, model_name
   - Response: List of ScheduledRun

3. `GET /api/scheduled/{run_id}`
   - Get specific scheduled run
   - Response: ScheduledRun

4. `PUT /api/scheduled/{run_id}`
   - Update scheduled run
   - Request body: schedule, parameters, enabled
   - Response: ScheduledRunResponse

5. `DELETE /api/scheduled/{run_id}`
   - Delete scheduled run
   - Response: Success message

6. `POST /api/scheduled/{run_id}/trigger`
   - Trigger immediate execution
   - Response: Execution result

### Dependencies
- croniter - for cron expression parsing
- Add to requirements.txt

## Testing Strategy

### Unit Tests
1. Test cron expression validation
2. Test next execution time calculation
3. Test scheduled run CRUD operations
4. Test scheduler logic

### Integration Tests
1. Test API endpoints
2. Test end-to-end scheduled run execution
3. Test error scenarios

### Performance Tests
1. Test scheduler with multiple concurrent scheduled runs
2. Test execution performance with large parameter sets

## Error Handling

### Common Error Scenarios
1. Invalid cron expressions
2. Non-existent model names
3. Database connection failures
4. Model execution errors
5. Authentication failures

### Error Responses
All errors will follow the existing API error response format:
```json
{
    "error": "Error type",
    "message": "Human-readable error message",
    "status_code": 400,
    "correlation_id": "unique-id"
}
```

## Security Considerations

1. All endpoints require authentication
2. Users can only access their own scheduled runs
3. Input validation on all parameters
4. Rate limiting applied to all endpoints
5. Secure storage of sensitive parameters

## Deployment Considerations

1. Scheduler should start with the application
2. Graceful shutdown of scheduler tasks
3. Recovery from unexpected shutdowns
4. Monitoring and alerting for scheduler health

## Timeline
- Phase 1: 2 days
- Phase 2: 1 day
- Phase 3: 2 days
- Phase 4: 2 days
- Phase 5: 2 days
- Phase 6: 1 day
- Total: 10 days