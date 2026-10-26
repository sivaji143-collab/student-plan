import json
import os
import random
import re

STORAGE_FILE = "storage.json"

def load_json(filepath: str) -> dict:
    """Loads JSON data from a file, returning an empty dict if the file is missing."""
    if not os.path.exists(filepath):
        print(f"INFO: Storage file '{filepath}' not found. Initializing new data structure.")
        return {"tasks": [], "history": []}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from '{filepath}'. Returning empty data.")
        return {"tasks": [], "history": []}
    except Exception as e:
        print(f"ERROR loading {filepath}: {e}")
        return {"tasks": [], "history": []}

def save_json(filepath: str, data: dict):
    """Saves dictionary data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"ERROR saving {filepath}: {e}")

def normalize_text(text: str) -> str:
    """Converts text to lowercase and removes non-alphanumeric characters for comparison."""
    text = text.lower()
    return re.sub(r'[^a-z0-9\s]', '', text)

def random_choice(data: list):
    """Returns a random element from a list."""
    if data:
        return random.choice(data)
    return ""