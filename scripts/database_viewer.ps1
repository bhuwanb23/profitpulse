# SuperHack Database Viewer
# Simple script to view and interact with the SQLite database

param(
    [string]$Action = "menu",
    [string]$Query = ""
)

$DB_FILE = "superhack.db"

function Show-Menu {
    Write-Host "🔍 SuperHack Database Viewer" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host "1. View all tables" -ForegroundColor Yellow
    Write-Host "2. View clients" -ForegroundColor Yellow
    Write-Host "3. View tickets" -ForegroundColor Yellow
    Write-Host "4. View invoices" -ForegroundColor Yellow
    Write-Host "5. View AI analytics" -ForegroundColor Yellow
    Write-Host "6. View AI recommendations" -ForegroundColor Yellow
    Write-Host "7. Run custom query" -ForegroundColor Yellow
    Write-Host "8. Database statistics" -ForegroundColor Yellow
    Write-Host "9. Exit" -ForegroundColor Yellow
    Write-Host ""
}

function Show-AllTables {
    Write-Host "📊 All Tables in Database:" -ForegroundColor Cyan
    sqlite3 $DB_FILE ".tables"
}

function Show-Clients {
    Write-Host "👥 Clients:" -ForegroundColor Cyan
    sqlite3 $DB_FILE "SELECT id, name, email, industry, contract_type, contract_value FROM clients LIMIT 10;"
}

function Show-Tickets {
    Write-Host "🎫 Recent Tickets:" -ForegroundColor Cyan
    sqlite3 $DB_FILE "SELECT ticket_number, title, priority, status, created_at FROM tickets ORDER BY created_at DESC LIMIT 10;"
}

function Show-Invoices {
    Write-Host "💰 Recent Invoices:" -ForegroundColor Cyan
    sqlite3 $DB_FILE "SELECT invoice_number, total_amount, status, invoice_date FROM invoices ORDER BY invoice_date DESC LIMIT 10;"
}

function Show-AIAnalytics {
    Write-Host "🧠 AI Analytics:" -ForegroundColor Cyan
    sqlite3 $DB_FILE "SELECT analysis_type, confidence_score, status, created_at FROM ai_analytics ORDER BY created_at DESC LIMIT 10;"
}

function Show-AIRecommendations {
    Write-Host "💡 AI Recommendations:" -ForegroundColor Cyan
    sqlite3 $DB_FILE "SELECT title, recommendation_type, impact_score, status FROM ai_recommendations ORDER BY created_at DESC LIMIT 10;"
}

function Show-DatabaseStats {
    Write-Host "📈 Database Statistics:" -ForegroundColor Cyan
    Write-Host "Organizations: " -NoNewline
    sqlite3 $DB_FILE "SELECT COUNT(*) FROM organizations;"
    Write-Host "Clients: " -NoNewline
    sqlite3 $DB_FILE "SELECT COUNT(*) FROM clients;"
    Write-Host "Tickets: " -NoNewline
    sqlite3 $DB_FILE "SELECT COUNT(*) FROM tickets;"
    Write-Host "Invoices: " -NoNewline
    sqlite3 $DB_FILE "SELECT COUNT(*) FROM invoices;"
    Write-Host "AI Analytics: " -NoNewline
    sqlite3 $DB_FILE "SELECT COUNT(*) FROM ai_analytics;"
    Write-Host "AI Recommendations: " -NoNewline
    sqlite3 $DB_FILE "SELECT COUNT(*) FROM ai_recommendations;"
}

function Run-CustomQuery {
    if ($Query -eq "") {
        $Query = Read-Host "Enter your SQL query"
    }
    Write-Host "🔍 Running query: $Query" -ForegroundColor Cyan
    sqlite3 $DB_FILE $Query
}

# Check if database exists
if (-not (Test-Path $DB_FILE)) {
    Write-Host "❌ Database file '$DB_FILE' not found!" -ForegroundColor Red
    Write-Host "Please run the setup script first: .\scripts\setup\sqlite_setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Main menu loop
if ($Action -eq "menu") {
    do {
        Show-Menu
        $choice = Read-Host "Select an option (1-9)"
        
        switch ($choice) {
            "1" { Show-AllTables }
            "2" { Show-Clients }
            "3" { Show-Tickets }
            "4" { Show-Invoices }
            "5" { Show-AIAnalytics }
            "6" { Show-AIRecommendations }
            "7" { Run-CustomQuery }
            "8" { Show-DatabaseStats }
            "9" { 
                Write-Host "👋 Goodbye!" -ForegroundColor Green
                exit 0 
            }
            default { Write-Host "❌ Invalid option. Please try again." -ForegroundColor Red }
        }
        
        if ($choice -ne "9") {
            Write-Host ""
            Read-Host "Press Enter to continue"
        }
    } while ($choice -ne "9")
} else {
    # Direct action
    switch ($Action) {
        "tables" { Show-AllTables }
        "clients" { Show-Clients }
        "tickets" { Show-Tickets }
        "invoices" { Show-Invoices }
        "analytics" { Show-AIAnalytics }
        "recommendations" { Show-AIRecommendations }
        "stats" { Show-DatabaseStats }
        "query" { Run-CustomQuery }
        default { 
            Write-Host "❌ Invalid action. Use -Action menu to see options." -ForegroundColor Red
        }
    }
}
