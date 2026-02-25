"""
AI Query Generator Module

Handles natural language to SQL conversion using Google Gemini AI.
Follows Single Responsibility Principle - only handles AI query generation.
"""

import google.generativeai as genai
from typing import Optional


class PromptTemplate:
    """
    Manages AI prompt templates for SQL generation.
    
    This class encapsulates prompt engineering logic.
    Follows Single Responsibility Principle.
    """
    
    @staticmethod
    def get_sql_generation_prompt() -> str:
        """
        Get the prompt template for SQL query generation.
        
        Returns:
            str: Complete prompt with database schema and examples
        """
        return """
You are an expert SQL assistant. Your task is to convert natural language questions into accurate, efficient SQL queries for a bike shop database.

Database Schema:
- **brands**: (brand_id INTEGER PRIMARY KEY, brand_name TEXT)
- **categories**: (category_id INTEGER PRIMARY KEY, category_name TEXT)
- **stores**: (store_id INTEGER PRIMARY KEY, store_name TEXT, phone TEXT, email TEXT, street TEXT, city TEXT, state TEXT, zip_code TEXT)
- **staffs**: (staff_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, phone TEXT, active INTEGER, store_id INTEGER, manager_id INTEGER) - References stores(store_id) and staffs(staff_id) for manager
- **customers**: (customer_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, phone TEXT, email TEXT, street TEXT, city TEXT, state TEXT, zip_code TEXT)
- **products**: (product_id INTEGER PRIMARY KEY, product_name TEXT, brand_id INTEGER, category_id INTEGER, model_year INTEGER, list_price REAL) - References brands(brand_id) and categories(category_id)
- **orders**: (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_status INTEGER, order_date TEXT, required_date TEXT, shipped_date TEXT, store_id INTEGER, staff_id INTEGER) - References customers(customer_id), stores(store_id), staffs(staff_id)
- **order_items**: (order_id INTEGER, item_id INTEGER, product_id INTEGER, quantity INTEGER, list_price REAL, discount REAL) - Primary key (order_id, item_id), references orders(order_id) and products(product_id)
- **stocks**: (store_id INTEGER, product_id INTEGER, quantity INTEGER) - Primary key (store_id, product_id), references stores(store_id) and products(product_id)

Guidelines:
- Generate only SELECT SQL queries for read-only access, no explanations or additional text.
- Use appropriate JOINs for multi-table queries.
- Ensure queries are efficient and avoid unnecessary complexity.
- Handle aggregations, filters, and sorting as needed.
- For date fields, assume TEXT format (YYYY-MM-DD).
- If the question is ambiguous, choose the most logical interpretation based on the schema.
- Do not generate INSERT, UPDATE, DELETE, DROP, or any modification queries.

Examples:
1. Question: "Show me all products from Trek."
   SQL: SELECT * FROM products WHERE brand_id = (SELECT brand_id FROM brands WHERE brand_name = 'Trek');

2. Question: "How many orders were placed in January 2023?"
   SQL: SELECT COUNT(*) FROM orders WHERE order_date LIKE '2023-01-%';

3. Question: "List customers who have placed orders with a total value over $1000."
   SQL: SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_id HAVING SUM(oi.quantity * oi.list_price * (1 - oi.discount)) > 1000;

4. Question: "What is the average price of products in the Mountain Bikes category?"
   SQL: SELECT AVG(list_price) FROM products WHERE category_id = (SELECT category_id FROM categories WHERE category_name = 'Mountain Bikes');

5. Question: "Show the top 5 stores by total sales."
   SQL: SELECT s.store_name, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales FROM stores s JOIN orders o ON s.store_id = o.store_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY s.store_id ORDER BY total_sales DESC LIMIT 5;

IMPORTANT: Do not include ``` or the word 'sql' in your output. Return only the raw SQL query.
"""


class GeminiQueryGenerator:
    """
    Generates SQL queries from natural language using Google Gemini AI.
    
    This class handles all AI model interactions for query generation.
    Follows Interface Segregation Principle.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """
        Initialize Gemini query generator.
        
        Args:
            api_key (str): Google Gemini API key
            model_name (str): Name of the Gemini model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self._configure_api()
        self.prompt_template = PromptTemplate()
    
    def _configure_api(self) -> None:
        """
        Configure Google Gemini API with the provided API key.
        
        Raises:
            Exception: If API configuration fails
        """
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise Exception(f"Failed to configure Gemini API: {str(e)}")
    
    def generate_sql_query(self, natural_language_question: str) -> str:
        """
        Generate SQL query from natural language question.
        
        Args:
            natural_language_question (str): User's question in natural language
            
        Returns:
            str: Generated SQL query
            
        Raises:
            Exception: If query generation fails
        """
        try:
            model = genai.GenerativeModel(self.model_name)
            prompt = self.prompt_template.get_sql_generation_prompt()
            
            response = model.generate_content([prompt, natural_language_question])
            
            sql_query = response.text.strip()
            
            if sql_query.startswith("```"):
                sql_query = sql_query.split("\n", 1)[1]
            if sql_query.endswith("```"):
                sql_query = sql_query.rsplit("\n", 1)[0]
            
            if sql_query.lower().startswith("sql"):
                sql_query = sql_query[3:].strip()
            
            return sql_query.strip()
            
        except Exception as e:
            raise Exception(f"Failed to generate SQL query: {str(e)}")
    
    def validate_query_is_select(self, sql_query: str) -> bool:
        """
        Validate that the generated query is a SELECT statement.
        
        Args:
            sql_query (str): SQL query to validate
            
        Returns:
            bool: True if query is a SELECT statement, False otherwise
        """
        return sql_query.strip().upper().startswith("SELECT")



class LLMQueryGenerator:
    """
    Generates SQL queries from natural language using an LLM provider (e.g., Gemini).
    
    This class handles all AI model interactions for query generation.
    Follows Interface Segregation Principle.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-pro"):
        """
        Initialize LLM query generator.
        
        Args:
            api_key (str): LLM provider API key
            model_name (str): Name of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self._configure_api()
        self.prompt_template = PromptTemplate()
    
    def _configure_api(self) -> None:
        """
        Configure the provider SDK (currently Google Gemini via google.generativeai).
        """
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise Exception(f"Failed to configure LLM API: {str(e)}")
    
    def generate_sql_query(self, natural_language_question: str) -> str:
        """
        Generate SQL query from natural language question.
        """
        try:
            model = genai.GenerativeModel(self.model_name)
            prompt = self.prompt_template.get_sql_generation_prompt()
            response = model.generate_content([prompt, natural_language_question])
            sql_query = response.text.strip()
            if sql_query.startswith("```"):
                sql_query = sql_query.split("\n", 1)[1]
            if sql_query.endswith("```"):
                sql_query = sql_query.rsplit("\n", 1)[0]
            if sql_query.lower().startswith("sql"):
                sql_query = sql_query[3:].strip()
            return sql_query.strip()
        except Exception as e:
            raise Exception(f"Failed to generate SQL query: {str(e)}")
    
    def validate_query_is_select(self, sql_query: str) -> bool:
        return sql_query.strip().upper().startswith("SELECT")


GeminiQueryGenerator = LLMQueryGenerator


class QueryGeneratorFactory:
    """
    Factory class for creating query generator instances.
    
    Follows Factory Pattern and Dependency Inversion Principle.
    """
    
    @staticmethod
    def create_generator(api_key: str, model_name: str = "gemini-2.5-flash") -> LLMQueryGenerator:
        """
        Create and return a query generator instance.
        """
        return LLMQueryGenerator(api_key, model_name)
