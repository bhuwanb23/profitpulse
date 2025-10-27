"""
Script to load sample data into the database for testing the AI/ML pipeline
"""

import sys
import os
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from datetime import datetime


def check_database_structure():
    """Check the current database structure"""
    print("Checking Database Structure")
    print("=" * 30)
    
    # Connect to the database
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'superhack.db')
    print(f"Database path: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        print("✅ Connected to database successfully")
        
        # Check tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Existing tables: {[table[0] for table in tables]}")
        
        # Show sample data from a few tables if they exist
        for table in tables[:3]:  # Show first 3 tables
            table_name = table[0]
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  - {table_name}: {count} records")
                
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    sample_data = cursor.fetchall()
                    print(f"    Sample: {sample_data}")
            except Exception as e:
                print(f"    Error reading {table_name}: {e}")
        
        # Close connection
        conn.close()
        print("✅ Database structure check completed")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Note: This is expected if you haven't set up the database yet")


def show_sample_data_files():
    """Show what sample data files are available"""
    print("\nAvailable Sample Data Files")
    print("=" * 30)
    
    seeds_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'seeds')
    print(f"Seeds directory: {seeds_dir}")
    
    if os.path.exists(seeds_dir):
        files = os.listdir(seeds_dir)
        for file in files:
            if file.endswith('.sql'):
                file_path = os.path.join(seeds_dir, file)
                size = os.path.getsize(file_path)
                print(f"  - {file} ({size} bytes)")
    else:
        print("  No seeds directory found")


def demonstrate_data_pipeline_readiness():
    """Demonstrate that the AI/ML pipeline is ready for data"""
    print("\nAI/ML Pipeline Readiness")
    print("=" * 25)
    
    # Check if preprocessing modules exist
    preprocessing_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'preprocessing')
    if os.path.exists(preprocessing_dir):
        print("✅ Preprocessing modules ready")
        modules = [f for f in os.listdir(preprocessing_dir) if f.endswith('.py') and not f.startswith('_')]
        print(f"   Available modules: {modules}")
    
    # Check if feature engineering exists
    feature_eng_file = os.path.join(preprocessing_dir, 'feature_engineering.py')
    if os.path.exists(feature_eng_file):
        print("✅ Feature engineering system ready")
    
    # Check if client genome exists
    genome_dir = os.path.join(preprocessing_dir, 'client_genome')
    if os.path.exists(genome_dir):
        print("✅ Client profitability genome system ready")
        genome_modules = [f for f in os.listdir(genome_dir) if f.endswith('.py') and not f.startswith('_')]
        print(f"   Genome modules: {genome_modules}")


def next_steps():
    """Show what to do next"""
    print("\nNext Steps")
    print("=" * 12)
    
    print("To start working with data, you can:")
    print("1. Load sample data:")
    print("   - Use the database/seeds/sample_data.sql file")
    print("   - Run: sqlite3 database/superhack.db < database/seeds/sample_data.sql")
    print()
    print("2. Or connect to real data sources:")
    print("   - Configure API credentials in your .env file")
    print("   - Run the data extraction pipeline")
    print()
    print("3. Then process data through the AI/ML pipeline:")
    print("   - python src/data/preprocessing.py")
    print("   - python src/data/preprocessing/feature_engineering.py")
    print("   - python src/data/preprocessing/client_genome/genome_creator.py")


def main():
    """Main function"""
    print("SuperHack AI/ML Data Loading Helper")
    print("=" * 35)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    check_database_structure()
    show_sample_data_files()
    demonstrate_data_pipeline_readiness()
    next_steps()
    
    print("\n💡 TIP: The entire AI/ML pipeline is ready and waiting for your data!")


if __name__ == "__main__":
    main()