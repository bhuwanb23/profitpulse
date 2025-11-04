# 🚀 ProfitPulse AI - AI-Powered Profitability & Growth Intelligence Platform

> **Transform your MSP operations into strategic growth with AI-driven financial insights**

<p align="center">
  <img src="images/readme/core_features.png" alt="Core Features" width="800"/>
</p>


## 🎯 Overview

ProfitPulse AI is an AI-powered platform designed to help Managed Service Providers (MSPs) and IT teams convert operational data into actionable financial insights. It integrates with SuperOps and other IT management tools to provide real-time profitability analysis, revenue leak detection, and growth recommendations.

### 🎯 Key Value Propositions

- **Financial Intelligence**: Transform operational data into financial insights
- **AI-Powered Predictions**: Leverage machine learning for accurate forecasting
- **Real-time Monitoring**: Continuous analysis of business performance
- **Actionable Recommendations**: Data-driven suggestions for growth optimization

## 📊 Business Impact Analysis

![Business Impact](images/readme/business_impact.png)

## 🔍 Pain Points & Root Causes

![Pain Points](images/readme/pain_points.png)
![Root Causes](images/readme/causes.png)

## 💡 Innovative Solutions

![Innovation](images/readme/innovation.png)

## 📈 Expected Impact

![Expected Impact](images/readme/expected_impact.png)

## ✨ Key Features

- 🧠 **AI-Powered Analytics** - Machine learning models for profitability analysis
- 💰 **Revenue Leak Detection** - Identify unbilled services and underpriced contracts
- 📊 **Real-time Dashboards** - Interactive financial intelligence dashboards
- 🔗 **Seamless Integrations** - SuperOps, QuickBooks, Zapier support
- 🎯 **Smart Recommendations** - AI-driven growth and optimization suggestions
- 📈 **Profit Forecasting** - Predictive analytics for future performance

## 🔍 SWOT Analysis

![SWOT Analysis](images/readme/swot.png)

## 🏗️ System Architecture

### 🌐 High-Level Architecture

```mermaid
graph TD
    A[Frontend - React] <-- HTTP/REST --> B[Backend - Node.js]
    B <-- HTTP/REST --> C[AI/ML Service - Python]
    B <--> D[(PostgreSQL Database)]
    B <--> E[(Redis Cache)]
    C <--> D
    C <--> F[Model Storage]
    G[SuperOps API] --> B
    H[QuickBooks API] --> B
    I[Zapier Integrations] --> B
```

### 📦 Container Architecture

```mermaid
graph LR
    subgraph "Docker Network"
        direction TB
        F[Frontend<br/>React/Vite<br/>Port: 5173] <--> B[Backend<br/>Node.js/Express<br/>Port: 3000]
        B <--> A[AI/ML Service<br/>Python/FastAPI<br/>Port: 5000]
        B <--> C[PostgreSQL<br/>Port: 5432]
        B <--> D[Redis<br/>Port: 6379]
        A <--> C
    end
```

