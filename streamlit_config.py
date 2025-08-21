"""
Streamlit App Configuration
"""

# App settings
APP_TITLE = "Comic Script Generator"
APP_ICON = "📚"
DEFAULT_PORT = 8501

# Processing limits
MAX_FILE_SIZE_MB = 100

# AI settings
DEFAULT_TEMPERATURE = 0.7
MIN_TEMPERATURE = 0.1
MAX_TEMPERATURE = 1.0

# Supported file types
SUPPORTED_COMIC_FORMATS = ['cbr', 'cbz']
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

# UI settings
MAX_PREVIEW_IMAGES = 5
PREVIEW_COLUMNS = 3
PREVIEW_THUMBNAIL_SIZE = (300, 400)

# File paths
TEMP_DIR_PREFIX = "comic_processor_"
OUTPUT_DIR_NAME = "streamlit_output"

# Messages
MESSAGES = {
    'upload_success': "✅ File uploaded successfully!",
    'processing_start': "🚀 Starting Processing",
    'processing_extract': "📦 Extracting comic archive...",
    'processing_analyze': "🤖 Analyzing comic pages...",
    'processing_success': "✅ Comic processing completed successfully!",
    'api_key_missing': "❌ Gemini API Key not found in config",
    'api_key_found': "✅ Gemini API Key configured",
    'no_file_uploaded': "ℹ️ Please upload a comic file first.",
    'no_images_found': "No image files found in the comic archive",
    'extraction_failed': "Failed to extract comic archive",
    'processing_failed': "Failed to process comic",
    'no_script_generated': "ℹ️ Process a comic first to see the generated script."
}
