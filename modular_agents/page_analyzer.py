# modular_agents/page_analyzer.py
import os
import sys
import json
from typing import Dict, Any, List
import concurrent.futures
from tqdm import tqdm

import google.generativeai as genai

from . import config

class PageAnalyzer:
    """
    Analyzes comic book pages using the Gemini API, with support for parallel processing.
    """
    def __init__(self, batch_size: int = None, model_name: str = None, api_key: str = None):
        """
        Initialize the PageAnalyzer with optional batch size for parallel processing.
        
        Args:
            batch_size: Optional batch size for processing multiple pages. If None,
                       will be calculated based on available CPU cores.
            model_name: This parameter is ignored. PageAnalyzer always uses gemini-2.0-flash
                       as per system requirements to ensure consistent analysis quality.
            api_key: The Gemini API key. If not provided, it will be read from the 
                     environment variable.
        """
        genai.configure(api_key=api_key or config.GEMINI_API_KEY)
        # Configure model with low temperature to reduce hallucinations
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,  # Low temperature for more focused, less creative output
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
        )
        # Always use the fixed model for page analysis - hardcoded as per requirements
        self.model = genai.GenerativeModel(
            config.FIXED_MODEL_NAME,  # Always "gemini-2.0-flash"
            generation_config=generation_config
        )
        self.batch_size = batch_size

    def analyze_page(self, image_path: str, page_number: int, total_pages: int) -> Dict[str, Any]:
        """
        Analyzes a single comic book page and returns a structured JSON object.
        """
        if not os.path.exists(image_path):
            return {
                "page": page_number,
                "error": f"Image file not found: {image_path}",
                "raw_response": ""
            }

        try:
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()

            image_part = {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }

            prompt = f"""Analyze comic book page {page_number} of {total_pages}.
            First determine if this page is part of the actual comic story or a non-story page, then extract key information.

            **JSON Schema:**
            {{
              "page": {page_number},
              "is_story_page": true/false,
              "page_type": "story|credits|advertisement|title|table_of_contents|testimonial|editorial|copyright|blank|other",
              "setting": "A brief description of the location and environment (only for story pages).",
              "characters_present": ["Character A", "Character B"],
              "key_actions_or_events": [
                "A summary of the most important action on the page.",
                "Another key event."
              ],
              "key_dialogue_summary": "A summary of the most important dialogue, capturing the core intent."
            }}

            **Page Classification Rules:**
            - **Story Pages:** Contain comic panels with narrative content, characters in action, dialogue, or story progression
            - **Non-Story Pages:** Credits, advertisements, testimonials, author notes, copyright pages, table of contents, blank pages, editorial content, publisher information, character bios outside the main story

            **Story Content Rules:**
            - Only extract setting, characters, actions, and dialogue for pages marked as "is_story_page": true
            - For non-story pages, leave story fields empty or use empty arrays
            - Be conservative: if unsure whether a page is story content, mark it as non-story

            **Response Rules:**
            - Provide only the JSON object in your response
            - If a field is not applicable, use an empty string or empty list
            - Always include the is_story_page and page_type fields

            Here is the image of the page:"""

            response = self.model.generate_content([prompt, image_part])
            
            cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            
            try:
                return json.loads(cleaned_response_text)
            except json.JSONDecodeError:
                start_index = cleaned_response_text.find('{')
                end_index = cleaned_response_text.rfind('}') + 1
                if start_index != -1 and end_index != -1:
                    json_text = cleaned_response_text[start_index:end_index]
                    return json.loads(json_text)
                else:
                    raise json.JSONDecodeError("No JSON object found in response", cleaned_response_text, 0)
        
        except Exception as e:
            return {
                "page": page_number,
                "error": f"An unexpected error occurred: {e}",
                "raw_response": getattr(e, 'text', str(e))
            }

    def analyze_pages_in_parallel(self, image_paths: List[str], max_workers: int = None) -> List[Dict[str, Any]]:
        """
        Analyzes multiple comic book pages in parallel using a process pool for CPU-intensive tasks.
        If max_workers is None, it will use the number of CPU cores.
        """
        total_pages = len(image_paths)
        all_analyses = [None] * total_pages
        
        # Use CPU count if max_workers not specified
        if max_workers is None:
            max_workers = os.cpu_count()

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Create batches for better memory management
            batch_size = max(1, total_pages // (max_workers * 2))
            future_to_page = {
                executor.submit(self.analyze_page, image_path, i + 1, total_pages): i
                for i, image_path in enumerate(image_paths)
            }
            
            with tqdm(total=total_pages, desc="Analyzing Pages") as pbar:
                for future in concurrent.futures.as_completed(future_to_page):
                    page_index = future_to_page[future]
                    try:
                        analysis = future.result()
                        all_analyses[page_index] = analysis
                    except Exception as exc:
                        all_analyses[page_index] = {
                            "page": page_index + 1,
                            "error": f"Page analysis failed with exception: {exc}",
                            "raw_response": ""
                        }
                    pbar.update(1)
        
        return all_analyses

    def filter_story_pages(self, all_analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters out non-story pages from the analysis results.
        
        Args:
            all_analyses: List of page analysis results
            
        Returns:
            List of only story page analyses
        """
        story_pages = []
        filtered_count = 0
        
        for analysis in all_analyses:
            # Skip pages with errors
            if "error" in analysis:
                continue
                
            # Check if this is a story page
            is_story = analysis.get("is_story_page", True)  # Default to True for backward compatibility
            
            if is_story:
                story_pages.append(analysis)
            else:
                filtered_count += 1
                page_type = analysis.get("page_type", "unknown")
                print(f"Filtered out page {analysis.get('page', 'unknown')} (type: {page_type})")
        
        print(f"📖 Story pages: {len(story_pages)}, Non-story pages filtered: {filtered_count}")
        return story_pages

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python page_analyzer.py <path_to_image_1> [<path_to_image_2> ...]")
        sys.exit(1)

    image_files = sys.argv[1:]
    
    try:
        analyzer = PageAnalyzer()
        if len(image_files) == 1:
            # Single page analysis
            analysis = analyzer.analyze_page(image_files[0], 1, 1)
            print(json.dumps(analysis, indent=2))
        else:
            # Batch analysis
            analyses = analyzer.analyze_pages_in_parallel(image_files)
            print(json.dumps(analyses, indent=2))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)