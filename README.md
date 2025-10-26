# Natural Language to SQL Query Chatbot

A Natural Language to SQL query generator using Google's Gemini AI API for a bike shop database. This project follows industry-standard design principles and best practices.

## Industry Standards Implemented

This project follows **4 key industry standards**:

1. **Code Structure & Modularization** - Clean separation into modules
2. **SOLID Principles** - All 5 principles implemented
3. **Separation of Concerns** - Clear layer separation
4. **Code Readability & Documentation** - Comprehensive docs and comments


## Project Structure

```
NLC/
├── src/                          # Source code (modular design)
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py          # Centralized settings
│   ├── database/                 # Data access layer
│   │   ├── __init__.py
│   │   ├── connection.py        # DB connection & query execution
│   │   └── loader.py            # Schema & data loading
│   ├── ai/                       # AI integration layer
│   │   ├── __init__.py
│   │   └── query_generator.py  # Gemini AI query generation
│   └── ui/                       # Presentation layer
│       ├── __init__.py
│       └── streamlit_app.py    # Streamlit interface
├── data/                         # CSV data files
│   ├── brands.csv
│   ├── categories.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── staffs.csv
│   ├── stocks.csv
│   └── stores.csv
├── scripts/                      # Utility scripts
│   ├── setup_database.py        # Database initialization
│   └── verify_setup.py          # Setup verification
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_database.py         # Database tests
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md          # Architecture details
│   └── API_DOCUMENTATION.md     # API reference
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── run.py                        # Main entry point
└── README.md                     # This file
```

## Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### Installation Steps

Open VS Code terminal and run these commands:

#### 1. Clone Repository (if from GitHub)

```cmd
git clone https://github.com/meethp1884/nlc_nl2sql.git
cd nlc_nl2sql
```

#### 2. Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

#### 4. Configure Environment

```cmd
copy .env.example .env
```

Then edit `.env` file and add your API key:
```
GENAI_API_KEY="your_google_gemini_api_key_here"
```

#### 5. Setup Database

```cmd
python scripts\setup_database.py
```

Expected output:
```
============================================================
DATABASE SETUP - Bike Shop SQL Database
============================================================

Step 1: Creating database tables...
------------------------------------------------------------
Table 'brands' created successfully
Table 'categories' created successfully
...
All tables created successfully!
```

#### 6. Verify Setup

```cmd
python scripts\verify_setup.py
```

Expected output:
```
============================================================
SETUP VERIFICATION - NLP to SQL Project
============================================================

Checking environment variables...
  GENAI_API_KEY is set
...
ALL CHECKS PASSED - System is ready!
```

#### 7. Run Application

```cmd
streamlit run run.py
```

Or alternative:
```cmd
python run.py
```

The application will open in your browser at `http://localhost:8501`

##Testing

### Run Tests

```cmd
python tests\test_database.py
```

Expected output:
```
============================================================
DATABASE TESTS
============================================================

Test 1: Database Connection
  PASSED: Database connection works

Test 2: SELECT Query Execution
  PASSED: Query returned 5 rows with columns ['brand_id', 'brand_name']
...
ALL TESTS PASSED!
```

## Usage Examples

### Example Queries

Once the application is running, try these natural language queries:

**Easy:**
- "Show all brands"
- "List all products from Trek"
- "How many customers are there?"

**Medium:**
- "Show the top 5 products by price"
- "List customers who live in California"
- "What is the total number of orders per store?"

**Hard:**
- "Find customers who have spent more than $1000"
- "Which product categories have the highest average price?"
- "Show the top 3 stores by total sales revenue"

## Architecture Overview

### Layer Separation

```
┌─────────────────────────────────────┐
│   Presentation Layer (UI)           │  ← User interaction
│   src/ui/streamlit_app.py           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Application Layer (Business)      │  ← Business logic
│   src/ai/query_generator.py         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Data Access Layer (Database)      │  ← Data operations
│   src/database/connection.py        │
│   src/database/loader.py            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Infrastructure Layer (Config)     │  ← Configuration
│   src/config/settings.py            │
└─────────────────────────────────────┘
```

### SOLID Principles Implementation

1. **Single Responsibility**: Each class has one job
   - `Config`: Manages configuration only
   - `QueryExecutor`: Executes queries only
   - `GeminiQueryGenerator`: Generates SQL only

2. **Open/Closed**: Extensible without modification
   - New tables can be added without changing code
   - New AI models can be integrated easily

3. **Liskov Substitution**: Interchangeable components
   - Database connections can be swapped
   - Query executors follow same interface

4. **Interface Segregation**: Focused interfaces
   - Classes only expose methods they need
   - No bloated interfaces

5. **Dependency Inversion**: Depends on abstractions
   - High-level modules don't depend on low-level details
   - Configuration injected, not hardcoded

## Documentation

- **Architecture**: See `docs/ARCHITECTURE.md` for design details
- **API Reference**: See `docs/API_DOCUMENTATION.md` for API docs


## Security Features

- **Read-Only Access**: Only SELECT queries allowed
- **Input Validation**: Query type checking before execution
- **Error Handling**: Comprehensive error messages
- **Environment Variables**: Secure API key management
- **SQL Injection Protection**: Parameterized queries

## Development

### Adding New Features

1. **New AI Model**: Add to `src/ai/query_generator.py`
2. **New Table**: Update `src/database/loader.py`
3. **New UI Component**: Extend `src/ui/streamlit_app.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all classes and methods
- Keep functions focused and small

## 📦 Dependencies

```
streamlit              # Web application framework
google-generativeai    # Google Gemini AI API
python-dotenv          # Environment variable management
pandas                 # Data manipulation
```

## Troubleshooting

### Common Issues

**Issue**: Module not found error
```cmd
# Solution: Ensure you're in project root and venv is activated
cd NLC
venv\Scripts\activate
```

**Issue**: Database not found
```cmd
# Solution: Run database setup
python scripts\setup_database.py
```

**Issue**: API key error
```cmd
# Solution: Check .env file exists and has correct API key
type .env
```
