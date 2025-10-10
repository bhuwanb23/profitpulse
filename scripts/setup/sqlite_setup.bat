@echo off
echo 🚀 Setting up SuperHack SQLite Database...

REM Check if SQLite is available
sqlite3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ SQLite not found. Please install SQLite first.
    echo Download from: https://www.sqlite.org/download.html
    echo Or use: winget install SQLite.SQLite
    pause
    exit /b 1
)

echo ✅ SQLite found

REM Database configuration
set DB_FILE=superhack.db
set SCHEMA_FILE=database/schemas/sqlite_init.sql
set SAMPLE_DATA_FILE=database/seeds/sqlite_sample_data.sql

echo 📊 Creating SQLite database: %DB_FILE%

echo 📋 Applying database schema...
sqlite3 %DB_FILE% < %SCHEMA_FILE%
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
    sqlite3 %DB_FILE% < %SAMPLE_DATA_FILE%
    if %errorlevel% equ 0 (
        echo ✅ Sample data loaded successfully
    ) else (
        echo ❌ Error loading sample data
    )
)

echo ⚙️  Creating environment configuration...

REM Create .env file
(
echo # Database Configuration ^(SQLite^)
echo DB_TYPE=sqlite
echo DB_FILE=./superhack.db
echo DB_URL=sqlite:./superhack.db
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

echo 🎉 SQLite database setup completed successfully!
echo 📝 Database file created: %DB_FILE%
echo 📝 Next steps:
echo    1. Update .env file with your actual API keys
echo    2. Start the backend: cd backend ^&^& npm start
echo    3. Start the frontend: cd frontend ^&^& npm run dev
echo    4. Start the AI/ML service: cd ai-ml ^&^& python app.py
echo    5. View database: sqlite3 %DB_FILE%

pause
