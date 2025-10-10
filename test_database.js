// Test database from new location
const sqlite3 = require('sqlite3').verbose();

console.log('🔍 Testing database from new location...');

const db = new sqlite3.Database('database/superhack.db');

// Test connection
db.get("SELECT COUNT(*) as count FROM clients", (err, row) => {
    if (err) {
        console.error('❌ Error connecting to database:', err);
    } else {
        console.log(`✅ Database connection successful! Found ${row.count} clients.`);
    }
    db.close();
});
