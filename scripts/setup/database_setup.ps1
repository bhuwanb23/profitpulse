# SuperHack Database Setup Script for Windows PowerShell
# This script sets up the PostgreSQL database for the SuperHack AI Platform

Write-Host "🚀 Setting up SuperHack Database..." -ForegroundColor Green

# Check if PostgreSQL is installed
try {
    $pgVersion = psql --version
    Write-Host "✅ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ PostgreSQL not found. Please install PostgreSQL first." -ForegroundColor Red
    Write-Host "Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
}

# Database configuration
$DB_NAME = "superhack_db"
$DB_USER = "superhack_user"
$DB_PASSWORD = "superhack_password"

Write-Host "📊 Creating database: $DB_NAME" -ForegroundColor Blue

# Create database
try {
    createdb $DB_NAME
    Write-Host "✅ Database '$DB_NAME' created successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Database might already exist or error occurred" -ForegroundColor Yellow
}

# Create user (optional, can use default postgres user)
Write-Host "👤 Setting up database user..." -ForegroundColor Blue
try {
    psql -d $DB_NAME -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    psql -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    Write-Host "✅ Database user created successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  User might already exist" -ForegroundColor Yellow
}

# Run schema
Write-Host "📋 Applying database schema..." -ForegroundColor Blue
try {
    psql -d $DB_NAME -f "database/schemas/init.sql"
    Write-Host "✅ Database schema applied successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Error applying schema" -ForegroundColor Red
    exit 1
}

# Load sample data (optional)
$loadSampleData = Read-Host "Do you want to load sample data? (y/n)"
if ($loadSampleData -eq "y" -or $loadSampleData -eq "Y") {
    Write-Host "📊 Loading sample data..." -ForegroundColor Blue
    try {
        psql -d $DB_NAME -f "database/seeds/sample_data.sql"
        Write-Host "✅ Sample data loaded successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error loading sample data" -ForegroundColor Red
    }
}

# Create .env file for database connection
Write-Host "⚙️  Creating environment configuration..." -ForegroundColor Blue
$envContent = @"
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_URL=postgresql://$DB_USER`:$DB_PASSWORD@localhost:5432/$DB_NAME

# Application Configuration
NODE_ENV=development
PORT=3000
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRES_IN=7d

# AI/ML Configuration
AI_MODEL_PATH=./ai-ml/models
AI_CONFIDENCE_THRESHOLD=0.7

# Integration APIs
SUPEROPS_API_KEY=your_superops_api_key
QUICKBOOKS_CLIENT_ID=your_quickbooks_client_id
QUICKBOOKS_CLIENT_SECRET=your_quickbooks_client_secret
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Environment file created" -ForegroundColor Green

Write-Host "🎉 Database setup completed successfully!" -ForegroundColor Green
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Update .env file with your actual API keys" -ForegroundColor White
Write-Host "   2. Start the backend: cd backend && npm start" -ForegroundColor White
Write-Host "   3. Start the frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host "   4. Start the AI/ML service: cd ai-ml && python app.py" -ForegroundColor White
