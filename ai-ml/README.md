# SuperHack AI/ML System

## 🧠 Overview

The SuperHack AI/ML system is a comprehensive machine learning platform designed to transform MSP (Managed Service Provider) financial data into actionable AI insights. The system provides client profitability optimization, revenue leak detection, predictive churn management, and dynamic pricing intelligence.

## 🏗️ Architecture

### Multi-Layered AI System
- **Data Ingestion Layer**: Real-time data extraction from SuperOps, QuickBooks, and internal systems
- **Feature Engineering Layer**: Advanced feature creation and client profitability genome
- **ML Models Layer**: Core AI/ML models for predictions and insights
- **Model Serving Layer**: FastAPI-based model serving with MLflow integration
- **Monitoring Layer**: Real-time monitoring, alerting, and performance tracking

### Core AI/ML Models
- **Client Profitability Predictor**: XGBoost/Random Forest for profitability scoring
- **Revenue Anomaly Detector**: Isolation Forest/Autoencoder for leak detection
- **Client Churn Predictor**: Logistic Regression/Neural Net for churn prediction
- **Dynamic Pricing Engine**: Reinforcement Learning for optimal pricing
- **Budget Optimization Model**: Linear Programming + RL for budget allocation
- **Service Demand Forecaster**: LSTM + ARIMA for demand prediction

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- SuperOps API access (optional - mock data available)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd superhack/ai-ml
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run tests**
```bash
python -m pytest tests/
```

6. **Start the API server**
```bash
python -m src.api.main
```

## 📁 Project Structure

```
ai-ml/
├── src/                    # Source code
│   ├── api/               # FastAPI application
│   ├── data/              # Data processing & ingestion
│   ├── features/          # Feature engineering
│   ├── models/            # ML models
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── summaries/             # Phase completion summaries
├── docs/                  # Documentation
├── examples/              # Usage examples
├── logs/                  # Log files
├── mlruns/                # MLflow runs
├── models/                # Saved models
└── feature_store/         # Feature store
```

## 🔧 Configuration

### Environment Variables
```bash
# SuperOps API Configuration
SUPEROPS_API_BASE_URL=https://api.superops.com
SUPEROPS_API_KEY=your_api_key
SUPEROPS_TENANT_ID=your_tenant_id

# Database Configuration
DATABASE_URL=sqlite:///superhack_ai.db

# MLflow Configuration
MLFLOW_TRACKING_URI=sqlite:///mlruns/mlflow.db
MLFLOW_EXPERIMENT_NAME=superhack_ai

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=true
```

### Configuration File
The main configuration is managed through `config.py` with environment-based settings:

```python
from config import settings

# Access configuration
print(settings.superops_api.base_url)
print(settings.database.url)
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Suites
```bash
# Data pipeline tests
python tests/test_data_pipeline.py

# Phase 2.1 tests (Data Ingestion)
python tests/test_phase_2_1.py

# API tests
python -m pytest tests/test_api.py
```

### Test Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 📊 API Documentation

### FastAPI Endpoints

#### Health & Monitoring
- `GET /api/health/` - Overall health status
- `GET /api/health/liveness` - Liveness check
- `GET /api/health/readiness` - Readiness check

#### Model Management
- `GET /api/models/` - List all models
- `GET /api/models/{model_name}` - Get model details
- `POST /api/models/deploy` - Deploy model
- `POST /api/models/rollback` - Rollback model

#### Predictions
- `POST /api/predictions/profitability` - Client profitability prediction
- `POST /api/predictions/churn` - Client churn prediction
- `POST /api/predictions/revenue-leak` - Revenue leak detection
- `POST /api/predictions/dynamic-pricing` - Dynamic pricing recommendations

#### Monitoring
- `GET /api/monitoring/metrics` - Real-time metrics
- `GET /api/monitoring/performance/{model_name}` - Model performance
- `GET /api/monitoring/health/{model_name}` - Model health status

### Interactive API Documentation
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

## 🔄 Data Pipeline

### Data Ingestion
```python
from src.data.data_extractor import create_data_extractor

# Initialize data extractor
extractor = create_data_extractor()
await extractor.initialize()

# Extract all data
all_data = await extractor.extract_all_data(
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now()
)

# Close extractor
await extractor.close()
```

### Real-time Streaming
```python
from src.data.streaming_service import create_streaming_service, StreamingConfig

