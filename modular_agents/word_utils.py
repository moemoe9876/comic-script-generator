import re

def count_words(text):
    """
    Count words in a string, handling punctuation and unicode robustly.
    Returns the word count as an integer.
    """
    # Use regex to match words (unicode aware)
    words = re.findall(r'\b\w+\b', text, re.UNICODE)
    return len(words)
