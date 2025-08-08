# Comic Script Generator - Web App

A Streamlit-powered web interface for generating YouTube scripts from comic book files (CBR/CBZ).

## 🌟 Features

- **📁 File Upload**: Drag & drop CBR/CBZ comic files
- **👀 Preview**: Visual preview of comic pages before processing
- **🤖 AI Processing**: Automated page analysis and script generation
- **📝 Transcript Integration**: Optional YouTube transcript input for enhanced context
- **📊 Results Dashboard**: View generated scripts, titles, and analysis reports
- **💾 Download Options**: Export scripts, reports, and raw data

## 🚀 Quick Start

### Option 1: Using the Launch Script (Recommended)
```bash
./run_app.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_streamlit.txt

# Launch app
streamlit run streamlit_app.py
```

## 📋 Prerequisites

- Python 3.8+
- Gemini API key (set in `.env` file)
- WinRAR/unrar for CBR files (optional, for better CBR support)

## 🎛️ App Interface

### 1. Upload Tab 📁
- Upload your CBR/CBZ comic files
- Configure processing options:
  - Creativity level (temperature)
  - Maximum pages to process
  - Optional YouTube transcript input

### 2. Processing Tab 🔄
- Real-time processing status
- Comic page preview
- Progress tracking and error handling

### 3. Results Tab 📜
- Generated YouTube script
- Title suggestions
- Word count metrics
- Full analysis report
- Download options (TXT, MD, JSON)

## ⚙️ Configuration Options

- **Creativity Level**: Controls AI creativity (0.1 = conservative, 1.0 = very creative)
- **Max Pages**: Limits processing for large comics (performance optimization)
- **YouTube Transcript**: Paste transcripts for enhanced script context

## 📥 Output Formats

- **Script**: Clean text format ready for YouTube
- **Report**: Detailed Markdown analysis
- **JSON**: Raw data with all processing results

## 🔧 Troubleshooting

### Common Issues:

1. **CBR files not extracting**: Install WinRAR or unrar utility
2. **API errors**: Check your Gemini API key in `.env`
3. **Large files timing out**: Reduce max pages or file size
4. **Memory issues**: Process smaller comics or restart the app

### Error Messages:
- "API Key not found": Create `.env` file with `GEMINI_API_KEY=your_key`
- "No image files found": Check if comic file is corrupted
- "Processing failed": Check logs in terminal for detailed error info

## 🎯 Tips for Best Results

1. **Optimal file size**: 10-50 pages work best
2. **Quality matters**: Higher resolution pages = better analysis
3. **Use transcripts**: YouTube transcripts significantly improve script quality
4. **Experiment with creativity**: Try different temperature settings

## 🔄 Workflow

1. Upload CBR/CBZ file
2. (Optional) Paste YouTube transcript
3. Adjust processing settings
4. Click "Start Processing"
5. Preview comic pages
6. View generated script and analysis
7. Download results

The app will automatically handle file extraction, image processing, AI analysis, and script generation - all through an intuitive web interface!
