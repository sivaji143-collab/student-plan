from tasks import Task
from datetime import datetime


class Planner:
    """
    A simple recommender system to suggest the next best task.
    Uses a priority score based on difficulty and time required.
    """
    def get_recommendation(self, tasks: list):
        """
        Calculates a priority score for all pending tasks.
        Score formula: (Difficulty * 5) + (1 / (Time Needed in Hours))
        This prioritizes high-difficulty, shorter tasks.
        """
        pending_tasks = [t for t in tasks if not t.is_completed]

        if not pending_tasks:
            return None

        scored_tasks = []
        for task in pending_tasks:
            # Time in hours (to make the reciprocal value smaller)
            time_in_hours = task.time_needed / 60.0
            if time_in_hours < 0.1:  # Prevent division by near-zero for very short tasks
                time_in_hours = 0.1
                
            # Calculate the score. Higher is better.
            score = (task.difficulty * 5) + (1.0 / time_in_hours)
            
            # Simple tie-breaker: prioritize tasks due sooner (if due date is set)
            due_score = 0
            if task.due_date != "N/A":
                try:
                    due_date = datetime.fromisoformat(task.due_date)
                    time_until_due = (due_date - datetime.now()).total_seconds()
                    # Closer due date -> higher due_score
                    if time_until_due > 0:
                        due_score = 1000 / time_until_due  # Very simple inverse seconds
                except ValueError:
                    pass  # Ignore if due_date is invalid

            total_score = score + due_score
            scored_tasks.append((total_score, task))

        # Sort by score, descending
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        
        # Return the highest-scoring task
        return scored_tasks[0][1]