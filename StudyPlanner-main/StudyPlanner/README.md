🧠 Minimal Study Planner Agent (StudyPlanner)

StudyPlanner is a lightweight, AI-powered conversational agent designed to help students add tasks, organize topics, track progress, and receive study recommendations.

The entire project is built using only the Python Standard Library, making it fast and easy to deploy.

✨ Features

Task Management: Add new tasks with topic, difficulty (1-5), and time needed.

Progress Tracking: Mark tasks as complete and view pending lists.

Intelligent Planning: The Planner recommends the next task based on a priority score (prioritizing high-difficulty, short-time tasks).

Conversational Interface: Uses simple Natural Language Understanding (NLU) to interpret commands.

Persistence: Task data is saved locally to storage.json.

🚀 Installation & Usage

Since this project uses only the Python Standard Library, no external requirements.txt dependencies are needed.

Prerequisites

Python 3.8+

Running the Agent

Navigate to the project directory:

cd studyPlanner


Run the main entry point:

python main.py


Example Commands

Once the agent is running, try these inputs:

Action

Example Input

Greeting

Hello

Add Task

add a task on microeconomics for 45 minutes, difficulty 4

Add Task (Implicit)

I need to study organic chemistry for 2 hours

List Tasks

show my tasks

Get Recommendation

what should I study next

Complete Task

complete task 1234 (Use the 4-digit ID shown when listing tasks)

Exit

quit or exit

📐 Project Structure

File

Description

main.py

Entry point. Runs the main CLI loop.

agent.py

Core orchestration. Directs flow between NLU, Memory, and Planner.

nlu.py

Lightweight NLU for intent and entity extraction (uses regex).

response_generator.py

Handles all conversational output using templates.

memory.py

Manages the persistence of tasks (reads/writes to storage.json).

planner.py

The task recommender engine. Calculates priority scores.

tasks.py

Defines the Task class and its serialization methods.

templates.json

Stores human-readable response strings for the agent.

storage.json

Local storage for all tasks and history (auto-created).

utils.py

Small helpers (JSON I/O, text normalization, randomness).