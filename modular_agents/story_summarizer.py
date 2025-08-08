# modular_agents/story_summarizer.py
import sys
import json
from typing import List, Dict, Any

import google.generativeai as genai

from . import config

class StorySummarizer:
    """
    Generates a story summary from a list of page analyses.
    """
    def __init__(self, model_name: str = None):
        """
        Initialize the StorySummarizer.
        
        Args:
            model_name: This parameter is ignored. StorySummarizer always uses gemini-2.0-flash
                       as per system requirements to ensure consistent story summarization.
        """
        genai.configure(api_key=config.GEMINI_API_KEY)
        # Configure model with low temperature to reduce hallucinations
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,  # Low temperature for more focused, less creative output
            top_p=0.8,
            top_k=40,
            max_output_tokens=8192,
        )
        # Always use the fixed model for story summarization - hardcoded as per requirements
        self.model = genai.GenerativeModel(
            config.FIXED_MODEL_NAME,  # Always "gemini-2.0-flash"
            generation_config=generation_config
        )

    def summarize_story(self, page_analyses: List[Dict[str, Any]]) -> str:
        """
        Generates a comprehensive story summary from a list of page analyses.
        """
        valid_analyses = [p for p in page_analyses if "error" not in p]
        
        if not valid_analyses:
            return "Error: No valid page analyses provided to generate a summary."

        analyses_str = json.dumps(valid_analyses, indent=2)

        prompt = f"""You are a master comic book analyst and storytelling expert specializing in comprehensive narrative synthesis.

        Your task is to create an exceptionally detailed, emotionally rich story summary that captures the complete essence of this comic book story. This summary will be used as the foundation for creating an engaging YouTube script that covers the entire comic story comprehensively.

        **Page Analyses:**
        {analyses_str}

        **CRITICAL REQUIREMENTS:**

        **CRITICAL WORD COUNT REQUIREMENT:**
        - Your summary must be between 400-600 words EXACTLY
        - Count every word as you write
        - If approaching 600 words, conclude efficiently while ensuring completeness
        - This summary will be used to create a 250-350 word script, so focus on the most essential story elements
        
        **COMPREHENSIVE COVERAGE WITHIN LIMITS:**
        - Include EVERY significant plot point, character moment, and story beat
        - Cover the entire narrative arc from opening to conclusion  
        - Don't skip or summarize major scenes - give them appropriate narrative weight
        - Include all character introductions, developments, and relationships
        - Prioritize story elements that will be essential for the final script

        **EFFICIENCY AND CONCISENESS:**
        - Every sentence must contribute essential story information
        - Combine related plot points where possible to save words
        - Focus on plot progression and character actions over excessive description
        - Write with the awareness that this feeds into a 250-350 word script

        **2. EMOTIONAL DEPTH & CHARACTER PSYCHOLOGY:**
        - Capture the internal emotional states of all main characters
        - Explain character motivations, fears, and desires
        - Include emotional beats: moments of tension, relief, surprise, sadness, triumph
        - Describe how characters change or grow throughout the story
        - Include psychological subtext and unspoken dynamics between characters

        **3. RICH CONTEXTUAL DETAILS:**
        - Describe key settings and how they contribute to mood
        - Include important dialogue or dialogue summaries that reveal character
        - Explain the stakes and consequences of actions
        - Provide backstory elements revealed during the narrative
        - Include world-building details that enrich the story

        **4. DRAMATIC STRUCTURE & PACING:**
        - Clearly establish the story's inciting incident
        - Build tension and conflict progressively
        - Identify and elaborate on the climax and resolution
        - Include quiet character moments alongside action sequences
        - Show how different story threads weave together

        **5. NARRATIVE FLOW & STORYTELLING:**
        - Write in engaging, flowing prose that reads like a compelling story
        - Use specific, vivid details rather than generic descriptions
        - Create smooth transitions between scenes and plot points
        - Maintain narrative momentum while being thorough
        - End with a satisfying conclusion that ties up story threads

        **6. COMPLETENESS FOR SCRIPT ADAPTATION:**
        - Provide enough detail that a scriptwriter could create a full video script
        - Include all key visual moments and action sequences
        - Cover all important character interactions and relationship dynamics
        - Ensure no significant story element is overlooked or underexplored

        **WRITING STYLE:**
        - Write in third person, past tense
        - Use sophisticated but accessible language
        - Create paragraphs that each focus on a distinct story beat or emotional moment
        - Balance action, character development, and emotional resonance
        - Make the summary engaging to read as a standalone narrative

        **OUTPUT:** A single, comprehensive story summary of exactly 400-600 words that serves as the complete foundation for the entire comic book story. Include a final word count verification.

        **Story Summary:**
        """

        response = self.model.generate_content(prompt)
        return response.text

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python story_summarizer.py <path_to_json_file_with_analyses>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r') as f:
            analyses = json.load(f)
        
        summarizer = StorySummarizer()
        summary = summarizer.summarize_story(analyses)
        print(summary)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)