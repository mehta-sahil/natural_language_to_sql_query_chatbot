# API Documentation

## Module APIs

### Configuration Module (`src.config.settings`)

#### Class: `Config`

Configuration manager for application settings.

**Methods**:

##### `__init__(self)`
Initialize configuration and load environment variables.

**Raises**:
- `ValueError`: If required environment variables are missing

##### `GENAI_API_KEY` (property)
Get the Gemini API key.

**Returns**: `str` - API key for Google Gemini

**Raises**: `ValueError` - If API key is not set

##### `DATABASE_PATH` (property)
Get database file path.

**Returns**: `str` - Path to SQLite database file

##### `DATA_FOLDER` (property)
Get data folder path.

**Returns**: `str` - Path to CSV data files folder

##### `MODEL_NAME` (property)
Get Gemini model name.

**Returns**: `str` - Name of the Gemini model to use

---

### Database Module (`src.database.connection`)

#### Class: `DatabaseConnection`

Database connection manager with context manager support.

**Constructor**:
```python
DatabaseConnection(db_path: str)
```

**Parameters**:
- `db_path` (str): Path to SQLite database file

**Methods**:

##### `get_connection(self)`
Context manager for database connections.

**Yields**: `sqlite3.Connection` - Database connection object

**Example**:
```python
with db.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brands")
```

---

#### Class: `QueryExecutor`

Executes SQL queries and returns formatted results.

**Constructor**:
```python
QueryExecutor(db_connection: DatabaseConnection)
```

**Parameters**:
- `db_connection` (DatabaseConnection): Database connection manager

**Methods**:

##### `execute_select_query(self, sql_query: str)`
Execute a SELECT query and return results.

**Parameters**:
- `sql_query` (str): SQL SELECT query to execute

**Returns**: `Tuple[List[Tuple], List[str]]`
- List of result rows (tuples)
- List of column names

**Raises**:
- `DatabaseError`: If query execution fails
- `ValueError`: If query is not a SELECT statement

**Example**:
```python
executor = QueryExecutor(db_connection)
rows, columns = executor.execute_select_query("SELECT * FROM brands")
```

##### `get_table_info(self, table_name: str)`
Get table schema information.

**Parameters**:
- `table_name` (str): Name of the table

**Returns**: `List[Tuple]` - Table schema information

---

### Database Module (`src.database.loader`)

#### Class: `SchemaManager`

Manages database schema creation.

**Constructor**:
```python
SchemaManager(db_path: str)
```

**Parameters**:
- `db_path` (str): Path to SQLite database file

**Methods**:

##### `create_tables(self)`
Create all database tables based on defined schemas.

**Raises**: `sqlite3.Error` - If table creation fails

**Example**:
```python
schema_manager = SchemaManager("bikes.db")
schema_manager.create_tables()
```

---

#### Class: `CSVDataLoader`

Loads data from CSV files into database tables.

**Constructor**:
```python
CSVDataLoader(db_path: str, data_folder: str)
```

**Parameters**:
- `db_path` (str): Path to SQLite database file
- `data_folder` (str): Path to folder containing CSV files

**Methods**:

##### `load_csv_to_table(self, table_name: str, csv_file: str)`
Load data from a CSV file into a database table.

**Parameters**:
- `table_name` (str): Name of the target table
- `csv_file` (str): Path to the CSV file

**Raises**:
- `