# ─────────────────────────────────────────────────────────────────────────────
# Entry Point: CLI interface for GenAI_BuildBuddy agent execution
# ─────────────────────────────────────────────────────────────────────────────

# Core modules for argument parsing, error handling, and system exit
import argparse
import sys
import traceback

# Import compiled LangGraph agent from graph definition
from agent.graph import agent

# ─────────────────────────────────────────────────────────────────────────────
# Main function: Handles CLI input, agent invocation, and error management
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # Set up the CLI argument parser with a recursion limit option
    parser = argparse.ArgumentParser(description = "Run engineering project planner")
    parser.add_argument(
                            "--recursion-limit", "-r",
                            type    = int,
                            default = 100,
                            help    = "Recursion limit for processing (default: 100)"
                        )
    args   = parser.parse_args()

    try:
        # Prompt user for project description
        user_prompt = input("Enter your project prompt: ")

        # Invoke LangGraph agent with user input and recursion control
        result      = agent.invoke(
                                    {"user_prompt"     : user_prompt},
                                    {"recursion_limit" : args.recursion_limit}
                                  )

        # Display final state returned by agent
        print("Final State:", result)

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\nOperation cancelled by user.")
        sys.exit(0)

    except Exception as e:
        # Print full traceback for debugging and exit with error code
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Script trigger: Executes main() when run directly
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()