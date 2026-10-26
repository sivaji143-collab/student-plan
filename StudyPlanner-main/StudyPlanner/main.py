import sys
import os
from agent import StudyPlannerAgent
from utils import save_json, STORAGE_FILE


def main():
    """Main function to run the Study Planner CLI."""
    try:
        agent = StudyPlannerAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        sys.exit(1)

    print("-" * 50)
    print("🧠 Minimal Study Planner Agent 🗓️")
    print("Type 'exit' or 'quit' to close the planner.")
    print("-" * 50)
    
    # Send a greeting message
    print(agent.process_input("Hi!"))

    while True:
        try:
            user_input = input("You > ")
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye! Happy studying.")
                break
            
            if not user_input.strip():
                continue

            response = agent.process_input(user_input)
            print(f"\nAgent > {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye! Happy studying.")
            break
        except EOFError:
            print("\nGoodbye! Happy studying.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Ensure all components have been initialized or files created
    if not os.path.exists(STORAGE_FILE):
        save_json(STORAGE_FILE, {"tasks": [], "history": []})
        
    main()