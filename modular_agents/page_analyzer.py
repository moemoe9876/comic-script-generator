# modular_agents/page_analyzer.py
import os
import sys
import json
from typing import Dict, Any, List
import concurrent.futures
from tqdm import tqdm

import google.generativeai as genai

import config

class PageAnalyzer:
    """
    Analyzes comic book pages using the Gemini API, with support for parallel processing.
    """
    def __init__(self, batch_size: int = None):
        """
        Initialize the PageAnalyzer with optional batch size for parallel processing.
        
        Args:
            batch_size: Optional batch size for processing multiple pages. If None,
                       will be calculated based on available CPU cores.
        """
        genai.configure(api_key=config.GEMINI_API_KEY)
        # Configure model with low temperature to reduce hallucinations
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,  # Low temperature for more focused, less creative output
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
        )
        self.model = genai.GenerativeModel(
            config.GENERATIVE_MODEL_NAME,
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
            Extract the key information and return it as a JSON object.

            **JSON Schema:**
            {{
              "page": {page_number},
              "setting": "A brief description of the location and environment.",
              "characters_present": ["Character A", "Character B"],
              "key_actions_or_events": [
                "A summary of the most important action on the page.",
                "Another key event."
              ],
              "key_dialogue_summary": "A summary of the most important dialogue, capturing the core intent."
            }}

            **Rules:**
            - Provide only the JSON object in your response.
            - If a field is not applicable, use an empty string or empty list.

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