# Architecture Documentation

## Overview

This document explains the architecture of the NLP to SQL project, following industry-standard design principles.

## Design Principles Applied

### 1. SOLID Principles

#### Single Responsibility Principle (SRP)
Each class has one reason to change:
- `Config`: Manages configuration only
- `DatabaseConnection`: Handles database connections only
- `QueryExecutor`: Executes queries only
- `SchemaManager`: Manages schema creation only
- `CSVDataLoader`: Loads CSV data only
- `GeminiQueryGenerator`: Generates SQL queries using AI only
- `StreamlitUI`: Handles UI rendering only

#### Open/Closed Principle (OCP)
Classes are open for extension but closed for modification:
- `SchemaManager`: New tables can be added to `TABLE_SCHEMAS` without modifying the class logic
- `PromptTemplate`: Prompts can be extended without changing the generator
- `QueryExecutor`: New query types can be added through inheritance

#### Liskov Substitution Principle (LSP)
Derived classes can replace base classes without breaking functionality:
- All query executors follow the same interface
- Database connections can be swapped with different implementations

#### Interface Segregation Principle (ISP)
Clients are not forced to depend on interfaces they don't use:
- `QueryExecutor` has focused methods for specific query types
- UI components only use methods they need

#### Dependency Inversion Principle (DIP)
High-level modules don't depend on low-level modules:
- `StreamlitUI` depends on abstractions (`QueryExecutor`, `QueryGenerator`)
- Configuration is injected, not hardcoded

### 2. Separation of Concerns

The project is organized into distinct layers:

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│         (src/ui/)                   │
│  - User Interface                   │
│  - Input Handling                   │
│  - Result Display                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Application Layer           │
│         (src/ai/)                   │
│  - Business Logic                   │
│  - Query Generation                 │
│  - AI Integration                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data Access Layer           │
│         (src/database/)             │
│  - Database Operations              │
│  - Query Execution                  │
│  - Data Loading                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Infrastructure Layer           │
│         (src/config/)               │
│  - Configuration Management         │
│  - Environment Variables            │
└─────────────────────────────────────┘
```

## Module Structure

### Configuration Module (`src/config/`)
**Purpose**: Centralized configuration management

**Components**:
- `settings.py`: Configuration class with environment variable handling

**Responsibilities**:
- Load and validate environment variables
- Provide configuration values to other modules
- Ensure proper application setup

### Database Module (`src/database/`)
**Purpose**: All database-related operations

**Components**:
- `connection.py`: Database connection management and query execution
- `loader.py`: Schema creation and CSV data loading

**Responsibilities**:
- Manage database connections with context managers
- Execute SQL queries safely
- Load data from CSV files
- Create and manage database schema

### AI Module (`src/ai/`)
**Purpose**: AI-powered query generation

**Components**:
- `query_generator.py`: Gemini AI integration for NL to SQL conversion

**Responsibilities**:
- Configure Gemini API
- Generate SQL from natural language
- Manage prompt templates
- Validate generated queries

### UI Module (`src/ui/`)
**Purpose**: User interface and interaction

**Components**:
- `streamlit_app.py`: Streamlit-based user interface

**Responsibilities**:
- Render UI components
- Handle user input
- Display results
- Orchestrate application flow

## Data Flow

```
User Input (Natural Language)
         │
         ▼
  StreamlitUI.get_user_input()
         │
         ▼
  GeminiQueryGenerator.generate_sql_query()
         │
         ▼
  Generated SQL Query
         │
         ▼
  QueryExecutor.execute_select_query()
         │
         ▼
  Query Results (rows + columns)
         │
         ▼
  StreamlitUI.display_query_results()
         │
         ▼
  User sees formatted table
```

## Key Design Decisions

### 1. Context Managers for Database Connections
Using Python's context manager pattern ensures:
- Automatic connection cleanup
- Proper error handling
- Resource management

### 2. Factory Pattern for Query Generators
The `QueryGeneratorFactory` provides:
- Centralized object creation
- Easy configuration changes
- Testability

### 3. Dependency Injection
Dependencies are injected rather than created internally:
- Improves testability
- Reduces coupling
- Enables easier modifications

### 4. Configuration Object Pattern
Centralized configuration provides:
- Single source of truth
- Easy environment variable management
- Validation at startup

## Security Considerations

1. **Read-Only Queries**: Only SELECT statements are allowed
2. **Query Validation**: All queries are validated before execution
3. **Environment Variables**: Sensitive data stored in .env file
4. **Error Handling**: Comprehensive error handling prevents data exposure

## Extensibility

The architecture supports easy extension:

### Adding New Tables
1. Add schema to `SchemaManager.TABLE_SCHEMAS`
2. Add CSV file mapping in `CSVDataLoader.load_all_data()`
3. Update documentation

### Adding New AI Models
1. Create new generator class inheriting from base
2. Update factory to support new model
3. No changes needed in UI or database layers

### Adding New UI Features
1. Add methods to `StreamlitUI` class
2. Business logic remains unchanged
3. Clear separation of concerns maintained

## Testing

The project includes automated tests to verify functionality:

### Database Functionality Tests

1. Tests database connection and query execution
2. Validates security (rejects non-SELECT queries)
3. Verifies table creation and data integrity

### Setup Verification Tests

1. Validates Python dependencies installation
2. Checks environment variables and CSV files
3. Tests Gemini API connectivity

## File Organization

```
NLC/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── loader.py
│   ├── ai/
│   │   ├── __init__.py
│   │   └── query_generator.py
│   └── ui/
│       ├── __init__.py
│       └── streamlit_app.py
├── data/
│   └── (your existing CSV files)
├── tests/
│   ├── __init__.py
│   └── test_database.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── API_DOCUMENTATION.md
├── scripts/
│   ├── setup_database.py
│   └── verify_setup.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

## Best Practices Implemented

1. **Code Organization**: Logical module structure
2. **Naming Conventions**: Clear, descriptive names
3. **Documentation**: Comprehensive docstrings
4. **Error Handling**: Try-except blocks with specific exceptions
5. **Type Hints**: Type annotations for better code clarity
6. **Constants**: Configuration values in config module


## Future Improvements

1. Add logging framework (replace print statements)
2. Implement caching for frequent queries
3. Add more comprehensive test suite
4. Add query history tracking
5. Implement user authentication
6. Add query performance monitoring