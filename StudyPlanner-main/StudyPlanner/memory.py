import os
from datetime import datetime
from tasks import Task
from utils import load_json, save_json, STORAGE_FILE


class Memory:
    """Manages the persistence and retrieval of tasks and history."""
    
    def __init__(self):
        self.tasks = []
        self.history = []
        self._load()

    def _load(self):
        """Loads data from the storage file."""
        data = load_json(STORAGE_FILE)
        
        # Load tasks
        self.tasks = [Task.from_dict(d) for d in data.get("tasks", [])]
        
        # Load history (completed tasks/logs)
        self.history = data.get("history", [])

    def _save(self):
        """Saves current tasks and history to the storage file."""
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "history": self.history
        }
        save_json(STORAGE_FILE, data)

    def add_task(self, task: Task):
        """Adds a new task to the memory and saves."""
        self.tasks.append(task)
        print(f"DEBUG: Added task {task.id}")
        self._save()

    def get_tasks(self, completed: bool = False) -> list:
        """Returns a list of tasks, filtered by completion status."""
        return [t for t in self.tasks if t.is_completed == completed]

    def find_task(self, query: str):
        """
        Finds a task by ID (first 4 chars) or topic. Prioritizes pending tasks.
        """
        query = query.lower()
        
        # Search pending tasks first
        pending_tasks = self.get_tasks(completed=False)
        for task in pending_tasks:
            # Check ID (first 4 chars) or full topic match
            if task.id.startswith(query) or query in task.topic.lower():
                return task
        
        # If no pending task found, search all tasks by ID
        for task in self.tasks:
            if task.id.startswith(query):
                return task
                
        return None

    def complete_task(self, task_id: str):
        """Marks a task as completed and moves it to history log."""
        for task in self.tasks:
            if task.id == task_id and not task.is_completed:
                task.is_completed = True
                
                # Log completion event
                self.history.append({
                    "task_id": task.id,
                    "completed_at": datetime.now().isoformat()
                })
                
                self._save()
                print(f"DEBUG: Completed task {task.id}")
                return task
        return None


# Initial check to ensure storage.json exists with the basic structure
if not os.path.exists(STORAGE_FILE):
    save_json(STORAGE_FILE, {"tasks": [], "history": []})