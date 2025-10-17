# Load environment variables securely from .env file
from dotenv                     import load_dotenv

# Enable LangChain debug and verbose logging for traceability
from langchain.globals          import set_verbose, set_debug

# Use Groq-hosted OSS GPT model for fast, cost-effective inference
from langchain_groq.chat_models import ChatGroq

# Wraps Python functions as agent-callable tools with name and input schema support.
from langchain_core.tools       import Tool

# LangGraph constants and primitives for graph orchestration
from langgraph.constants        import END
from langgraph.graph            import StateGraph
from langgraph.prebuilt         import create_react_agent

# Modular imports for prompts, state schemas, and tool functions
from agent.prompts              import *
from agent.states               import *
from agent.tools                import write_file, read_file, get_current_directory, list_files

# Load environment variables (e.g., API keys) into runtime
_ = load_dotenv()

# Enable verbose and debug logs for audit clarity and troubleshooting
set_debug  (True)
set_verbose(True)

# Initialize LLM with structured output support (Groq-hosted GPT OSS 120B)
llm = ChatGroq(model="openai/gpt-oss-120b")


def planner_agent(state: dict) -> dict:
    """
    Step 1: - Convert a raw user prompt into a structured Plan object.
            - Uses planner_prompt() to guide LLM response
            - Ensures output conforms to Plan schema
    """
    user_prompt = state["user_prompt"]
    resp        = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))

    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """
    Step 2: - Convert the Plan into a TaskPlan with implementation steps.
            - Uses the architect_prompt() to guide LLM response
            - Injects original Plan into the TaskPlan for traceability
    """
    plan : Plan = state["plan"]
    resp        = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan=plan.model_dump_json()))

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    # Attach the original Plan to TaskPlan for downstream context
    resp.plan  = plan
    print(resp.model_dump_json())     # Optional: log TaskPlan for audit/debug
    return {"task_plan" : resp}


def coder_agent(state: dict) -> dict:
    """
    Step 3: - Execute the implementation steps using a LangGraph tool-using agent.
            - Reads the current step from TaskPlan
            - Loads existing file content
            - Invokes react_agent with system + user prompt
            - Increments step index for next iteration
    """
    coder_state: CoderState = state.get("coder_state")

    if coder_state is None:
        # Initialize the coder state with the first step
        coder_state  = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps            = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        # All steps completed — signal graph termination
        return {"coder_state": coder_state, "status": "DONE"}

    current_task     = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    # Construct prompts for tool-using agent
    system_prompt    = coder_system_prompt()
    user_prompt      = (
                            f"Task             : {current_task.task_description}\n"
                            f"File             : {current_task.filepath}\n"
                            f"Existing content :\n{existing_content}\n"
                            "Use write_file(path, content) to save your changes."
                       )

    # Register available tools for agent execution
    repo_browser_list_files = Tool.from_function(
                                        func        = list_files,
                                        name        = "repo_browser.list_files",
                                        description = "Lists all files in a given directory within the project root."
                                                 )

    coder_tools      = [read_file, write_file, repo_browser_list_files, get_current_directory]
    react_agent      = create_react_agent(llm, coder_tools)

    # Invoke agent with structured prompt
    react_agent.invoke({
                            "messages": [
                                            {"role": "system", "content": system_prompt},
                                            {"role": "user",   "content": user_prompt}
                                        ]
                       })

    # Move to the next step in TaskPlan
    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


# Define LangGraph execution flow using StateGraph
graph               = StateGraph(dict)

# Register nodes (modular agents)
graph.add_node("planner",   planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder",     coder_agent)

# Define directed edges between nodes
graph.add_edge("planner",   "architect")
graph.add_edge("architect", "coder")

# Conditional edge: loop coder until all steps are done
graph.add_conditional_edges(
                            "coder",
                             lambda s: "END" if s.get("status") == "DONE" else "coder",
                            {"END": END, "coder": "coder"}
                           )

# Set the entry point for graph execution
graph.set_entry_point("planner")

# Compile graph into executable agent
agent       = graph.compile()

# Entry point for manual testing or CLI invocation
if __name__ == "__main__":
    result  = agent.invoke(
                             {"user_prompt"     : "Build a colourful modern todo app in html css and js"},
                            {"recursion_limit" : 100}
                           )
    print("Final State:", result)