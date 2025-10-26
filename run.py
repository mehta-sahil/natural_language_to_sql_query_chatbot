"""
Main Application Entry Point

This is the main file to run the NLP to SQL application.
It initializes and starts the Streamlit UI.

Usage:
    python run.py
"""

from src.ui.streamlit_app import StreamlitUI


def main():
    """
    Main entry point for the application.
    
    Initializes and runs the Streamlit UI.
    """
    app = StreamlitUI()
    app.run()


if __name__ == "__main__":
    main()