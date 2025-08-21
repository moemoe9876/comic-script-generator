import google.generativeai as genai
import json
from .config import GEMINI_API_KEY, FIXED_MODEL_NAME

class ImageSelector:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(FIXED_MODEL_NAME)

    def select_images(self, script, page_analysis, max_segments: int | None = None, min_seconds: int = 4, max_seconds: int = 10):
        """Select pages and map them to substantial script text chunks.

        Args:
            script: The full generated script text.
            page_analysis: Page-by-page analyses (list/dict) produced by PageAnalyzer.
            max_segments: Optional maximum number of page-text pairs to return.
            min_seconds: Minimum target seconds per segment (default 4).
            max_seconds: Maximum target seconds per segment (default 10).
        Returns:
            List of objects: [{"page_number": int, "text": "..."}, ...]
        """
        prompt = self._build_prompt(script, page_analysis, max_segments, min_seconds, max_seconds)
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)

    def _build_prompt(self, script, page_analysis, max_segments, min_seconds, max_seconds):
        seconds_range = f"{min_seconds}-{max_seconds}"
        max_segments_text = f"Limit the total number of segments to {max_segments}." if max_segments else "Do not select an excessive number of segments; keep the selection concise."

        prompt = f"""
You are an expert comic book video creator making a YouTube short (under 90 seconds). Your task is to select a small, impactful set of comic book pages and map them to substantial chunks of the provided script.

**Script:**
{script}

**Page-by-Page Analysis:**
{page_analysis}

**Guidelines:**
- Break the script into meaningful chunks where each chunk is substantial enough to be narrated for approximately {seconds_range} seconds. Aim for text chunks that contain roughly the number of words corresponding to that duration (assume ~3 words/second).
- For each chunk, select the single best page number from the page analysis that visually represents that chunk.
- Provide a one-to-one mapping between each selected page and the chunk of script text.
- {max_segments_text}

**Output Format:**
Return a valid JSON array of objects. Each object must have the keys: "page_number" (integer) and "text" (the chunk of script text to display/narrate for that page).

**Example Output:**
```json
[
  {{
    "page_number": 1,
    "text": "In the sprawling metropolis of Neo-Veridia, towering chrome spires pierced the clouds, casting long shadows over the bustling streets below."
  }},
  {{
    "page_number": 3,
    "text": "Suddenly, a crimson alert flashed across the city's sky-screens, signaling a threat from the outer sectors. Our hero, Captain Comet, suited up, his face a mask of grim determination."
  }}
]
```

Please respond with only the JSON array and nothing else.
"""
        return prompt

    def _parse_response(self, response_text):
        try:
            raw = response_text
            # If model wrapped JSON in code fences, extract the JSON block
            if '```json' in raw:
                raw = raw.split('```json', 1)[1].split('```', 1)[0]
            elif '```' in raw:
                # sometimes they use generic fences
                raw = raw.split('```', 1)[1].split('```', 1)[0]

            raw = raw.strip()
            selected_pairs = json.loads(raw)

            if not isinstance(selected_pairs, list):
                return []

            # Validate structure and coerce types where reasonable
            validated = []
            for item in selected_pairs:
                if not isinstance(item, dict):
                    continue
                page = item.get('page_number') or item.get('page') or item.get('pageNumber')
                text = item.get('text') or item.get('sentence') or item.get('chunk')
                try:
                    page_int = int(page)
                except Exception:
                    continue
                if not isinstance(text, str) or text.strip() == '':
                    continue
                validated.append({'page_number': page_int, 'text': text.strip()})

            return validated
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response from image selector: {e}")
            print(f"Raw response was: {response_text}")
            return []
        except Exception as e:
            print(f"Unexpected error parsing image selector response: {e}")
            return []
