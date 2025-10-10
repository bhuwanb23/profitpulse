@echo off
echo 🚀 Setting up SuperHack Database...

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL not found. Please install PostgreSQL first.
    echo Download from: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo ✅ PostgreSQL found

REM Database configuration
set DB_NAME=superhack_db

echo 📊 Creating database: %DB_NAME%

REM Create database
createdb %DB_NAME%
if %errorlevel% equ 0 (
    echo ✅ Database '%DB_NAME%' created successfully
) else (
    echo ⚠️  Database might already exist or error occurred
)

echo 📋 Applying database schema...
psql -d %DB_NAME% -f database/schemas/init.sql
if %errorlevel% equ 0 (
    echo ✅ Database schema applied successfully
) else (
    echo ❌ Error applying schema
    echo Make sure you're in the project root directory
    pause
    exit /b 1
)

set /p loadSampleData="Do you want to load sample data? (y/n): "
if /i "%loadSampleData%"=="y" (
    echo 📊 Loading sample data...
    psql -d %DB_NAME% -f database/seeds/sample_data.sql
    if %errorlevel% equ 0 (
        echo ✅ Sample data loaded successfully
    ) else (
        echo ❌ Error loading sample data
    )
)

echo ⚙️  Creating environment configuration...

REM Create .env file
(
echo # Database Configuration
echo DB_HOST=localhost
echo DB_PORT=5432
echo DB_NAME=superhack_db
echo DB_USER=postgres
echo DB_PASSWORD=your_postgres_password
echo DB_URL=postgresql://postgres:your_postgres_password@localhost:5432/superhack_db
echo.
echo # Application Configuration
echo NODE_ENV=development
echo PORT=3000
echo JWT_SECRET=your_jwt_secret_key_here_change_this_in_production
echo JWT_EXPIRES_IN=7d
echo.
echo # AI/ML Configuration
echo AI_MODEL_PATH=./ai-ml/models
echo AI_CONFIDENCE_THRESHOLD=0.7
echo.
echo # Integration APIs
echo SUPEROPS_API_KEY=your_superops_api_key
echo QUICKBOOKS_CLIENT_ID=your_quickbooks_client_id
echo QUICKBOOKS_CLIENT_SECRET=your_quickbooks_client_secret
) > .env

echo ✅ Environment file created

echo 🎉 Database setup completed successfully!
echo 📝 Next steps:
echo    1. Update .env file with your actual PostgreSQL password
echo    2. Update .env file with your API keys
echo    3. Start the backend: cd backend ^&^& npm start
echo    4. Start the frontend: cd frontend ^&^& npm run dev
echo    5. Start the AI/ML service: cd ai-ml ^&^& python app.py

pause
