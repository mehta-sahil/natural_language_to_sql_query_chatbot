"""
Database Tests

Basic tests to verify database functionality.
Run these tests to ensure database operations work correctly.

Usage:
    python -m pytest tests/test_database.py
    or
    python tests/test_database.py
"""

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.settings import config
from src.database.connection import DatabaseConnection, QueryExecutor


class TestDatabase:
    """Test suite for database operations."""
    
    def __init__(self):
        """Initialize test suite."""
        self.db_connection = DatabaseConnection(config.DATABASE_PATH)
        self.query_executor = QueryExecutor(self.db_connection)
        self.passed_tests = 0
        self.failed_tests = 0
    
    def test_database_connection(self):
        """Test that database connection works."""
        print("\nTest 1: Database Connection")
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                assert result[0] == 1
            print(" PASSED: Database connection works")
            self.passed_tests += 1
            return True
        except Exception as e:
            print(f"FAILED: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_select_query_execution(self):
        """Test that SELECT queries execute correctly."""
        print("\nTest 2: SELECT Query Execution")
        try:
            query = "SELECT * FROM brands LIMIT 5"
            rows, columns = self.query_executor.execute_select_query(query)
            assert len(columns) > 0
            assert 'brand_id' in columns or 'brand_name' in columns
            print(f"PASSED: Query returned {len(rows)} rows with columns {columns}")
            self.passed_tests += 1
            return True
        except Exception as e:
            print(f"FAILED: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_query_validation(self):
        """Test that non-SELECT queries are rejected."""
        print("\nTest 3: Query Validation (Security)")
        try:
            invalid_query = "DELETE FROM brands WHERE brand_id = 1"
            try:
                self.query_executor.execute_select_query(invalid_query)
                print("FAILED: Invalid query was not rejected")
                self.failed_tests += 1
                return False
            except ValueError:
                print("PASSED: Invalid query correctly rejected")
                self.passed_tests += 1
                return True
        except Exception as e:
            print(f"FAILED: Unexpected error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_table_existence(self):
        """Test that all required tables exist."""
        print("\nTest 4: Table Existence")
        required_tables = [
            'brands', 'categories', 'stores', 'staffs',
            'customers', 'products', 'orders', 'order_items', 'stocks'
        ]
        
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                missing_tables = [
                    t for t in required_tables if t not in existing_tables
                ]
                
                if missing_tables:
                    print(f"FAILED: Missing tables: {missing_tables}")
                    self.failed_tests += 1
                    return False
                else:
                    print(f"PASSED: All {len(required_tables)} tables exist")
                    self.passed_tests += 1
                    return True
        except Exception as e:
            print(f"FAILED: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_data_integrity(self):
        """Test that tables have data."""
        print("\nTest 5: Data Integrity")
        try:
            query = "SELECT COUNT(*) FROM products"
            rows, columns = self.query_executor.execute_select_query(query)
            count = rows[0][0]
            
            if count > 0:
                print(f"PASSED: Found {count} products in database")
                self.passed_tests += 1
                return True
            else:
                print("FAILED: No data found in products table")
                self.failed_tests += 1
                return False
        except Exception as e:
            print(f"FAILED: {str(e)}")
            self.failed_tests += 1
            return False
    
    def run_all_tests(self):
        """Run all tests and display summary."""
        print("=" * 60)
        print("DATABASE TESTS")
        print("=" * 60)
        
        self.test_database_connection()
        self.test_select_query_execution()
        self.test_query_validation()
        self.test_table_existence()
        self.test_data_integrity()
        
        print()
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        total_tests = self.passed_tests + self.failed_tests
        print(f"  Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print("=" * 60)
        
        if self.failed_tests == 0:
            print("ALL TESTS PASSED!")
            return True
        else:
            print("SOME TESTS FAILED")
            return False


def main():
    """Run the test suite."""
    tester = TestDatabase()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()