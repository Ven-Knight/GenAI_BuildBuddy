# 🛠️ BuildBuddy

**BuildBuddy** is an AI-powered coding assistant built with [LangGraph](https://github.com/langchain-ai/langgraph).  
It functions as a multi-agent development team that transforms natural language requests into complete, working projects — file by file — using real-world developer workflows.

---

## 🏗️ Architecture Overview

Coder Buddy orchestrates three specialized agents:

- **🧠 Planner Agent** – Interprets user intent and generates a high-level project roadmap.
- **📐 Architect Agent** – Breaks the roadmap into granular engineering tasks with file-level context.
- **💻 Coder Agent** – Executes each task, writes code directly to files, and uses tools like a real developer.

<p align="center">
  <img src="resources/coder_buddy_diagram.png" alt="Coder Buddy Architecture" width="90%">
</p>

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for virtual environment and dependency management.
- Create a [Groq account](https://console.groq.com/keys) and generate your API key.

### ⚙️ Installation & Setup

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r pyproject.toml

# Configure environment variables
cp .sample_env .env
# Then edit .env with your Groq API key and other required values
```

### ▶️ Run the Application

```bash
python main.py
```

---

## 🧪 Example Prompts

Try these natural language instructions to generate full projects:

- “Create a to-do list application using HTML, CSS, and JavaScript.”
- “Build a simple calculator web app.”
- “Create a blog API in FastAPI with a SQLite backend.”

---
