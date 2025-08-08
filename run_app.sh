#!/bin/bash

# Comic Script Generator Streamlit App Launcher
echo "🚀 Starting Comic Script Generator Web App..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements_streamlit.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your GEMINI_API_KEY"
    echo "Example:"
    echo "GEMINI_API_KEY=your_api_key_here"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Launch Streamlit app
echo "🌐 Launching Streamlit app..."
echo "📱 App will open in your browser automatically"
echo "🛑 Press Ctrl+C to stop the app"
echo ""

# Set environment variables to reduce noise
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --logger.level error
