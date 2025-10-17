# ─────────────────────────────────────────────────────────────────────────────
# Imports: Core modules for path handling, subprocess execution, and typing
# ─────────────────────────────────────────────────────────────────────────────
import pathlib
import subprocess
import json
from   typing               import Tuple

# LangChain tool decorator for exposing functions to agent
from   langchain_core.tools import tool

# ─────────────────────────────────────────────────────────────────────────────
# Project root directory for all generated files
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"

# ─────────────────────────────────────────────────────────────────────────────
# Utility: Validates and resolves safe file paths within project root
# ─────────────────────────────────────────────────────────────────────────────
def safe_path_for_project(path: str) -> pathlib.Path:
    """
    Resolves a given path relative to PROJECT_ROOT and ensures it's safe.
    Prevents accidental writes outside the designated workspace.
    """
    p = (PROJECT_ROOT / path).resolve()
    if (
            PROJECT_ROOT.resolve() not in p.parents
            and PROJECT_ROOT.resolve() != p.parent
            and PROJECT_ROOT.resolve() != p
        ):
        raise ValueError("Attempt to write outside project root")
    return p

# ─────────────────────────────────────────────────────────────────────────────
# Tool: Write content to a file within project root
# ─────────────────────────────────────────────────────────────────────────────
@tool
def write_file(path: str, content: str) -> str:
    """
    Creates or overwrites a file at the given path.
    Ensures parent directories exist and writes UTF-8 encoded content.
    """
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Optional: try to decode escaped JSON if it's valid
    try:
        content     = json.loads(content)
        if isinstance(content, dict):
            content = json.dumps(content, indent=2)
    except json.JSONDecodeError:
        pass  # Leave content as-is if not valid JSON

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"

# ─────────────────────────────────────────────────────────────────────────────
# Tool: Read content from a file within project root
# ─────────────────────────────────────────────────────────────────────────────
@tool
def read_file(path: str) -> str:
    """
    Reads UTF-8 content from the specified file.
    Returns an empty string if the file does not exist.
    """
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

# ─────────────────────────────────────────────────────────────────────────────
# Tool: Return current working directory (project root)
# ─────────────────────────────────────────────────────────────────────────────
@tool
def get_current_directory() -> str:
    """
    Returns the absolute path of the project root directory.
    Used for context in agent prompts or shell commands.
    """
    return str(PROJECT_ROOT)

# ─────────────────────────────────────────────────────────────────────────────
# Tool: List all files in a given directory within project root
# ─────────────────────────────────────────────────────────────────────────────
@tool
def list_files(directory: str = ".") -> str:
    """
    Recursively lists all files in the specified directory.
    Returns relative paths. Handles invalid directory gracefully.
    """
    p     = safe_path_for_project(directory)

    if not p.is_dir():
        return f"ERROR: {p} is not a directory"

    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

# wanted to check the reason for wrong toll call 
# ─────────────────────────────────────────────────────────────────────────────
# Tool: Run shell command in a safe project directory
# ─────────────────────────────────────────────────────────────────────────────
@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """
    Executes a shell command in the specified directory.
    Returns (exit_code, stdout, stderr). Defaults to project root.
    """
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
    res     = subprocess.run(
                                cmd,
                                shell          = True,
                                cwd            = str(cwd_dir),
                                capture_output = True,
                                text           = True,
                                timeout        = timeout
                            )
    return res.returncode, res.stdout, res.stderr

# ─────────────────────────────────────────────────────────────────────────────
# Init: Create project root directory if not already present
# ─────────────────────────────────────────────────────────────────────────────
def init_project_root():
    """
    Ensures the project root directory exists.
    Used during setup or before the file operations.
    """
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)