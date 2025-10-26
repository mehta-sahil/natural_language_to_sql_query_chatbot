"""
Database Setup Script

This script initializes the database with schema and loads data from CSV files.
Run this script before starting the application for the first time.

Usage:
    python scripts/setup_database.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.settings import config
from src.database.loader import SchemaManager, CSVDataLoader


def main():
    """
    Main function to set up the database.
    
    Steps:
        1. Create database tables from schema
        2. Load data from CSV files into tables
        3. Verify data was loaded successfully
    """
    print("=" * 60)
    print("DATABASE SETUP - Bike Shop CSV to SQL Database")
    print("=" * 60)
    print()

    print("Step 1: Creating database tables...")
    print("-" * 60)
    try:
        schema_manager = SchemaManager(config.DATABASE_PATH)
        schema_manager.create_tables()
        print("All tables created successfully!")
        print()
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        sys.exit(1)
    
    print("Step 2: Loading data from CSV files...")
    print("-" * 60)
    try:
        csv_loader = CSVDataLoader(config.DATABASE_PATH, config.DATA_FOLDER)
        csv_loader.load_all_data()
        print("All data loaded successfully!")
        print()
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        sys.exit(1)
    
    print("Step 3: Verifying database setup...")
    print("-" * 60)
    import sqlite3
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    tables = [
        'brands', 'categories', 'stores', 'staffs',
        'customers', 'products', 'orders', 'order_items', 'stocks'
    ]
    
    print("\nTable Row Counts:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  • {table:15s}: {count:5d} rows")
    
    conn.close()
    
    print()
    print("=" * 60)
    print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Next step: Run the application using:")
    print("  python run.py")
    print()


if __name__ == "__main__":
    main()