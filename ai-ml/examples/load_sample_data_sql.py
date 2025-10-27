"""
Script to load sample data from SQL file into the database
"""

import sys
import os
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def load_sample_data():
    """Load sample data from SQL file into the database"""
    print("Loading Sample Data")
    print("=" * 20)
    
    # Paths
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'superhack.db')
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'seeds', 'sample_data.sql')
    
    print(f"Database path: {db_path}")
    print(f"SQL file path: {sql_file_path}")
    
    # Check if files exist
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return False
    
    if not os.path.exists(sql_file_path):
        print("❌ SQL file not found")
        return False
    
    try:
        # Read the SQL file
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        
        print("✅ SQL file read successfully")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("✅ Connected to database")
        
        # Execute the SQL script
        # Split by semicolon to execute each statement separately
        statements = sql_script.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Warning: Could not execute statement: {e}")
                    print(f"Statement: {statement[:50]}...")
        
        # Commit changes
        conn.commit()
        print("✅ Sample data loaded successfully")
        
        # Verify data was loaded
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]
        print(f"📊 Clients in database: {client_count}")
        
        cursor.execute("SELECT COUNT(*) FROM tickets")
        ticket_count = cursor.fetchone()[0]
        print(f"📊 Tickets in database: {ticket_count}")
        
        cursor.execute("SELECT COUNT(*) FROM invoices")
        invoice_count = cursor.fetchone()[0]
        print(f"📊 Invoices in database: {invoice_count}")
        
        # Close connection
        conn.close()
        print("✅ Database connection closed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        return False


def main():
    """Main function"""
    print("SuperHack Sample Data Loader")
    print("=" * 30)
    
    success = load_sample_data()
    
    if success:
        print("\n🎉 Sample data loaded successfully!")
        print("You can now use the AI/ML pipeline with real data.")
        print("\nTry running:")
        print("  python examples/simple_data_access_example.py")
        print("  python src/data/preprocessing.py")
    else:
        print("\n❌ Failed to load sample data")
        print("Check the paths and try again.")


if __name__ == "__main__":
    main()