# SuperHack Integration Test Script
# Starts both services and runs integration tests

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 SuperHack Service Startup & Testing" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$backendPath = "backend"
$aiMlPath = "ai-ml"
$backendProcess = $null
$aiMlProcess = $null

# Cleanup function
function Stop-Services {
    Write-Host "`n🛑 Shutting down services..." -ForegroundColor Yellow
    
    if ($backendProcess -and !$backendProcess.HasExited) {
        Write-Host "Stopping Backend..." -ForegroundColor Yellow
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    }
    
    if ($aiMlProcess -and !$aiMlProcess.HasExited) {
        Write-Host "Stopping AI/ML..." -ForegroundColor Yellow
        Stop-Process -Id $aiMlProcess.Id -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "✅ Services stopped" -ForegroundColor Green
}

# Register cleanup on exit
Register-ObjectEvent -InputObject ([System.Console]) -EventName "CancelKeyPress" -Action { Stop-Services; exit } | Out-Null

# Start Backend
Write-Host "`n🚀 Starting Backend Service..." -ForegroundColor Cyan
Set-Location $backendPath

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Start backend
$backendProcess = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -PassThru -NoNewWindow
Write-Host "✅ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
Set-Location ..

# Start AI/ML
Write-Host "`n🚀 Starting AI/ML Service..." -ForegroundColor Cyan
Set-Location $aiMlPath

# Check for virtual environment
$venvPython = "venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonCmd = $venvPython
    Write-Host "✅ Using virtual environment" -ForegroundColor Green
} else {
    $pythonCmd = "python"
    Write-Host "⚠️  Using system Python (venv not found)" -ForegroundColor Yellow
}

# Start AI/ML
$aiMlProcess = Start-Process -FilePath $pythonCmd -ArgumentList "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -PassThru -NoNewWindow
Write-Host "✅ AI/ML started (PID: $($aiMlProcess.Id))" -ForegroundColor Green
Set-Location ..

# Wait for services to start
Write-Host "`n⏳ Waiting for services to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Test services
Write-Host "`n🧪 Testing services..." -ForegroundColor Cyan

# Test Backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/health" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is responding" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend not responding: $_" -ForegroundColor Red
}

# Test AI/ML
try {
    $headers = @{ "Authorization" = "Bearer admin_key" }
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Headers $headers -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ AI/ML is responding" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ AI/ML not responding: $_" -ForegroundColor Red
}

Write-Host "`n✅ Services are running!" -ForegroundColor Green
Write-Host "📝 Backend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📝 AI/ML: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📝 AI/ML Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n⚠️  Press Ctrl+C to stop all services" -ForegroundColor Yellow

# Keep script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
        if ($backendProcess.HasExited -or $aiMlProcess.HasExited) {
            Write-Host "`n⚠️  A service has stopped" -ForegroundColor Yellow
            break
        }
    }
} finally {
    Stop-Services
}

