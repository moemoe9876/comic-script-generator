# modular_agents/main_coordinator.py
import os
import sys
import json
from pathlib import Path

import config
from image_extractor import ImageExtractor
from page_analyzer import PageAnalyzer
from story_summarizer import StorySummarizer
from script_generator import ScriptGenerator

def main(comic_path: str, output_dir: str):
    """
    Coordinates the entire comic-to-script pipeline in a single process.
    
    Args:
        comic_path: Path to the comic file (.cbr, .cbz, etc.)
        output_dir: Directory to save all outputs
    """
    # --- Setup ---
    if not os.path.exists(comic_path):
        print(f"Error: Comic file not found: {comic_path}", file=sys.stderr)
        sys.exit(1)

    base_name = Path(comic_path).stem
    
    # Use the provided output directory directly
    comic_output_dir = Path(output_dir)
    os.makedirs(comic_output_dir, exist_ok=True)
    
    # Define file paths for only essential output files
    final_report_file = comic_output_dir / "final_report.md"

    # --- Instantiate all agents ---
    image_extractor = ImageExtractor()
    page_analyzer = PageAnalyzer()
    story_summarizer = StorySummarizer()
    script_generator = ScriptGenerator()
    
    try:
        # --- Agent 1: Image Extractor ---
        print("🚀 Starting: Extracting images from comic for analysis...")
        # Extract to temporary directory for analysis only
        image_paths = image_extractor.extract_images_to_temp(comic_path)
        if not image_paths:
             raise Exception("Image extraction yielded no paths.")
        print(f"✅ Finished: Extracted {len(image_paths)} images for analysis")

        # --- Agent 2: Page Analyzer ---
        print(f"🚀 Starting: Analyzing {len(image_paths)} pages in parallel...")
        # Calculate optimal batch size based on CPU cores and available memory
        cpu_count = os.cpu_count() or 4  # Default to 4 if can't determine
        batch_size = max(1, len(image_paths) // (cpu_count * 2))
        
        # Initialize page analyzer with optimized batch size
        page_analyzer = PageAnalyzer(batch_size=batch_size)
        
        # Use parallel processing with automatic worker count
        all_analyses = page_analyzer.analyze_pages_in_parallel(image_paths)
        
        if any('error' in analysis for analysis in all_analyses):
            print("⚠️  Some pages had analysis errors. Check the final report for details.")
        
        print(f"✅ Finished: Page analysis complete")

        # --- Agent 3: Story Summarizer ---
        print("🚀 Starting: Generating story summary...")
        story_summary = story_summarizer.summarize_story(all_analyses)
        print("✅ Finished: Generating story summary.")

        # --- Agent 4: Script Generator ---
        print(f"🚀 Starting: Generating final script...")
        script_data = script_generator.generate_script(story_summary)
        
        print("✅ Finished: Generating final script.")

        # --- Word Count ---
        script_word_count = len(script_data.get('script', '').split())
        summary_word_count = len(story_summary.split())

        # --- Validation ---
        print(f"📊 Script word count: {script_word_count} words")
        print(f"📊 Summary word count: {summary_word_count} words")
        
        if script_word_count < 300:
            print(f"⚠️  Warning: Script is only {script_word_count} words (target: 300-350)")
        elif script_word_count > 350:
            print(f"⚠️  Warning: Script is {script_word_count} words (target: 300-350)")
        else:
            print(f"✅ Script word count is within target range (300-350 words)")

        # --- Final Report Generation ---
        print("🚀 Starting: Generating comprehensive final report...")
        with open(final_report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Pipeline Report for {base_name}\n\n")
            
            f.write("## � Final Script\n\n")
            f.write(f"**Title Suggestions:**\n{script_data.get('title_suggestions', 'N/A')}\n\n")
            f.write(f"**Script:**\n{script_data.get('script', 'N/A')}\n\n")
            
            f.write("## � Story Summary\n\n")
            f.write(f"{story_summary}\n\n")
            
            f.write("## 📊 Word Count\n\n")
            f.write(f"- **Script:** {script_word_count} words\n")
            f.write(f"- **Summary:** {summary_word_count} words\n")
            f.write(f"- **Target Range:** 300-350 words for script\n")
            if 200 <= script_word_count <= 350:
                f.write(f"- **Status:** ✅ Within target range\n\n")
            else:
                f.write(f"- **Status:** ⚠️ Outside target range\n\n")
            
            f.write("## 📄 Page-by-Page Analysis\n\n")
            f.write("```json\n")
            f.write(json.dumps(all_analyses, indent=2))
            f.write("\n```\n\n")
        print(f"✅ Finished: Final report saved to {final_report_file}")
        print("\n🎉 Pipeline completed successfully!")
        
    except Exception as e:
        print(f"\n--- FATAL ERROR ---", file=sys.stderr)
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # --- Cleanup ---
        print("🧹 Cleaning up temporary files...")
        image_extractor.cleanup()
        print("✅ Cleanup complete.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <path_to_comic_file> <output_directory>")
        sys.exit(1)

    comic_file_path = sys.argv[1]
    output_dir_path = sys.argv[2]

    if not config.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    main(comic_file_path, output_dir_path)