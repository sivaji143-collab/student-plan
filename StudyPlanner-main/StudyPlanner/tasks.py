import uuid
from datetime import datetime


class Task:
    """
    Represents a single study task.
    Difficulty is on a scale of 1 (Easy) to 5 (Hard).
    """
    def __init__(self, topic: str, description: str = "", difficulty: int = 3, time_needed: int = 30, due_date: str = "N/A", task_id: str = None, is_completed: bool = False, created_at: str = None):
        self.id = task_id if task_id else uuid.uuid4().hex
        self.topic = topic
        self.description = description
        # Ensure difficulty is an integer between 1 and 5
        self.difficulty = max(1, min(5, int(difficulty)))
        # Time needed in minutes
        self.time_needed = max(5, int(time_needed))
        self.due_date = due_date
        self.is_completed = is_completed
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self):
        """Converts the Task object to a dictionary for storage."""
        return {
            "id": self.id,
            "topic": self.topic,
            "description": self.description,
            "difficulty": self.difficulty,
            "time_needed": self.time_needed,
            "due_date": self.due_date,
            "is_completed": self.is_completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Task object from a dictionary."""
        return cls(
            task_id=data.get("id"),
            topic=data.get("topic", "Unknown Topic"),
            description=data.get("description", "No description provided."),
            difficulty=data.get("difficulty", 3),
            time_needed=data.get("time_needed", 30),
            due_date=data.get("due_date", "N/A"),
            is_completed=data.get("is_completed", False),
            created_at=data.get("created_at"),
        )

    def __str__(self):
        status = "✅ Completed" if self.is_completed else "⏳ Pending"
        return (
            f"[{self.id[:4]}] {self.topic} ({status})\n"
            f"  Desc: {self.description}\n"
            f"  Difficulty: {self.difficulty}/5 | Time: {self.time_needed} mins | Due: {self.due_date}"
        )


# Helper function to generate a simple short ID (used in Task if task_id is None)
def generate_task_id():
    return uuid.uuid4().hex