# Create streaming configuration
config = StreamingConfig(
    update_interval=60,
    websocket_port=8765,
    enable_websocket=True
)

# Start streaming service
streaming_service = create_streaming_service(config)
await streaming_service.start()

# Get stream data
realtime_data = streaming_service.get_stream_data("realtime_metrics", 10)
```

## 🤖 Machine Learning Models

### Model Training
```python
from src.models.profitability_predictor import ProfitabilityPredictor

# Initialize predictor
predictor = ProfitabilityPredictor()

# Train model
model = await predictor.train(
    data_source="internal_db",
    hyperparameters={"n_estimators": 100, "learning_rate": 0.1}
)

# Save model
await predictor.save_model(model, "client_profitability_predictor_v1.0")
```

### Model Prediction
```python
from src.utils.predictor import create_predictor

# Create predictor
predictor = create_predictor()

# Make prediction
result = await predictor.predict_profitability({
    "client_id": "CLIENT-001",
    "features": {
        "monthly_spend": 5000,
        "service_tier": "premium",
        "contract_value": 60000
    }
})

print(f"Profitability Score: {result.prediction_value}")
print(f"Confidence: {result.confidence}")
```

## 📈 Monitoring & Observability

### Metrics Collection
- **Application Metrics**: Request rates, response times, error rates
- **ML Metrics**: Model performance, prediction accuracy, drift detection
- **System Metrics**: CPU, memory, disk usage, network I/O

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

### Health Checks
```python
from src.utils.health_checker import HealthChecker

# Check system health
health_checker = HealthChecker()
health_status = await health_checker.get_overall_health()

print(f"System Status: {health_status['status']}")
print(f"Dependencies: {health_status['dependencies']}")
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build Docker image
docker build -t superhack-ai-ml .

# Run container
docker run -p 8000:8000 superhack-ai-ml
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

### Environment-specific Configuration
```bash
# Development
export ENVIRONMENT=development
python -m src.api.main

# Production
export ENVIRONMENT=production
python -m src.api.main
```

## 📚 Documentation

### Phase Summaries
- [Phase 1: AI/ML Infrastructure Setup](summaries/PHASE_1_SUMMARY.md)
- [Phase 2.1: Data Ingestion System](summaries/PHASE_2_1_SUMMARY.md)

### Architecture Documentation
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Model Architecture](docs/MODEL_ARCHITECTURE.md)

### Development Guides
- [Development Setup](docs/DEVELOPMENT_SETUP.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)
- [Testing Guide](docs/TESTING_GUIDE.md)

## 🔧 Development

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement feature in appropriate `/src` directory
3. Add tests in `/tests` directory
4. Update documentation in `/docs`
5. Create pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Add comprehensive docstrings
- Maintain test coverage above 80%

### Testing
- Write unit tests for all new code
- Add integration tests for API endpoints
- Include performance tests for critical paths
- Update test documentation

## 📊 Performance

### Benchmarks
- **Data Processing**: 69.38 records/second
- **API Response Time**: < 100ms average
- **Memory Usage**: 103.88 MB for full system
- **Concurrent Streams**: 5 real-time data streams

### Optimization
- Async/await for I/O operations
- Connection pooling for database access
- Caching for frequently accessed data
- Batch processing for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check the `/docs` directory
- **Examples**: See `/examples` for usage patterns
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

### Common Issues
- **API Connection**: Check SuperOps API credentials
- **Database Issues**: Verify database connection settings
- **Memory Issues**: Monitor memory usage and adjust batch sizes
- **Performance**: Check system resources and optimize queries

## 🎯 Roadmap

### Completed Phases
- ✅ **Phase 1**: AI/ML Infrastructure Setup
- ✅ **Phase 2.1**: Data Ingestion System

### Upcoming Phases
- 🔄 **Phase 2.2**: Feature Engineering & Client Genome
- 🔄 **Phase 2.3**: Data Quality & Monitoring
- 🔄 **Phase 3**: Core AI/ML Models Development
- 🔄 **Phase 4**: Model Training & Optimization
- 🔄 **Phase 5**: Model Deployment & Serving

---

**Version**: 1.0.0  
**Last Updated**: October 15, 2025  
**Maintainer**: SuperHack AI/ML Team