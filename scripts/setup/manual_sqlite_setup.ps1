# Manual SQLite Setup - Alternative Method
# This script creates a simple database without requiring SQLite command line

Write-Host "🚀 Setting up SuperHack Database (Manual Method)..." -ForegroundColor Green

# Create a simple database file using Node.js
Write-Host "📊 Creating database using Node.js..." -ForegroundColor Blue

# Create a simple setup script
$setupScript = @"
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

// Create database
const db = new sqlite3.Database('superhack.db');

// Read and execute schema
const schema = fs.readFileSync('database/schemas/sqlite_init.sql', 'utf8');
db.exec(schema, (err) => {
    if (err) {
        console.error('Error creating schema:', err);
        process.exit(1);
    }
    console.log('✅ Database schema created successfully');
    
    // Ask if user wants sample data
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    rl.question('Do you want to load sample data? (y/n): ', (answer) => {
        if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
            const sampleData = fs.readFileSync('database/seeds/sqlite_sample_data.sql', 'utf8');
            db.exec(sampleData, (err) => {
                if (err) {
                    console.error('Error loading sample data:', err);
                } else {
                    console.log('✅ Sample data loaded successfully');
                }
                db.close();
                rl.close();
            });
        } else {
            db.close();
            rl.close();
        }
    });
});
"@

$setupScript | Out-File -FilePath "setup_db.js" -Encoding UTF8

# Create package.json for sqlite3
$packageJson = @"
{
  "name": "superhack-db-setup",
  "version": "1.0.0",
  "description": "Database setup for SuperHack",
  "main": "setup_db.js",
  "dependencies": {
    "sqlite3": "^5.1.6"
  }
}
"@

$packageJson | Out-File -FilePath "package.json" -Encoding UTF8

Write-Host "📦 Installing SQLite3 via npm..." -ForegroundColor Blue
npm install

Write-Host "🗄️  Creating database..." -ForegroundColor Blue
node setup_db.js

# Clean up
Remove-Item "setup_db.js" -Force
Remove-Item "package.json" -Force
Remove-Item "package-lock.json" -Force -ErrorAction SilentlyContinue
Remove-Item "node_modules" -Recurse -Force -ErrorAction SilentlyContinue

# Create .env file
Write-Host "⚙️  Creating environment configuration..." -ForegroundColor Blue

$envContent = @"
# Database Configuration (SQLite)
DB_TYPE=sqlite
DB_FILE=./superhack.db
DB_URL=sqlite:./superhack.db

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

Write-Host "🎉 Database setup completed successfully!" -ForegroundColor Green
Write-Host "📝 Database file created: superhack.db" -ForegroundColor Cyan
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Update .env file with your actual API keys" -ForegroundColor White
Write-Host "   2. Start the backend: cd backend; npm start" -ForegroundColor White
Write-Host "   3. Start the frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host "   4. Start the AI/ML service: cd ai-ml; python app.py" -ForegroundColor White
