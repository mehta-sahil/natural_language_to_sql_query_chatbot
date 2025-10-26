"""
Streamlit UI Module

Handles all user interface logic and user interactions.
Follows Separation of Concerns - UI logic separated from business logic.
"""

import streamlit as st
import pandas as pd
from typing import Tuple, List

from src.config.settings import config
from src.database.connection import DatabaseConnection, QueryExecutor
from src.ai.query_generator import QueryGeneratorFactory


class StreamlitUI:
    """
    Manages the Streamlit user interface.
    
    This class handles all UI rendering and user interactions.
    Follows Single Responsibility Principle.
    """
    
    def __init__(self):
        """Initialize the Streamlit UI with dependencies."""
        self.config = config
        self.db_connection = DatabaseConnection(self.config.DATABASE_PATH)
        self.query_executor = QueryExecutor(self.db_connection)
        self.query_generator = QueryGeneratorFactory.create_generator(
            api_key=self.config.GENAI_API_KEY,
            model_name=self.config.MODEL_NAME
        )
    
    def setup_page_config(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="SQL Query Generator with Gemini",
            layout="wide"
        )
    
    def render_header(self) -> None:
        """Render the application header."""
        st.title("SQL Query Generator using Google Gemini")
        st.markdown("""
        Convert natural language questions into SQL queries for the bike shop database.
        
        **Examples:**
        - "Show all products from Trek"
        - "List customers in California"
        - "What is the average price of mountain bikes?"
        """)
        st.divider()
    
    def get_user_input(self) -> str:
        """
        Get natural language input from user.
        
        Returns:
            str: User's natural language question
        """
        return st.text_input(
            "Enter your question:",
            key="user_question",
            placeholder="e.g., Show me all brands"
        )
    
    def display_sql_query(self, sql_query: str) -> None:
        """
        Display generated SQL query.
        
        Args:
            sql_query (str): SQL query to display
        """
        st.subheader("Generated SQL Query")
        st.code(sql_query, language='sql')
    
    def display_query_results(
        self, 
        rows: List[Tuple], 
        columns: List[str]
    ) -> None:
        """
        Display query results in a formatted table.
        
        Args:
            rows (List[Tuple]): Query result rows
            columns (List[str]): Column names
        """
        st.subheader("Query Results")
        
        if rows:
            try:
                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                st.caption(
                    f"Total rows: {len(rows)} | "
                    f"Columns: {', '.join(columns)}"
                )
            except Exception as e:
                st.error(f"Error creating table: {str(e)}")
                st.write("Raw data:")
                for i, row in enumerate(rows):
                    st.write(f"Row {i+1}: {row}")
        else:
            st.info("No results found.")
    
    def display_error(self, error_message: str) -> None:
        """
        Display error message to user.
        
        Args:
            error_message (str): Error message to display
        """
        st.error(f"{error_message}")
    
    def display_warning(self, warning_message: str) -> None:
        """
        Display warning message to user.
        
        Args:
            warning_message (str): Warning message to display
        """
        st.warning(f"{warning_message}")
    
    def process_query(self, user_question: str) -> None:
        """
        Process user's natural language question.
        
        This method orchestrates the entire query generation and execution flow.
        
        Args:
            user_question (str): User's natural language question
        """
        try:
            
            with st.spinner("Generating SQL query..."):
                sql_query = self.query_generator.generate_sql_query(user_question)
            
            self.display_sql_query(sql_query)
            
            
            if not self.query_generator.validate_query_is_select(sql_query):
                self.display_error(
                    "Only read-only queries (SELECT) are allowed for safety reasons. "
                    "Please try a different question."
                )
                return
            
            with st.spinner("Executing query..."):
                rows, columns = self.query_executor.execute_select_query(sql_query)
            
            self.display_query_results(rows, columns)
            
        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"An error occurred: {str(e)}")
    
    def run(self) -> None:
        """
        Main method to run the Streamlit application.
        
        This method sets up the UI and handles user interactions.
        """

        self.setup_page_config()

        self.render_header()
        

        user_question = self.get_user_input()
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            submit_button = st.button("Generate Query", type="primary")
        
        with col2:
            clear_button = st.button("Clear")
        
        if clear_button:
            st.rerun()
        
        if submit_button and user_question:
            self.process_query(user_question)
        elif submit_button and not user_question:
            self.display_warning("Please enter a question first!")
        
        
        st.divider()
        st.markdown("""
        <div style='text-align: center; color: gray;'>
        <small>Natural Language to SQL Query Chatbot | Read-only database access</small>
        </div>
        """, unsafe_allow_html=True)