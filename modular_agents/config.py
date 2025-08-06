# modular_agents/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
GENERATIVE_MODEL_NAME = "gemini-2.5-pro-preview-05-06"

# File Paths
DEFAULT_OUTPUT_DIR = "pipeline_output"