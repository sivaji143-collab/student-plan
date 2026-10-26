import json
import os
from utils import random_choice, load_json
from tasks import Task

class ResponseGenerator:
    """
    Generates flexible and varied natural responses using templates.
    """
    def __init__(self, templates_file: str = "templates.json"):
        self.templates = load_json(templates_file)

    def generate(self, intent: str, data: dict = None) -> str:
        """
        Generates a response based on the detected intent and data.
        
        :param intent: The NLU intent (e.g., 'add_task_success').
        :param data: A dictionary containing data to fill the templates.
        :return: The formatted response string.
        """
        data = data if data is not None else {}
        
        # Handle NLU Fallback
        if intent == "fallback":
            return random_choice(self.templates.get("nlu_fallback", ["I'm having trouble understanding."]))
        
        # Get the list of templates for the intent
        template_list = self.templates.get(intent)
        
        if not template_list:
            return f"SYSTEM ERROR: No template found for intent '{intent}'."

        # Choose a random template
        template = random_choice(template_list)
        
        # Format the template with the provided data
        try:
            return template.format(**data)
        except KeyError as e:
            print(f"ERROR: Template for '{intent}' is missing key: {e}")
            return template # Return unfomatted if formatting fails
        except Exception as e:
            print(f"ERROR during response generation: {e}")
            return template
            
    def format_tasks_list(self, tasks: list[Task]) -> str:
        """Formats a list of Task objects into a readable string."""
        if not tasks:
            return ""
        
        task_strings = []
        for i, task in enumerate(tasks):
            # Shortened display for the list view
            status = "✅" if task.is_completed else "⏳"
            task_strings.append(f"  {i+1}. [{task.id[:4]}] {task.topic} ({task.time_needed} min, D:{task.difficulty}) {status}")
            
        return "\n".join(task_strings)