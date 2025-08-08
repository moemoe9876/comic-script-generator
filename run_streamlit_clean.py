#!/usr/bin/env python3
"""
Clean launcher for the Streamlit app that suppresses unnecessary warnings
"""
import os
import sys
import warnings

# Suppress specific Streamlit warnings when not in actual Streamlit context
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")
warnings.filterwarnings("ignore", message=".*to view a Streamlit app on a browser.*")

# Set environment variable to reduce Streamlit warnings
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

if __name__ == "__main__":
    # Import and run streamlit
    from streamlit.web import cli as stcli
    
    # Set up the arguments for streamlit run
    sys.argv = [
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
        "--logger.level=error"
    ]
    
    # Run streamlit
    sys.exit(stcli.main())
