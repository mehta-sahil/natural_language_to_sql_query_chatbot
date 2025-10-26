"""
Database Connection Module

Handles all database connection and query execution operations.
Follows Single Responsibility Principle and Open/Closed Principle.
"""

import sqlite3
from typing import List, Tuple, Optional
from contextlib import contextmanager


class DatabaseConnection:
    """
    Database connection manager with context manager support.
    
    This class provides a clean interface for database operations
    and ensures proper connection management.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize database connection manager.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection object
            
        Example:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM brands")
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()


class QueryExecutor:
    """
    Executes SQL queries and returns formatted results.
    
    This class is responsible for query execution and result formatting.
    Follows Interface Segregation Principle.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize query executor.
        
        Args:
            db_connection (DatabaseConnection): Database connection manager
        """
        self.db_connection = db_connection
    
    def execute_select_query(
        self,
        sql_query: str
    ) -> Tuple[List[Tuple], List[str]]:
        """
        Execute a SELECT query and return results with column names.
        
        Args:
            sql_query (str): SQL SELECT query to execute
            
        Returns:
            Tuple[List[Tuple], List[str]]: 
                - List of result rows (tuples)
                - List of column names
                
        Raises:
            DatabaseError: If query execution fails
            ValueError: If query is not a SELECT statement
        """

        if not sql_query.strip().upper().startswith("SELECT"):
            raise ValueError(
                "Only SELECT queries are allowed for security reasons."
            )
        
        with self.db_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            return rows, column_names
    
    def get_table_info(self, table_name: str) -> List[Tuple]:
        """
        Get table schema information.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            List[Tuple]: Table schema information
        """
        query = f"PRAGMA table_info({table_name})"
        
        with self.db_connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass