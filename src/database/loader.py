"""
Database Schema Loader Module

Handles database schema creation and CSV data loading.
Follows Single Responsibility Principle - only manages data loading.
"""

import sqlite3
import csv
import os
from typing import Dict


class SchemaManager:
    """
    Manages database schema creation.
    
    This class is responsible for creating and managing database tables.
    Follows Open/Closed Principle - extensible for new tables.
    """
    
    TABLE_SCHEMAS: Dict[str, str] = {
        'brands': """
        CREATE TABLE IF NOT EXISTS brands (
            brand_id INTEGER PRIMARY KEY,
            brand_name TEXT NOT NULL
        );
        """,
        'categories': """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL
        );
        """,
        'stores': """
        CREATE TABLE IF NOT EXISTS stores (
            store_id INTEGER PRIMARY KEY,
            store_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT
        );
        """,
        'staffs': """
        CREATE TABLE IF NOT EXISTS staffs (
            staff_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            active INTEGER NOT NULL,
            store_id INTEGER,
            manager_id INTEGER,
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (manager_id) REFERENCES staffs(staff_id)
        );
        """,
        'customers': """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT
        );
        """,
        'products': """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            brand_id INTEGER,
            category_id INTEGER,
            model_year INTEGER,
            list_price REAL,
            FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );
        """,
        'orders': """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_status INTEGER,
            order_date TEXT,
            required_date TEXT,
            shipped_date TEXT,
            store_id INTEGER,
            staff_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (staff_id) REFERENCES staffs(staff_id)
        );
        """,
        'order_items': """
        CREATE TABLE IF NOT EXISTS order_items (
            order_id INTEGER,
            item_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            list_price REAL,
            discount REAL,
            PRIMARY KEY (order_id, item_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """,
        'stocks': """
        CREATE TABLE IF NOT EXISTS stocks (
            store_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            PRIMARY KEY (store_id, product_id),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    }
    
    def __init__(self, db_path: str):
        """
        Initialize schema manager.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
    
    def create_tables(self) -> None:
        """
        Create all database tables based on defined schemas.
        
        Raises:
            sqlite3.Error: If table creation fails
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for table_name, schema in self.TABLE_SCHEMAS.items():
                cursor.execute(schema)
                print(f"Table '{table_name}' created successfully")
            
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Failed to create tables: {str(e)}")
        finally:
            conn.close()


class CSVDataLoader:
    """
    Loads data from CSV files into database tables.
    
    This class handles CSV file reading and data insertion.
    Follows Dependency Inversion Principle.
    """
    
    def __init__(self, db_path: str, data_folder: str):
        """
        Initialize CSV data loader.
        
        Args:
            db_path (str): Path to SQLite database file
            data_folder (str): Path to folder containing CSV files
        """
        self.db_path = db_path
        self.data_folder = data_folder
    
    def load_csv_to_table(self, table_name: str, csv_file: str) -> None:
        """
        Load data from a CSV file into a database table.
        
        Args:
            table_name (str): Name of the target table
            csv_file (str): Path to the CSV file
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            Exception: If data insertion fails
        """
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                columns = reader.fieldnames
                placeholders = ', '.join(['?' for _ in columns])
                insert_query = (
                    f"INSERT OR IGNORE INTO {table_name} "
                    f"({', '.join(columns)}) VALUES ({placeholders})"
                )
                
                for row in reader:
                    values = [row[col] for col in columns]
                    cursor.execute(insert_query, values)
            
            conn.commit()
            print(f"Data loaded into '{table_name}' successfully")
        except Exception as e:
            conn.rollback()
            raise Exception(f"Failed to load data into {table_name}: {str(e)}")
        finally:
            conn.close()
    
    def load_all_data(self) -> None:
        """
        Load data from all CSV files into corresponding tables.
        
        CSV files mapping:
            - brands.csv -> brands table
            - categories.csv -> categories table
            - And so on...
        """
        csv_files_mapping = {
            'brands': os.path.join(self.data_folder, 'brands.csv'),
            'categories': os.path.join(self.data_folder, 'categories.csv'),
            'stores': os.path.join(self.data_folder, 'stores.csv'),
            'staffs': os.path.join(self.data_folder, 'staffs.csv'),
            'customers': os.path.join(self.data_folder, 'customers.csv'),
            'products': os.path.join(self.data_folder, 'products.csv'),
            'orders': os.path.join(self.data_folder, 'orders.csv'),
            'order_items': os.path.join(self.data_folder, 'order_items.csv'),
            'stocks': os.path.join(self.data_folder, 'stocks.csv')
        }
        
        for table_name, csv_file in csv_files_mapping.items():
            try:
                self.load_csv_to_table(table_name, csv_file)
            except FileNotFoundError as e:
                print(f"Warning: {e}")
            except Exception as e:
                print(f"Error: {e}")