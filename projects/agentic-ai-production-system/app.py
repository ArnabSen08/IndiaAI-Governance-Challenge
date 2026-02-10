"""
Main Streamlit application for the Multi-Agent AI System.
Production-ready web interface with comprehensive error handling and monitoring.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.web.interface import MultiAgentInterface
from src.core.config import Config
from src.utils.logger import setup_logger
from src.core.health import HealthChecker

# Configure page
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point."""
    
    # Initialize configuration and logging
    config = Config()
    logger = setup_logger()
    
    # Initialize health checker
    health_checker = HealthChecker(config)
    
    # Check system health
    health_status = health_checker.check_system_health()
    
    if not health_status["healthy"]:
        st.error("⚠️ System Health Issues Detected")
        st.error(f"Issues: {', '.join(health_status['issues'])}")
        st.stop()
    
    # Initialize the main interface
    interface = MultiAgentInterface(config, logger)
    
    # Render the application
    interface.render()

if __name__ == "__main__":
    main()