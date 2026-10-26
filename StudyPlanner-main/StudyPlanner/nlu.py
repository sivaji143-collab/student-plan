import re
from utils import normalize_text


class NLU:
    """
    Lightweight Natural Language Understanding component.
    Identifies intent and extracts simple entities using regex and keyword matching.
    """
    def __init__(self):
        # Regex patterns for key intents
        self.patterns = {
            "add_task": re.compile(r"(add|new|create|schedule)\s+task|study\s+(.+?)(\s+for\s+(\d+)\s*min)", re.IGNORECASE),
            "complete_task": re.compile(r"(complete|done|finish|mark)\s+(?:task\s+)?(.+)", re.IGNORECASE),
            "view_tasks": re.compile(r"(list|show|view|what are|tasks|schedule)", re.IGNORECASE),
            "get_recommendation": re.compile(r"(recommend|next|best|what\s+should\s+i\s+do)", re.IGNORECASE),
            "greet": re.compile(r"(hello|hi|hey|greetings)", re.IGNORECASE),
        }
        
        # Keywords for entity extraction
        self.difficulty_keywords = {
            "easy": 1, "simple": 1,
            "medium": 3, "average": 3,
            "hard": 5, "difficult": 5, "tough": 5
        }

    def _extract_task_details(self, text: str) -> dict:
        """Extracts topic, time, and difficulty from a given text."""
        entities = {}
        
        # 1. Extract Time (e.g., "60 minutes" or "30min")
        time_match = re.search(r'(\d+)\s*(minutes?|min|hrs?)', text, re.IGNORECASE)
        if time_match:
            time_val = int(time_match.group(1))
            unit = time_match.group(2).lower()
            # Convert hours to minutes if necessary
            entities['time_needed'] = time_val * 60 if 'hr' in unit else time_val
        
        # 2. Extract Difficulty (e.g., "difficulty 4" or "easy")
        difficulty_match = re.search(r'(difficulty|level|rating)\s*(\d)', text, re.IGNORECASE)
        if difficulty_match:
            entities['difficulty'] = int(difficulty_match.group(2))
        else:
            # Check for keyword difficulty
            for keyword, value in self.difficulty_keywords.items():
                if keyword in normalize_text(text):
                    entities['difficulty'] = value
                    break
        
        # 3. Extract Topic (simple placeholder until better extraction is implemented)
        # This is a basic placeholder; in a real NLU, this would be more complex.
        topic_match = re.search(r'(?:task|study|on|about)\s+(.+?)(?:\s+for\s+\d+|$)', text, re.IGNORECASE)
        if topic_match:
            topic = topic_match.group(1).strip()
            # Try to clean up the topic by removing other entities
            if 'time_needed' in entities:
                topic = re.sub(r'\s*\d+\s*(minutes?|min|hrs?)', '', topic, re.IGNORECASE).strip()
            if 'difficulty' in entities:
                topic = re.sub(r'(difficulty|level|rating)\s*\d', '', topic, re.IGNORECASE).strip()
                for keyword in self.difficulty_keywords:
                    topic = re.sub(r'\b' + keyword + r'\b', '', topic, re.IGNORECASE).strip()
            
            entities['topic'] = topic.strip().capitalize()
        
        # Fallback for simple topic extraction
        if 'topic' not in entities and not any(intent in text for intent in ["view", "list", "recommend", "complete"]):
            # Assume the whole input is a topic if no other intent is strong
            if len(text.split()) > 1 and len(text) < 50:
                entities['topic'] = text.strip().capitalize()

        return entities

    def parse(self, text: str) -> dict:
        """Main parsing method to determine intent and entities."""
        result = {"intent": "fallback", "entities": {}, "confidence": 0.5}
        
        normalized_text = normalize_text(text)
        
        # Check for specific intents
        for intent, pattern in self.patterns.items():
            match = pattern.search(text)
            if match:
                result['intent'] = intent
                result['confidence'] = 0.9
                
                # Special handling for entity extraction based on intent
                if intent == "add_task":
                    result['entities'] = self._extract_task_details(text)
                    # If we found time and a topic, increase confidence
                    if result['entities'].get('topic') and result['entities'].get('time_needed'):
                        result['confidence'] = 1.0
                
                elif intent == "complete_task":
                    # Extract the query (ID or topic) after the trigger word
                    query = match.group(2).strip()
                    if query:
                        result['entities']['query'] = query
                        result['confidence'] = 1.0
                    else:
                        # Fallback if no query provided after "complete"
                        result['intent'] = "fallback"

                return result
        
        # If no specific intent matched, try to extract task details anyway (potential implicit add_task)
        entities = self._extract_task_details(text)
        if entities.get('topic') and entities.get('time_needed'):
            result['intent'] = "add_task"
            result['entities'] = entities
            result['confidence'] = 0.8
        
        return result