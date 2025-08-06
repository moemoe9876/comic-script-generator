# Comic Book Script Generator

This project is a modular system for converting comic books into engaging YouTube scripts. It consists of several specialized agents that work together to analyze comic book pages, understand the story, and generate compelling scripts.

## Features

- Image extraction from comic book archives (.cbr, .cbz)
- Page-by-page analysis using Google's Gemini AI
- Story summarization with emotional depth and context
- YouTube script generation optimized for engagement

## Components

1. **ImageExtractor**: Extracts images from comic book archives
2. **PageAnalyzer**: Analyzes individual comic pages using Gemini AI
3. **StorySummarizer**: Creates comprehensive story summaries
4. **ScriptGenerator**: Converts summaries into engaging YouTube scripts

## Setup

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

```bash
python main_coordinator.py path/to/comic.cbr output_directory
```

## Project Structure

```plaintext
modular_agents/
├── config.py              # Configuration and environment variables
├── image_extractor.py     # Comic book archive extraction
├── main_coordinator.py    # Main pipeline coordinator
├── page_analyzer.py       # Page analysis using Gemini AI
├── script_generator.py    # Script generation from summaries
└── story_summarizer.py    # Story summarization
```

## Requirements

- Python 3.8+
- Google Gemini AI API key
- `unar` command line tool for CBR extraction
