# modular_agents/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
# Default model for backward compatibility (not used by modular agents anymore)
GENERATIVE_MODEL_NAME = "gemini-2.5-pro-preview-05-06"

# Fixed model for image_extractor, page_analyzer, and story_summarizer
# This model is hardcoded and cannot be overridden by user selection
FIXED_MODEL_NAME = "gemini-2.0-flash"

# Default model for script_generator (can be overridden by user selection)
DEFAULT_SCRIPT_MODEL = "gemini-2.5-pro"

# File Paths
DEFAULT_OUTPUT_DIR = "pipeline_output"