### 💾 Data Model

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : "has"
    ORGANIZATIONS ||--o{ CLIENTS : "manages"
    ORGANIZATIONS ||--o{ SERVICES : "offers"
    ORGANIZATIONS ||--o{ BUDGETS : "plans"
    CLIENTS ||--o{ CLIENT_SERVICES : "subscribes"
    CLIENTS ||--o{ TICKETS : "creates"
    CLIENTS ||--o{ INVOICES : "receives"
    SERVICES ||--o{ CLIENT_SERVICES : "provided"
    INVOICES ||--o{ INVOICE_ITEMS : "contains"
    TICKETS ||--o{ INVOICE_ITEMS : "billed"
    SERVICES ||--o{ INVOICE_ITEMS : "billed"
    BUDGETS ||--o{ BUDGET_CATEGORIES : "divided"
    BUDGETS ||--o{ EXPENSES : "tracks"
    BUDGET_CATEGORIES ||--o{ EXPENSES : "categorized"
    ORGANIZATIONS ||--o{ AI_ANALYTICS : "analyzes"
    ORGANIZATIONS ||--o{ AI_RECOMMENDATIONS : "suggests"
    ORGANIZATIONS ||--o{ INTEGRATION_SETTINGS : "connects"
```

### 🔌 API Architecture

#### Backend API Endpoints (Node.js)

```mermaid
graph LR
    A[API Gateway] --> B[Authentication]
    A --> C[User Management]
    A --> D[Organization Management]
    A --> E[Client Management]
    A --> F[Service Management]
    A --> G[Ticket Operations]
    A --> H[Ticket Analytics]
    A --> I[Invoice Management]
    A --> J[Budget Management]
    A --> K[Analytics]
    A --> L[Billing Analytics]
    A --> M[AI Services]
    A --> N[Integrations]
    A --> O[Reports]
    A --> P[Notifications]
```

#### AI/ML API Endpoints (Python)

```mermaid
graph LR
    A[AI/ML API] --> B[Health Checks]
    A --> C[Model Management]
    A --> D[Predictions]
    A --> E[Profitability Analysis]
    A --> F[Churn Prediction]
    A --> G[Revenue Leak Detection]
    A --> H[Pricing Optimization]
    A --> I[Budget Optimization]
    A --> J[Demand Forecasting]
    A --> K[Anomaly Detection]
    A --> L[Monitoring]
    A --> M[Admin]
    A --> N[Scheduled Runs]
    A --> O[Historical Analysis]
    A --> P[Model Retraining]
    A --> Q[Performance Reporting]
```

### 🧠 AI/ML Model Architecture

```mermaid
graph TD
    A[Data Ingestion] --> B[Data Preprocessing]
    B --> C[Feature Engineering]
    C --> D[Model Training]
    D --> E[Model Validation]
    E --> F[Model Deployment]
    F --> G[Real-time Predictions]
    G --> H[Performance Monitoring]
    H --> I[Model Retraining]
    I --> D
```

## 📁 Project Structure

```
ProfitPulse/
├── backend/                 # Node.js/Express API
│   ├── src/
│   │   ├── controllers/     # API route handlers
│   │   ├── models/          # Database models
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── integrations/    # External API integrations
│   └── tests/               # Backend tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── public/             # Static assets
├── ai-ml/                  # Python AI/ML layer
│   ├── src/
│   │   ├── models/         # ML models
│   │   ├── preprocessing/  # Data preprocessing
│   │   └── prediction/     # Prediction services
│   └── data/               # Data storage
├── database/               # Database related files
│   ├── schemas/            # DB schemas
│   ├── migrations/         # DB migrations
│   └── seeds/              # Sample data
└── docs/                   # Documentation
```

## 📈 Scalability & Feasibility

![Scalability](images/readme/scalability.png)
![Feasibility](images/readme/feasibility.png)

## 🚀 Quick Start

### 📋 Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 13+
- Git
- Docker (optional, for containerized deployment)

### 📥 Installation Options

#### Option 1: Docker Setup (Recommended)

```bash
# Start all services with Docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProfitPulse
   ```

2. **Set up the database**
   ```powershell
   # Windows PowerShell
   .\scripts\setup\database_setup.ps1
   ```

3. **Install dependencies for each service**

   **Backend (Node.js)**
   ```bash
   cd backend
   npm install
   ```

   **Frontend (React)**
   ```bash
   cd ../frontend
   npm install
   ```

   **AI/ML Service (Python)**
   ```bash
   cd ../ai-ml
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Start the services**

   **Backend API**
   ```bash
   cd backend
   npm start
   ```

   **Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

   **AI/ML Service**
   ```bash
   cd ai-ml
   python src/api/main.py
   ```

6. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3000
   - AI/ML Service: http://localhost:5000

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ProfitPulse_db
DB_USER=ProfitPulse_user
DB_PASSWORD=ProfitPulse_password

# API Keys
SUPEROPS_API_KEY=your_superops_api_key
QUICKBOOKS_CLIENT_ID=your_quickbooks_client_id
QUICKBOOKS_CLIENT_SECRET=your_quickbooks_client_secret

# AI Configuration
AI_CONFIDENCE_THRESHOLD=0.7
AI_MODEL_PATH=./ai-ml/models
```

## 🧪 Testing

```bash
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm test

# AI/ML tests
cd ai-ml
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   NODE_ENV=production
   DB_URL=postgresql://user:pass@host:port/db
   JWT_SECRET=your_production_secret
   ```

2. **Database Migration**
   ```bash
   npm run migrate:up
   ```

3. **Build and Deploy**
   ```bash
   # Backend
   cd backend && npm run build
   
   # Frontend
   cd frontend && npm run build
   
   # AI/ML
   cd ai-ml && pip install -r requirements.txt
   ```

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- 📧 Email: support@ProfitPulse.ai
- 🐛 Issues: [GitHub Issues](https://github.com/ProfitPulse/issues)

---