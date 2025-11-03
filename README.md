# 🚀 ProfitPulse AI - AI-Powered Profitability & Growth Intelligence Platform

> **Transform your MSP operations into strategic growth with AI-driven financial insights**

## 🎯 Overview

ProfitPulse AI is an AI-powered platform designed to help Managed Service Providers (MSPs) and IT teams convert operational data into actionable financial insights. It integrates with SuperOps and other IT management tools to provide real-time profitability analysis, revenue leak detection, and growth recommendations.

## 📊 Business Impact Analysis

![Business Impact](images/readme/business_impact.png)

## 🔍 Pain Points & Root Causes

![Pain Points](images/readme/pain_points.png)
![Root Causes](images/readme/causes.png)

## 💡 Innovative Solutions

![Innovation](images/readme/innovation.png)

## 📈 Expected Impact

![Expected Impact](images/readme/expected_impact.png)

## 🎯 Key Features

- 🧠 **AI-Powered Analytics** - Machine learning models for profitability analysis
- 💰 **Revenue Leak Detection** - Identify unbilled services and underpriced contracts
- 📊 **Real-time Dashboards** - Interactive financial intelligence dashboards
- 🔗 **Seamless Integrations** - SuperOps, QuickBooks, Zapier support
- 🎯 **Smart Recommendations** - AI-driven growth and optimization suggestions
- 📈 **Profit Forecasting** - Predictive analytics for future performance

![Core Features](images/readme/core_features.png)

## 🔍 SWOT Analysis

![SWOT Analysis](images/readme/swot.png)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI/ML Layer   │
│   (React)       │◄──►│   (Node.js)     │◄──►│   (Python)      │
│   Dashboard     │    │   API Server    │    │   Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Redis Cache   │    │   File Storage  │
│   Database      │    │   Sessions      │    │   Models/Data   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
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

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 13+
- Git

### Installation Options

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