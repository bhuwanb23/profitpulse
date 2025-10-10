# SuperHack SQLite Database Setup - Simple Version
# This script creates a SQLite database for development and testing

Write-Host "🚀 Setting up SuperHack SQLite Database..." -ForegroundColor Green

# Database configuration
$DB_FILE = "database/superhack.db"
$SCHEMA_FILE = "database/schemas/sqlite_init.sql"
$SAMPLE_DATA_FILE = "database/seeds/sqlite_sample_data.sql"

Write-Host "📊 Creating SQLite database: $DB_FILE" -ForegroundColor Blue

# Check if SQLite is available
try {
    $sqliteVersion = sqlite3 --version
    Write-Host "✅ SQLite found: $sqliteVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ SQLite not found. Please install SQLite first." -ForegroundColor Red
    Write-Host "Download from: https://www.sqlite.org/download.html" -ForegroundColor Yellow
    Write-Host "Or use: winget install SQLite.SQLite" -ForegroundColor Yellow
    exit 1
}

# Create database and apply schema
Write-Host "📋 Applying database schema..." -ForegroundColor Blue
try {
    Get-Content $SCHEMA_FILE | sqlite3 $DB_FILE
    Write-Host "✅ Database schema applied successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Error applying schema" -ForegroundColor Red
    Write-Host "Make sure you're in the project root directory" -ForegroundColor Yellow
    exit 1
}

# Load sample data (optional)
$loadSampleData = Read-Host "Do you want to load sample data? (y/n)"
if ($loadSampleData -eq "y" -or $loadSampleData -eq "Y") {
    Write-Host "📊 Loading sample data..." -ForegroundColor Blue
    try {
        Get-Content $SAMPLE_DATA_FILE | sqlite3 $DB_FILE
        Write-Host "✅ Sample data loaded successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error loading sample data" -ForegroundColor Red
    }
}

# Create .env file for database connection
Write-Host "⚙️  Creating environment configuration..." -ForegroundColor Blue

$envContent = @"
# Database Configuration (SQLite)
DB_TYPE=sqlite
DB_FILE=./database/superhack.db
DB_URL=sqlite:./database/superhack.db

# Application Configuration
NODE_ENV=development
PORT=3000
JWT_SECRET=your_jwt_secret_key_here_change_this_in_production
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

Write-Host "🎉 SQLite database setup completed successfully!" -ForegroundColor Green
Write-Host "📝 Database file created: $DB_FILE" -ForegroundColor Cyan
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Update .env file with your actual API keys" -ForegroundColor White
Write-Host "   2. Start the backend: cd backend; npm start" -ForegroundColor White
Write-Host "   3. Start the frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host "   4. Start the AI/ML service: cd ai-ml; python app.py" -ForegroundColor White
Write-Host "   5. View database: sqlite3 $DB_FILE" -ForegroundColor White
