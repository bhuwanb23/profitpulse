# Development Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)
- Code editor (VS Code, PyCharm, etc.)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd superhack/ai-ml

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
# Windows:
notepad .env
# macOS/Linux:
nano .env
```

### 3. Verify Installation

```bash
# Run tests
python tests/run_tests.py

# Run basic examples
python examples/basic_usage.py
```

## 🔧 Development Environment

### VS Code Setup

1. **Install Extensions**:
   - Python
   - Pylance
   - Python Docstring Generator
   - GitLens
   - REST Client

2. **Workspace Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv": true,
        "**/mlruns": true,
        "**/logs": true
    }
}
```

3. **Launch Configuration** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/api/main.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Python: Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        }
    ]
}
```

### PyCharm Setup

1. **Open Project**: Open the `ai-ml` folder as a project
2. **Configure Interpreter**: Set Python interpreter to `venv/Scripts/python.exe`
3. **Configure Tests**: Set test runner to pytest
4. **Configure Run Configurations**:
   - FastAPI Server: `src/api/main.py`
   - Tests: `tests/` directory

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test suite
python tests/run_tests.py --test phase_2_1

# Run with verbose output
python tests/run_tests.py --verbose

# Run individual test files
python tests/test_data_pipeline.py
python tests/test_phase_2_1.py
```

### Test Structure

```
tests/
├── __init__.py
├── run_tests.py              # Test runner
├── test_data_pipeline.py     # Data pipeline tests
├── test_phase_2_1.py         # Phase 2.1 tests
├── test_api.py               # API tests (when created)
├── test_models.py            # Model tests (when created)
└── test_integration.py       # Integration tests (when created)
```

### Writing Tests

```python
import asyncio
import pytest
from src.data.data_extractor import create_data_extractor

class TestDataExtractor:
    async def test_extract_tickets(self):
        """Test ticket data extraction"""
        extractor = create_data_extractor()
        await extractor.initialize()
        
        tickets = await extractor.extract_ticket_data()
        assert len(tickets) > 0
        assert all('id' in ticket for ticket in tickets)
        
        await extractor.close()
```

## 📊 Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... implement feature ...

# Run tests
python tests/run_tests.py

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature
```

### 2. Code Quality

```bash
# Format code
black src/ tests/

# Lint code
pylint src/ tests/

# Type checking
mypy src/

# Security check
bandit -r src/
```

### 3. Documentation

```bash
# Generate API docs
sphinx-build -b html docs/ docs/_build/

# Update README
# Edit README.md

# Update project structure
# Edit docs/PROJECT_STRUCTURE.md
```

## 🔧 Configuration Management

### Environment Variables

```bash
# Development
export ENVIRONMENT=development
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG

# Production
export ENVIRONMENT=production
export DEBUG_MODE=false
export LOG_LEVEL=INFO
```

### Configuration Files

- **`config.py`**: Main configuration with environment-based settings
- **`.env`**: Environment-specific variables
- **`requirements.txt`**: Python dependencies
- **`setup.py`**: Package configuration

## 🚀 API Development

### Starting the API Server

```bash
# Development mode
python -m src.api.main

# Production mode
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Adding New Endpoints

```python
# In src/api/routes/new_route.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class NewRequest(BaseModel):
    field1: str
    field2: int

@router.post("/new-endpoint")
async def new_endpoint(request: NewRequest):
    """New endpoint description"""
    return {"message": "Success", "data": request.dict()}
```

## 📈 Monitoring and Debugging

### Logging

```python
import logging
from src.utils.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Use logger
logger.info("Processing data...")
logger.error("Error occurred: %s", error_message)
```

### Debugging

```python
# Add breakpoints in VS Code
import pdb; pdb.set_trace()

# Or use logging
logger.debug("Debug info: %s", debug_data)
```

### Performance Monitoring

```python
import time
from src.utils.metrics_collector import get_metrics_collector

# Start timer
start_time = time.time()

# ... do work ...

# Record metrics
duration = time.time() - start_time
metrics_collector = get_metrics_collector()
metrics_collector.record_request_duration(duration)
```

## 🔄 Database Development

### SQLite (Development)

```bash
# Database file: superhack_ai.db
# No setup required - created automatically
```

### PostgreSQL (Production)

```bash
# Install PostgreSQL
# Create database
createdb superhack_ai

# Update config.py
DATABASE_URL=postgresql://user:password@localhost/superhack_ai
```

### Database Migrations

```python
# Run migrations
python -m alembic upgrade head

# Create new migration
python -m alembic revision --autogenerate -m "description"
```

## 🧪 MLflow Development

### Starting MLflow Server

```bash
# Start MLflow tracking server
mlflow server --backend-store-uri sqlite:///mlruns/mlflow.db --default-artifact-root ./mlruns
```

### MLflow UI

- **MLflow UI**: http://localhost:5000
- **Experiments**: View and compare experiments
- **Models**: Manage model versions and stages

### Using MLflow

```python
import mlflow
import mlflow.sklearn

# Start experiment
mlflow.set_experiment("superhack_ai")

# Log parameters and metrics
with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", 0.95)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
```

## 🚀 Deployment

### Docker Development

```bash
# Build image
docker build -t superhack-ai-ml .

# Run container
docker run -p 8000:8000 superhack-ai-ml
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
      - ./mlruns:/app/mlruns
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Add src to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

2. **Database Connection Issues**:
   ```bash
   # Check database file permissions
   ls -la superhack_ai.db
   
   # Recreate database
   rm superhack_ai.db
   python -c "from src.data.ingestion import *; print('Database recreated')"
   ```

3. **Port Already in Use**:
   ```bash
   # Find process using port
   netstat -ano | findstr :8000
   
   # Kill process
   taskkill /PID <PID> /F
   ```

4. **Memory Issues**:
   ```bash
   # Monitor memory usage
   python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
   ```

### Debug Mode

```bash
# Enable debug mode
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG

# Run with debug
python -m src.api.main
```

## 📚 Resources

### Documentation
- [Project Structure](PROJECT_STRUCTURE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Model Architecture](MODEL_ARCHITECTURE.md)

### Examples
- [Basic Usage](../examples/basic_usage.py)
- [API Examples](../examples/api_examples.py)
- [Model Examples](../examples/model_examples.py)

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**Last Updated**: October 15, 2025  
**Version**: 1.0.0  
**Maintainer**: SuperHack AI/ML Team
