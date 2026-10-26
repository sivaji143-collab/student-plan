from nlu import NLU
from memory import Memory
from planner import Planner
from response_generator import ResponseGenerator
from tasks import Task


class StudyPlannerAgent:
    """
    Main agent that orchestrates NLU, Memory, Planner, and ResponseGenerator.
    """
    def __init__(self):
        self.nlu = NLU()
        self.memory = Memory()
        self.planner = Planner()
        self.response_gen = ResponseGenerator()

    def process_input(self, user_input: str) -> str:
        """
        Main processing loop:
        1. Parse input with NLU
        2. Determine intent
        3. Execute corresponding action
        4. Generate response
        """
        # Parse user input
        parsed = self.nlu.parse(user_input)
        intent = parsed["intent"]
        entities = parsed["entities"]

        # Route based on intent
        if intent == "greet":
            return self.response_gen.generate("greet")

        elif intent == "add_task":
            return self._handle_add_task(entities)

        elif intent == "view_tasks":
            return self._handle_view_tasks()

        elif intent == "complete_task":
            return self._handle_complete_task(entities)

        elif intent == "get_recommendation":
            return self._handle_recommendation()

        else:  # fallback
            return self.response_gen.generate("fallback")

    def _handle_add_task(self, entities: dict) -> str:
        """Handles task creation."""
        topic = entities.get("topic")
        time_needed = entities.get("time_needed")
        difficulty = entities.get("difficulty", 3)

        if not topic or time_needed is None:
            return self.response_gen.generate("add_task_incomplete")

        # Create and save the task
        task = Task(
            topic=topic,
            description="",
            difficulty=difficulty,
            time_needed=time_needed,
        )
        self.memory.add_task(task)

        return self.response_gen.generate(
            "add_task_success",
            {"topic": topic, "time_needed": time_needed}
        )

    def _handle_view_tasks(self) -> str:
        """Handles viewing all pending tasks."""
        pending_tasks = self.memory.get_tasks(completed=False)

        if not pending_tasks:
            return self.response_gen.generate("view_tasks_empty")

        tasks_list = self.response_gen.format_tasks_list(pending_tasks)
        return self.response_gen.generate(
            "view_tasks_header",
            {"count": len(pending_tasks), "tasks_list": tasks_list}
        )

    def _handle_complete_task(self, entities: dict) -> str:
        """Handles marking a task as complete."""
        query = entities.get("query", "").strip()

        if not query:
            return self.response_gen.generate("add_task_incomplete")

        # Find task by query
        task = self.memory.find_task(query)

        if not task:
            return self.response_gen.generate(
                "complete_task_not_found",
                {"query": query}
            )

        # Complete the task
        self.memory.complete_task(task.id)
        return self.response_gen.generate(
            "complete_task_success",
            {"topic": task.topic}
        )

    def _handle_recommendation(self) -> str:
        """Handles getting a task recommendation."""
        recommended_task = self.planner.get_recommendation(self.memory.tasks)

        if not recommended_task:
            return self.response_gen.generate("recommend_none")

        task_details = str(recommended_task)
        return self.response_gen.generate(
            "recommend_task",
            {"task_details": task_details}
        )