# ─────────────────────────────────────────────────────────────────────────────
# Prompt: Planner agent — Converts user request into structured engineering plan
# ─────────────────────────────────────────────────────────────────────────────
def planner_prompt(user_prompt: str) -> str:
    """
    Constructs the prompt for the PLANNER agent.
    Injects the raw user request into a scaffold that guides the LLM to produce:
    - App name, description, tech stack, features, and file layout.
    """
    PLANNER_PROMPT = f"""
You are the PLANNER agent. Convert the user prompt into a COMPLETE engineering project plan.

User request:
{user_prompt}
    """
    return PLANNER_PROMPT

# ─────────────────────────────────────────────────────────────────────────────
# Prompt: Architect agent — Converts Plan into ordered implementation tasks
# ─────────────────────────────────────────────────────────────────────────────
def architect_prompt(plan: str) -> str:
    """
    Constructs the prompt for the ARCHITECT agent.
    Injects the Plan JSON and guides the LLM to:
    - Create IMPLEMENTATION TASKS for each file
    - Specify exact logic, naming, dependencies, and integration details
    - Maintain order and context across steps
    """
    ARCHITECT_PROMPT = f"""
You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.

RULES:
- For each FILE in the plan, create one or more IMPLEMENTATION TASKS.
- In each task description:
    * Specify exactly what to implement.
    * Name the variables, functions, classes, and components to be defined.
    * Mention how this task depends on or will be used by previous tasks.
    * Include integration details: imports, expected function signatures, data flow.
- Order tasks so that dependencies are implemented first.
- Each step must be SELF-CONTAINED but also carry FORWARD the relevant context from earlier tasks.

Project Plan:
{plan}
    """
    return ARCHITECT_PROMPT

# ─────────────────────────────────────────────────────────────────────────────
# Prompt: Coder agent — System-level instructions for tool-using implementation
# ─────────────────────────────────────────────────────────────────────────────
def coder_system_prompt() -> str:
    """
    Constructs the system prompt for the CODER agent.
    Guides the agent to:
    - Read existing files for compatibility
    - Implement full file content with modular integration
    - Maintain naming consistency and validate imports
    """

    CODER_SYSTEM_PROMPT = """
You are the CODER agent.
You are implementing a specific engineering task.
You have access to the following tools to read and write files.

Available tools:
- read_file(path)
- write_file(path, content)
- list_files(directory)
- get_current_directory()

Always:
- Do not call tools that are not listed above.
- Use list_files(directory) to explore the file structure.
- Use read_file(path) to inspect existing content.
- Use write_file(path, content) to save changes.
- Review existing files to maintain compatibility and avoid duplication.
- Implement the FULL file content, integrating with other modules.
- Maintain consistent naming of variables, functions, classes, and imports.
- When a module is imported from another file, ensure it exists and is implemented as described.
    """
    return CODER_SYSTEM_PROMPT