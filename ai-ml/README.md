# SuperHack AI/ML System

AI/ML system for MSP profitability optimization and predictive analytics.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (venv)

### Installation

1. **Clone and navigate to the AI/ML directory:**
   ```bash
   cd ai-ml
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the development server:**
   ```bash
   python -m src.api.main
   ```

## 📁 Project Structure

```
ai-ml/
├── src/                    # Source code
│   ├── api/               # API endpoints and model serving
│   ├── data/              # Data processing and ingestion
│   ├── features/          # Feature engineering
│   ├── models/            # ML models and algorithms
│   └── utils/             # Utility functions
├── data/                  # Data storage
├── models/                # Trained models
├── logs/                  # Log files
├── feature_store/         # Feature store
├── mlruns/               # MLflow experiments
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
└── AI_ML_TODO.md        # Development roadmap
```

## 🧠 AI/ML Models

### Core Models
1. **Client Profitability Predictor** - Predicts client profitability using XGBoost and Random Forest
2. **Revenue Leak Detector** - Detects revenue leaks using Isolation Forest and Autoencoders
3. **Client Churn Predictor** - Predicts client churn using Logistic Regression and Neural Networks
4. **Dynamic Pricing Engine** - Optimizes pricing using Reinforcement Learning
5. **Budget Optimization Model** - Optimizes budget allocation using Linear Programming
6. **Service Demand Forecaster** - Forecasts service demand using LSTM and ARIMA
7. **Anomaly Detection System** - Detects anomalies using One-Class SVM and DBSCAN

### Client Profitability Genome
Each client is represented by a 50-dimensional vector:
- **Financial Health** (dimensions 0-9): Revenue, margins, payment behavior
- **Operational Efficiency** (dimensions 10-19): SLA compliance, resolution times
- **Engagement Level** (dimensions 20-29): Communication, satisfaction scores
- **Growth Potential** (dimensions 30-39): Upselling opportunities, expansion potential
- **Risk Factors** (dimensions 40-49): Churn risk, payment delays, service issues

## 🔧 Configuration

The system uses environment variables for configuration. See `.env.example` for all available options.

Key configurations:
- **Database**: SQLite (development) or PostgreSQL (production)
- **Backend API**: Integration with SuperHack backend
- **External APIs**: SuperOps, QuickBooks integration
- **MLflow**: Model tracking and management
- **Redis**: Caching and task queue

## 📊 API Endpoints

### Model Serving
- `POST /api/predict/profitability` - Predict client profitability
- `POST /api/predict/churn` - Predict client churn risk
- `POST /api/detect/anomalies` - Detect revenue anomalies
- `POST /api/optimize/pricing` - Get pricing recommendations
- `POST /api/optimize/budget` - Get budget optimization suggestions
- `POST /api/forecast/demand` - Forecast service demand

### Data Management
- `GET /api/data/clients` - Get client data
- `POST /api/data/sync` - Sync data from external sources
- `GET /api/features/genome/{client_id}` - Get client profitability genome

### Model Management
- `GET /api/models/status` - Get model status
- `POST /api/models/retrain` - Trigger model retraining
- `GET /api/models/performance` - Get model performance metrics

## 🚀 Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
flake8 src/
mypy src/
```

### Pre-commit Hooks
```bash
pre-commit install
pre-commit run --all-files
```

## 📈 Monitoring

- **MLflow**: Model tracking and experiments
- **Weights & Biases**: Experiment monitoring
- **Prometheus**: System metrics
- **Custom Dashboards**: Business metrics and model performance

## 🔒 Security

- Environment-based configuration
- JWT authentication
- Data encryption
- API rate limiting
- Input validation

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions, please contact the SuperHack team.
