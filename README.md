MUBO

MUBO is a local AI coding assistant that runs on your own computer.

It connects a local language model with workspace tools so it can read files, search code, run tests, inspect Git changes, remember conversations, and answer questions about your codebase.

Features

* 🤖 Local AI through LM Studio
* 📁 Read, create, and update workspace files
* 🔎 Search code inside the workspace
* 💻 Run commands inside the workspace
* 🧪 Run Python tests with pytest
* 🔧 Git status, diff, log, and commit inspection
* 🧠 SQLite conversation memory
* 📚 Simple code-aware retrieval (RAG)
* 🌐 Simple web chat interface
* ⏱️ Response-time indicator
* 🔒 Workspace path protection and basic command safety

Architecture

Browser
   ↓
FastAPI
   ↓
MUBO Agent
   ├── File Tools
   ├── Terminal & Tests
   ├── Git Tools
   ├── SQLite Memory
   └── Code Retrieval
   ↓
Local LLM
(LM Studio)

Tech Stack

* Python
* FastAPI
* SQLite
* JavaScript
* HTML / CSS
* Git
* LM Studio
* pytest

Project Structure

MUBO/
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── ai.py
│   ├── file_tools.py
│   ├── terminal_tools.py
│   ├── memory.py
│   └── rag.py
│
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── workspace/
│   └── example project files
│
├── .gitignore
├── requirements.txt
└── README.md

How It Works

When a user sends a request, MUBO first checks whether a workspace tool is needed.

For example:

"list files"
      ↓
MUBO Agent
      ↓
File Tool
      ↓
Workspace

For normal questions, MUBO sends the request to a locally running language model.

For code-related questions, MUBO can retrieve relevant code from the workspace and provide it as context to the model.

Conversation history is stored locally in SQLite so recent interactions can be used as context.

Running MUBO

1. Create the virtual environment

python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies

pip install -r requirements.txt

3. Start LM Studio

Run a compatible local model and enable the OpenAI-compatible server.

MUBO currently expects the server at:

http://127.0.0.1:1234/v1

4. Start MUBO

uvicorn app.main:app --reload

Then open:

http://127.0.0.1:8000

Example Requests

MUBO can handle requests such as:

What is Python?
list files
read hello.py
search print
write test.py: print("Hello")
run python test.py
run tests
git status
git diff
review my changes
What does hello.py print?

Safety

MUBO restricts file operations to its workspace directory.

Some potentially dangerous terminal commands are blocked.

Git operations are used for inspecting the local repository. MUBO does not automatically push changes to GitHub.

Project Goal

MUBO was built as a practical project to explore how local AI models can be connected to real developer tools.

The focus is on keeping the system simple, understandable, and useful rather than building an unnecessarily complex multi-agent system.

Future Improvements

Possible future improvements include:

* Better semantic code retrieval
* More programming-language support
* Improved conversation memory
* Better error handling
* More advanced code review
* Additional developer tools
* Optional VS Code integration

Author

Sarbpreet Singh

BSc Computer Science student
University of Hertfordshire