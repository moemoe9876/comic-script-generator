import streamlit as st
import tempfile
import os
import json
from pathlib import Path
import zipfile
try:
    import rarfile  # type: ignore
except Exception:  # pragma: no cover
    rarfile = None
from PIL import Image
import io

# Import your existing modules
from modular_agents.main_coordinator import MainCoordinator
from modular_agents.word_utils import count_words
from modular_agents.config import GEMINI_API_KEY

st.set_page_config(
    page_title="Comic Script Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.section-header {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
.success-box {
    padding: 1rem;
    background-color: #f8f9fa;
    color: #212529;
    border-radius: 0.5rem;
    border-left: 4px solid #28a745;
    margin: 1rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.info-box {
    padding: 1rem;
    background-color: #f8f9fa;
    color: #495057;
    border-radius: 0.5rem;
    border-left: 4px solid #17a2b8;
    margin: 1rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.warning-box {
    padding: 1rem;
    background-color: #fff3cd;
    border-radius: 0.5rem;
    border-left: 4px solid #ffc107;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def extract_comic_archive(uploaded_file, extract_dir):
    """Extract CBR or CBZ file to a directory"""
    try:
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        # Save uploaded file temporarily
        temp_path = os.path.join(extract_dir, uploaded_file.name)
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Create extraction directory
        comic_extract_dir = os.path.join(extract_dir, f"extracted_{uploaded_file.name.split('.')[0]}")
        os.makedirs(comic_extract_dir, exist_ok=True)
        
        if file_extension == 'cbz':
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                zip_ref.extractall(comic_extract_dir)
        elif file_extension == 'cbr':
            if not rarfile:
                st.error("CBR extraction requires the 'rarfile' package and an unrar backend. Please install dependencies.")
                return None
            with rarfile.RarFile(temp_path, 'r') as rar_ref:
                rar_ref.extractall(comic_extract_dir)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
        
        # Clean up temp file
        os.remove(temp_path)
        
        return comic_extract_dir
        
    except Exception as e:
        st.error(f"Error extracting comic archive: {str(e)}")
        return None

def get_image_files(directory):
    """Get all image files from directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    
    return sorted(image_files)

def display_image_preview(image_files, max_images=None, quality_settings="High"):
    """Display preview of comic pages"""
    st.markdown("### 📖 Comic Pages Preview")
    
    # Define quality settings
    quality_options = {
        "High": {"max_width": 500, "max_height": 750},
        "Medium": {"max_width": 400, "max_height": 600}, 
        "Low": {"max_width": 300, "max_height": 450}
    }
    
    quality_config = quality_options.get(quality_settings, quality_options["High"])
    
    total_pages = len(image_files)
    
    if max_images is None:
        # Show all pages
        display_files = image_files
        st.info(f"Showing all {total_pages} pages (Quality: {quality_settings})")
    else:
        # Show limited pages
        if total_pages > max_images:
            st.info(f"Showing first {max_images} pages out of {total_pages} total pages (Quality: {quality_settings})")
            display_files = image_files[:max_images]
        else:
            display_files = image_files
            st.info(f"Showing all {total_pages} pages (Quality: {quality_settings})")
    
    # Create a grid layout - 3 columns per row
    cols_per_row = 3
    
    for i in range(0, len(display_files), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(display_files):
                img_path = display_files[idx]
                with cols[j]:
                    try:
                        img = Image.open(img_path)
                        
                        # Get original dimensions
                        original_width, original_height = img.size
                        
                        # Use quality settings for dimensions
                        max_width = quality_config["max_width"]
                        max_height = quality_config["max_height"]
                        
                        # Calculate scaling factor to maintain aspect ratio
                        width_ratio = max_width / original_width
                        height_ratio = max_height / original_height
                        scaling_factor = min(width_ratio, height_ratio)
                        
                        # Calculate new dimensions
                        new_width = int(original_width * scaling_factor)
                        new_height = int(original_height * scaling_factor)
                        
                        # Use high-quality resampling
                        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Display with high quality
                        st.image(
                            img_resized, 
                            caption=f"Page {idx + 1} ({original_width}×{original_height})", 
                            use_container_width=True,
                            output_format="PNG"  # Use PNG for better quality
                        )
                    except Exception as e:
                        st.error(f"Error loading image {os.path.basename(img_path)}: {str(e)}")

def main():
    st.markdown('<h1 class="main-header">📚 Comic Script Generator</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key Input
        st.markdown("### 🔑 Gemini API Key")
        user_api_key = st.text_input(
            "Enter your Gemini API Key:",
            type="password",
            help="Your API key is required to process comics."
        )

        if not user_api_key:
            st.warning("Please enter your Gemini API Key to proceed.")
            st.stop()
        
        st.success("✅ Gemini API Key entered")
        
        st.markdown("---")
        
        # Processing options
        st.markdown("### 🔧 Processing Options")
        
        generation_temperature = st.slider(
            "Creativity Level", 
            min_value=0.1, 
            max_value=1.0, 
            value=0.5,  # Default set to 0.5 to match ScriptGenerator
            step=0.1,
            help="Higher values = more creative but less consistent. 0.5 is optimal for script generation."
        )
        
    # NOTE: Removed 'Max Pages to Process' limit — all pages will be processed
        
        # Model selection
        model_name = st.selectbox(
            "Gemini Model for Script Generation",
            options=[
                "gemini-2.0-flash-lite",
                "gemini-2.0-flash", 
                "gemini-2.5-flash-lite",
                "gemini-2.5-flash",
                "gemini-2.5-pro"
            ],
            index=4,  # Default to gemini-2.5-pro
            help="Choose the Gemini model for script generation only. Other processing uses gemini-2.0-flash."
        )
        
        # Model usage explanation
        with st.expander("ℹ️ Model Usage Information"):
            st.markdown("""
            **Script Generator:** Uses your selected model above for creative script writing.
            
            **Fixed Components (Always use gemini-2.0-flash):**
            - 📖 **Page Analyzer:** Analyzes comic pages and extracts story elements
            - 📝 **Story Summarizer:** Creates comprehensive story summaries
            
            This ensures consistent analysis quality while allowing creative flexibility for script generation.
            """)
        
        st.markdown("---")
        
        # Image display options
        st.markdown("### 🖼️ Preview Options")
        
        show_image_preview = st.checkbox("Show Image Preview", value=True, 
                                       help="Uncheck to skip image preview for faster processing")
        
        if show_image_preview:
            show_all_pages = st.checkbox("Show All Pages", value=True)
            
            if not show_all_pages:
                max_preview_pages = st.number_input(
                    "Max Pages to Preview", 
                    min_value=1, 
                    max_value=50, 
                    value=10,
                    help="Limit image preview for performance"
                )
            else:
                max_preview_pages = None
        else:
            show_all_pages = False
            max_preview_pages = 0
        
        # Image quality options
        image_quality = st.selectbox(
            "Image Quality",
            options=["High", "Medium", "Low"],
            index=0,
            help="Higher quality = better images but slower loading"
        )
        
        # Set quality parameters based on selection
        if image_quality == "High":
            quality_settings = {"max_width": 500, "max_height": 750, "format": "PNG"}
        elif image_quality == "Medium":
            quality_settings = {"max_width": 400, "max_height": 600, "format": "PNG"}
        else:  # Low
            quality_settings = {"max_width": 300, "max_height": 450, "format": "JPEG"}
        
        st.markdown("---")
        
        # Optional transcript section
        st.markdown("### 📝 Optional YouTube Transcript")
        use_transcript = st.checkbox("Include YouTube Transcript")
        
        transcript_text = ""
        if use_transcript:
            transcript_text = st.text_area(
                label="Paste YouTube Transcript Here:",
                height=150,
                placeholder="Paste your YouTube video transcript here...",
                help="This will be used as primary context for script generation"
            )

        # Target word count range
        target_word_count_min = st.number_input(
            "Target Min Word Count", min_value=50, max_value=1000, value=200, step=10,
            help="Minimum target word count for generated script"
        )
        target_word_count_max = st.number_input(
            "Target Max Word Count", min_value=target_word_count_min, max_value=2000, value=max(250, target_word_count_min), step=10,
            help="Maximum target word count for generated script"
        )
        
        # Validation for word count range
        if target_word_count_max < target_word_count_min:
            st.warning("⚠️ Maximum word count cannot be less than minimum word count!")
            target_word_count_max = target_word_count_min

        st.session_state['target_word_count_min'] = target_word_count_min
        st.session_state['target_word_count_max'] = target_word_count_max
    
    # Main content - Single page with step-by-step flow
    st.markdown('<h2 class="section-header">🚀 Generate Your Comic Script</h2>', unsafe_allow_html=True)
    
    # Step 1: Upload Comic
    st.markdown("### Step 1: Upload Your Comic File")
    
    uploaded_file = st.file_uploader(
        "Choose a comic file (CBR or CBZ)",
        type=['cbr', 'cbz'],
        help="Upload your comic book archive file"
    )
    
    if uploaded_file is not None:
        st.markdown('<div class="success-box">✅ File uploaded successfully!</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**File Size:** {uploaded_file.size / 1024 / 1024:.2f} MB")
        
        with col2:
            file_type = uploaded_file.name.split('.')[-1].upper()
            st.write(f"**File Type:** {file_type}")
        
        # Store in session state
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['user_api_key'] = user_api_key
        st.session_state['generation_temperature'] = generation_temperature
    # No max_pages stored anymore — process all extracted pages
        st.session_state['transcript_text'] = transcript_text if use_transcript else ""
        st.session_state['max_preview_pages'] = max_preview_pages
        st.session_state['quality_settings'] = image_quality
        st.session_state['show_image_preview'] = show_image_preview
        st.session_state['model_name'] = model_name
        
        st.markdown("---")
        
        # Step 2: Preview and Process
        st.markdown("### Step 2: Preview & Start Processing")
        
        # Show processing button prominently
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_button = st.button(
                "🚀 Start Processing Comic", 
                type="primary", 
                use_container_width=True,
                help="Extract pages, analyze content, and generate script"
            )
        
        st.markdown("---")
        
        # Processing logic
        if process_button or st.session_state.get('processing_complete', False):
            if process_button:
                st.session_state['processing_started'] = True
                st.session_state['processing_complete'] = False
            
            if st.session_state.get('processing_started', False) and not st.session_state.get('processing_complete', False):
                # Processing Section
                st.markdown("### � Processing Your Comic")
                
                with st.spinner("Processing your comic... This may take a few minutes."):
                    try:
                        # Create temporary directory
                        import tempfile
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Extract comic
                            st.info("📦 Extracting comic archive...")
                            extract_dir = extract_comic_archive(uploaded_file, temp_dir)
                            
                            if extract_dir is None:
                                st.error("Failed to extract comic archive")
                                st.stop()
                            
                            # Get image files
                            image_files = get_image_files(extract_dir)
                            
                            if not image_files:
                                st.error("No image files found in the comic archive")
                                st.stop()
                            
                            st.success(f"Found {len(image_files)} pages in the comic")
                            
                            # Display preview of all pages (if enabled)
                            if st.session_state.get('show_image_preview', True):
                                max_preview = st.session_state.get('max_preview_pages', None)
                                quality_setting = st.session_state.get('quality_settings', "High")
                                display_image_preview(image_files, max_preview, quality_setting)
                            else:
                                st.info("📖 Image preview disabled - skipping to processing...")
                            
                            # No page limit: process all extracted pages
                            
                            # Process with MainCoordinator
                            st.info("🤖 Analyzing comic pages...")
                            
                            # Create output directory
                            output_dir = os.path.join(temp_dir, "streamlit_output")
                            os.makedirs(output_dir, exist_ok=True)
                            
                            # Get processing parameters
                            selected_model = st.session_state.get('model_name')
                            temperature = st.session_state.get('generation_temperature')
                            api_key = st.session_state.get('user_api_key')
                            
                            # Validate model selection
                            valid_models = [
                                "gemini-2.0-flash-lite",
                                "gemini-2.0-flash", 
                                "gemini-2.5-flash-lite",
                                "gemini-2.5-flash",
                                "gemini-2.5-pro"
                            ]
                            
                            # Handle edge cases for model selection
                            if not selected_model or selected_model.strip() == "":
                                st.warning("⚠️ No model selected. Using default model for script generation.")
                                selected_model = None  # Will use default in ScriptGenerator
                            elif selected_model not in valid_models:
                                st.error(f"❌ Invalid model selected: {selected_model}. Using default model.")
                                selected_model = None  # Will use default in ScriptGenerator
                            
                            # Validate temperature
                            if temperature is None or not isinstance(temperature, (int, float)):
                                st.warning("⚠️ Invalid temperature setting. Using default value (0.5).")
                                temperature = 0.5
                            elif not (0.1 <= temperature <= 1.0):
                                st.warning(f"⚠️ Temperature {temperature} out of range. Clamping to valid range.")
                                temperature = max(0.1, min(1.0, temperature))
                            
                            # Log processing parameters to terminal
                            print(f"\n🚀 PROCESSING STARTED:")
                            print(f"📊 Selected Model for Script Generation: {selected_model or 'default (gemini-2.5-pro)'}")
                            print(f"🔒 Fixed Models: gemini-2.0-flash (PageAnalyzer, StorySummarizer)")
                            print(f"🎯 Word Target: {target_word_count_min} - {target_word_count_max} words")
                            print(f"🌡️  Temperature: {temperature}")
                            
                            try:
                                coordinator = MainCoordinator(
                                    model_name=selected_model,  # Only affects ScriptGenerator
                                    temperature=temperature,
                                    api_key=api_key
                                )
                            except Exception as e:
                                st.error(f"❌ Failed to initialize processing coordinator: {str(e)}")
                                st.stop()
                            
                            # Log actual models being used for API calls
                            print(f"🔧 Model Configuration: {coordinator.get_actual_model_name()}")
                            
                            # Process the comic with enhanced error handling
                            try:
                                result = coordinator.process_comic(
                                    extract_dir, 
                                    output_dir, 
                                    st.session_state.get('transcript_text', ''),
                                    target_word_count_min,
                                    target_word_count_max
                                )
                            except Exception as processing_error:
                                st.error(f"❌ Processing failed with exception: {str(processing_error)}")
                                st.error("This could be due to API rate limits, network issues, or invalid API keys.")
                                st.info("💡 Please check your Gemini API key and try again.")
                                st.exception(processing_error)
                                return
                            
                            if result and result.get('success'):
                                # Store results in session state
                                st.session_state['generated_script'] = result['script_data']
                                
                                if 'story_summary' in result:
                                    st.session_state['story_summary'] = result['story_summary']

                                if 'selected_pages' in result:
                                    st.session_state['selected_pages'] = result['selected_pages']
                                
                                # Try to read the report file if it exists with error handling
                                try:
                                    report_file = result['output_files'].get('report')
                                    if report_file and os.path.exists(report_file):
                                        with open(report_file, 'r', encoding='utf-8') as f:
                                            st.session_state['generated_report'] = f.read()
                                except Exception as report_error:
                                    st.warning(f"⚠️ Could not load report file: {str(report_error)}")
                                
                                st.session_state['processing_complete'] = True
                                st.success("✅ Comic processing completed successfully!")
                                st.balloons()
                                st.rerun()  # Refresh to show results
                            else:
                                error_msg = result.get('error', 'Unknown error') if result else 'Processing failed'
                                st.error(f"Failed to process comic: {error_msg}")
                    
                    except Exception as e:
                        st.error(f"Error processing comic: {str(e)}")
                        st.exception(e)
            
            # Results Section
            if st.session_state.get('processing_complete', False) and 'generated_script' in st.session_state:
                st.markdown("---")
                st.markdown("### 📜 Your Generated Script")
                
                script_data = st.session_state['generated_script']
                
                # Display selected pages if available
                if 'selected_pages' in st.session_state:
                    st.markdown("#### 🖼️ Selected Pages for Video (page number + script text chunk)")
                    selected_pages = st.session_state['selected_pages']

                    if selected_pages:
                        for pair in selected_pages:
                            page_num = pair.get('page_number')
                            text_chunk = pair.get('text')

                            # Show the mapping with a nice layout
                            st.markdown(f"**Page {page_num}**")
                            st.write(text_chunk)
                            st.markdown("---")
                    else:
                        st.warning("No page-text pairs were selected.")

                # Display script
                if 'script' in script_data:
                    st.markdown("#### ✍️ YouTube Script")
                    
                    # Use a clean container for the script
                    with st.container():
                        st.markdown("""
                        <div style="
                            background-color: #ffffff;
                            padding: 1.5rem;
                            border-radius: 0.5rem;
                            border: 1px solid #e0e0e0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            color: #333333;
                            line-height: 1.6;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        ">
                        """ + script_data["script"].replace('\n', '<br>') + """
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Word count (robust)
                    word_count = count_words(script_data['script'])
                    st.metric("Word Count", word_count)
                    
                    # Download button for script
                    st.download_button(
                        label="📥 Download Script",
                        data=script_data['script'],
                        file_name=f"comic_script_{uploaded_file.name.split('.')[0]}.txt",
                        mime="text/plain"
                    )
                
                # Display title suggestions
                if 'title_suggestions' in script_data:
                    st.markdown("#### 🎬 Title Suggestions")
                    
                    # Clean container for title suggestions
                    with st.container():
                        st.markdown("""
                        <div style="
                            background-color: #f8f9fa;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            border-left: 4px solid #007bff;
                            color: #495057;
                            line-height: 1.5;
                        ">
                        """ + script_data['title_suggestions'].replace('\n', '<br>') + """
                        </div>
                        """, unsafe_allow_html=True)
                
                # Additional options
                st.markdown("---")
                st.markdown("#### 📊 Additional Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Display full report if available
                    if 'generated_report' in st.session_state:
                        with st.expander("📊 Full Analysis Report"):
                            st.markdown(st.session_state['generated_report'])
                            
                            # Download button for report
                            st.write(f"Target: {st.session_state['target_word_count_min']} - {st.session_state['target_word_count_max']} words")
                            st.download_button(
                                label="📥 Download Full Report",
                                data=st.session_state['generated_report'],
                                file_name=f"comic_report_{uploaded_file.name.split('.')[0]}.md",
                                mime="text/markdown"
                            )
                
                with col2:
                    # JSON download
                    with st.expander("🔧 Raw JSON Data"):
                        st.json(script_data)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json.dumps(script_data, indent=2),
                            file_name=f"comic_data_{uploaded_file.name.split('.')[0]}.json",
                            mime="application/json"
                        )
                
                # Reset button
                st.markdown("---")
                if st.button("🔄 Process Another Comic", type="secondary"):
                    # Clear session state for new processing
                    for key in ['processing_started', 'processing_complete', 'generated_script', 'generated_report', 'story_summary', 'selected_pages']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
    
    else:
        # No file uploaded yet
        st.markdown("""
        <div style="
            background-color: #e3f2fd;
            color: #1565c0;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #2196f3;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        ">
            <span style="font-size: 1.2em; margin-right: 0.5rem;">📁</span>
            <span>Upload a CBR or CBZ comic file above to get started!</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
