"""
Setup Verification Script

Verifies that all components are properly configured and working.

Usage:
    python scripts/verify_setup.py
"""

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def check_environment_variables():
    """Check if required environment variables are set."""
    print("Checking environment variables...")
    try:
        from src.config.settings import config
        api_key = config.GENAI_API_KEY
        print("GENAI_API_KEY is set")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def check_database_exists():
    """Check if database file exists."""
    print("\nChecking database file...")
    from src.config.settings import config
    
    if os.path.exists(config.DATABASE_PATH):
        print(f"Database file exists: {config.DATABASE_PATH}")
        return True
    else:
        print(f"Database file not found: {config.DATABASE_PATH}")
        return False


def check_database_tables():
    """Check if all required tables exist in database."""
    print("\nChecking database tables...")
    import sqlite3
    from src.config.settings import config
    
    required_tables = [
        'brands', 'categories', 'stores', 'staffs',
        'customers', 'products', 'orders', 'order_items', 'stocks'
    ]
    
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        all_exist = True
        for table in required_tables:
            if table in existing_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table:15s}: {count:5d} rows")
            else:
                print(f"{table:15s}: Missing")
                all_exist = False
        
        conn.close()
        return all_exist
        
    except Exception as e:
        print(f"Error checking tables: {str(e)}")
        return False


def check_csv_files():
    """Check if all required CSV files exist."""
    print("\nChecking CSV data files...")
    from src.config.settings import config
    
    required_files = [
        'brands.csv', 'categories.csv', 'stores.csv', 'staffs.csv',
        'customers.csv', 'products.csv', 'orders.csv', 
        'order_items.csv', 'stocks.csv'
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = os.path.join(config.DATA_FOLDER, filename)
        if os.path.exists(filepath):
            print(f"{filename}")
        else:
            print(f"{filename} - Not found")
            all_exist = False
    
    return all_exist


def check_dependencies():
    """Check if all required Python packages are installed."""
    print("\nChecking Python dependencies...")
    
    dependencies = {
        'streamlit': 'Streamlit',
        'google.generativeai': 'Google Generative AI',
        'pandas': 'Pandas',
        'dotenv': 'Python Dotenv'
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"{name}")
        except ImportError:
            print(f"{name} - Not installed")
            all_installed = False
    
    return all_installed


def check_api_connection():
    """Test connection to Gemini API."""
    print("\nTesting Gemini API connection...")
    try:
        import google.generativeai as genai
        from src.config.settings import config
        
        genai.configure(api_key=config.GENAI_API_KEY)
        models = list(genai.list_models())
        
        if models:
            print(f"API connection successful")
            print(f"Found {len(models)} available models")
            return True
        else:
            print(f"API connected but no models found")
            return False
            
    except Exception as e:
        print(f" API connection failed: {str(e)}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("SETUP VERIFICATION - Natural Language to SQL Query Chatbot")
    print("=" * 60)
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_environment_variables),
        ("CSV Files", check_csv_files),
        ("Database File", check_database_exists),
        ("Database Tables", check_database_tables),
        ("API Connection", check_api_connection)
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    print()
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print()
    
    all_passed = all(results.values())
    
    for check_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {check_name:25s}: {status}")
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("ALL CHECKS PASSED - System is ready!")
        print("=" * 60)
        print()
        print("You can now run the application:")
        print("  python run.py")
        print()
    else:
        print("SOME CHECKS FAILED")
        print("=" * 60)
        print()
        print("Please fix the issues above before running the application.")
        print()
        print("Common fixes:")
        print("  • Missing dependencies: pip install -r requirements.txt")
        print("  • Missing .env file: Copy .env.example to .env and add your API key")
        print("  • Missing database: Run python scripts/setup_database.py")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()