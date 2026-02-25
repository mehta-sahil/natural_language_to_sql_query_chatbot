"""
Configuration Settings Module

This module handles all configuration settings for the application.
Follows Single Responsibility Principle (SRP) - only manages configuration.
"""

import os
from dotenv import load_dotenv
from typing import Optional


class Config:
    """
    Configuration class that manages all application settings.
    
    Attributes:
        GENAI_API_KEY (str): Google Gemini API key from environment
        DATABASE_PATH (str): Path to SQLite database file
        DATA_FOLDER (str): Path to CSV data files folder
        MODEL_NAME (str): Name of the Gemini model to use
    """
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        self._validate_environment()
    
    @property
    def GENAI_API_KEY(self) -> str:
        """
        Get the Gemini API key from environment variables.
        
        Returns:
            str: API key for Google Gemini
            
        Raises:
            ValueError: If API key is not set
        """
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "GENAI_API_KEY not found in environment variables. "
                "Please check your .env file."
            )
        return api_key
    
    @property
    def DATABASE_PATH(self) -> str:
        """Get database file path."""
        return "bikes.db"
    
    @property
    def DATA_FOLDER(self) -> str:
        """Get data folder path."""
        return "data/"
    
    @property
    def MODEL_NAME(self) -> str:
        """Get Gemini model name."""
        return "gemini-2.5-flash"
    
    def _validate_environment(self) -> None:
        """
        Validate that all required environment variables are set.
        
        Raises:
            ValueError: If required variables are missing
        """
        required_vars = ["GENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please create a .env file with these variables."
            )



config = Config()
