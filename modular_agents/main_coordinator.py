# modular_agents/main_coordinator.py
import os
import sys
import json
from pathlib import Path

from . import config
from .image_extractor import ImageExtractor
from .page_analyzer import PageAnalyzer
from .story_summarizer import StorySummarizer
from .script_generator import ScriptGenerator
from .word_utils import count_words

class MainCoordinator:
    """
    Coordinates the entire comic-to-script pipeline.
    """
    def __init__(self, model_name=None, temperature: float | None = None):
        self.model_name = model_name  # Store the provided model name
        self.image_extractor = ImageExtractor()
        self.page_analyzer = PageAnalyzer(model_name=model_name)
        self.story_summarizer = StorySummarizer(model_name=model_name)
        self.script_generator = ScriptGenerator(model_name=model_name, temperature=temperature)
    
    def get_actual_model_name(self) -> str:
        """
        Returns the actual model name being used for API calls.
        If no model_name was provided, returns the default from config.
        """
        return self.model_name if self.model_name else config.GENERATIVE_MODEL_NAME
    
    def process_comic(self, comic_path: str, output_dir: str, youtube_transcript: str = "", target_min_words: int = 300, target_max_words: int = 350) -> dict:
        """
        Process a comic and generate a script with optional YouTube transcript.
        
        Args:
            comic_path: Path to the comic file or extracted directory
            output_dir: Directory to save outputs
            youtube_transcript: Optional YouTube transcript for enhanced context
            
        Returns:
            dict: Processing results including script data
        """
        try:
            # Log the actual processing details
            print(f"📋 PROCESSING DETAILS:")
            print(f"   • Model for API calls: {self.get_actual_model_name()}")
            print(f"   • Word target range: {target_min_words} - {target_max_words}")
            print(f"   • YouTube transcript: {'Yes' if youtube_transcript.strip() else 'No'}")
            print(f"   • Comic path: {comic_path}")
            
            base_name = Path(comic_path).stem if os.path.isfile(comic_path) else Path(comic_path).name
            
            comic_output_dir = Path(output_dir)
            os.makedirs(comic_output_dir, exist_ok=True)
            
            # Define output files
            script_file = comic_output_dir / "final_script.json"
            analyses_file = comic_output_dir / "page_analyses.json"
            summary_file = comic_output_dir / "summary.txt"
            final_report_file = comic_output_dir / "final_report.md"
            
            # Extract images
            print("🚀 Starting: Extracting images from comic for analysis...")
            if os.path.isfile(comic_path):
                image_paths = self.image_extractor.extract_images_to_temp(comic_path)
            else:
                # Assume it's already an extracted directory
                image_paths = self._get_image_files_from_directory(comic_path)
            
            if not image_paths:
                raise Exception("Image extraction yielded no paths.")
            print(f"✅ Finished: Extracted {len(image_paths)} images for analysis")
            
            # Analyze pages
            print(f"🚀 Starting: Analyzing {len(image_paths)} pages...")
            all_analyses = self.page_analyzer.analyze_pages_in_parallel(image_paths)
            
            # Filter out non-story pages
            print("🔍 Filtering story pages from non-story content...")
            story_analyses = self.page_analyzer.filter_story_pages(all_analyses)
            
            # Save all analyses (including filtered ones for reference)
            with open(analyses_file, 'w', encoding='utf-8') as f:
                json.dump(all_analyses, f, indent=2, ensure_ascii=False)
            print(f"✅ Finished: Analyzed pages, saved to {analyses_file}")
            
            # Save story-only analyses
            story_analyses_file = comic_output_dir / "story_analyses.json"
            with open(story_analyses_file, 'w', encoding='utf-8') as f:
                json.dump(story_analyses, f, indent=2, ensure_ascii=False)
            print(f"📖 Filtered story pages saved to {story_analyses_file}")
            
            # Generate story summary using only story pages
            print("🚀 Starting: Generating story summary...")
            story_summary = self.story_summarizer.summarize_story(story_analyses)
            
            # Save summary
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(story_summary)
            print("✅ Finished: Generating story summary.")
            
            # Generate script with optional transcript
            print("🚀 Starting: Generating final script...")
            script_data = self.script_generator.generate_script(story_summary, youtube_transcript, target_min_words, target_max_words)
            
            # Save script
            with open(script_file, 'w', encoding='utf-8') as f:
                json.dump(script_data, f, indent=2, ensure_ascii=False)
            print("✅ Finished: Generating final script.")
            
            # Generate comprehensive report
            self._generate_final_report(
                final_report_file, base_name, script_data, 
                story_summary, story_analyses, youtube_transcript,
                target_min_words, target_max_words, len(all_analyses), len(story_analyses)
            )
            
            return {
                'success': True,
                'script_data': script_data,
                'story_summary': story_summary,
                'analyses': all_analyses,
                'story_analyses': story_analyses,
                'output_files': {
                    'script': str(script_file),
                    'report': str(final_report_file),
                    'summary': str(summary_file),
                    'analyses': str(analyses_file),
                    'story_analyses': str(story_analyses_file)
                }
            }
            
        except Exception as e:
            print(f"❌ Error in processing pipeline: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            # Cleanup temporary files
            if hasattr(self.image_extractor, 'cleanup'):
                self.image_extractor.cleanup()
    
    def _get_image_files_from_directory(self, directory: str) -> list:
        """Get image files from a directory"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        image_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(root, file))
        
        return sorted(image_files)
    
    def _generate_final_report(self, report_file, base_name, script_data, 
                              story_summary, story_analyses, youtube_transcript,
                              target_min_words=300, target_max_words=350, 
                              total_pages=None, story_pages=None):
        """Generate comprehensive final report"""
        script_word_count = count_words(script_data.get('script', ''))
        summary_word_count = count_words(story_summary)

        print(f"📊 Script word count: {script_word_count} words")

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Pipeline Report for {base_name}\n\n")

            if youtube_transcript:
                f.write("## 📝 YouTube Transcript Used\n\n")
                f.write("✅ YouTube transcript was provided and used for enhanced context.\n\n")

            # Add page filtering information
            if total_pages and story_pages:
                filtered_pages = total_pages - story_pages
                f.write("## 📄 Page Analysis Summary\n\n")
                f.write(f"- **Total pages analyzed:** {total_pages}\n")
                f.write(f"- **Story pages identified:** {story_pages}\n")
                f.write(f"- **Non-story pages filtered:** {filtered_pages}\n")
                f.write(f"- **Story page percentage:** {(story_pages/total_pages)*100:.1f}%\n\n")

            f.write("## 📜 Final Script\n\n")
            f.write(f"**Title Suggestions:**\n{script_data.get('title_suggestions', 'N/A')}\n\n")
            f.write(f"**Script:**\n{script_data.get('script', 'N/A')}\n\n")

            f.write("## 📖 Story Summary\n\n")
            f.write(f"{story_summary}\n\n")

            f.write("## 📊 Word Count\n\n")
            f.write(f"- **Script:** {script_word_count} words\n")
            f.write(f"- **Summary:** {summary_word_count} words\n")
            f.write(f"- **Target Range:** {target_min_words}-{target_max_words} words for script\n")
            if target_min_words <= script_word_count <= target_max_words:
                f.write(f"- **Status:** ✅ Within target range\n\n")
            else:
                f.write(f"- **Status:** ⚠️ Outside target range\n\n")

            f.write("## 📄 Story Page Analysis (Filtered)\n\n")
            f.write("*Only story pages are included below. Non-story pages (credits, ads, etc.) have been filtered out.*\n\n")
            f.write("```json\n")
            f.write(json.dumps(story_analyses, indent=2))
            f.write("\n```\n\n")

        print(f"✅ Finished: Final report saved to {report_file}")

def main(comic_path: str, output_dir: str):
    """
    Legacy function for backwards compatibility with existing CLI usage
    """
    if not os.path.exists(comic_path):
        print(f"Error: Comic file not found: {comic_path}", file=sys.stderr)
        sys.exit(1)
    
    coordinator = MainCoordinator()
    result = coordinator.process_comic(comic_path, output_dir)
    
    if result['success']:
        print("\n🎉 Pipeline completed successfully!")
    else:
        print(f"\n❌ Pipeline failed: {result['error']}")
        sys.exit(1)

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