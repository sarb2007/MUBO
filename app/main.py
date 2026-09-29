from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

from .file_tools import list_files, read_file, write_file, search_code
from .agent import handle_request

app = FastAPI()


class ChatRequest(BaseModel):
    message: str

class WriteFileRequest(BaseModel):
    file_path: str
    content: str

def ask_local_ai(message: str) -> str:
    """Send a message to the local model running in LM Studio."""

    url = "http://127.0.0.1:1234/v1/chat/completions"

    data = {
        "model": "local-model",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are MUBO, a local AI coding assistant. "
                    "Keep answers short, clear, and practical. "
                    "For simple questions, answer in 2-5 sentences. "
                    "Only give detailed explanations when the user asks for them."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        "temperature": 0.2,
        "max_tokens": 250,
    }

    response = requests.post(url, json=data)

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


@app.post("/api/chat")
def chat(request: ChatRequest):

    # First check whether MUBO needs to use a workspace tool.
    tool_result = handle_request(request.message)

    if tool_result is not None:
        return {
            "response": tool_result
        }

    # If no tool is needed, ask the local AI normally.
    answer = ask_local_ai(request.message)

    return {
        "response": answer
    }

@app.get("/api/files")
def get_files():
    """Return the files inside the MUBO workspace."""

    return {
        "files": list_files()
    }

@app.get("/api/files/{file_path:path}")
def get_file(file_path: str):
    """Return the contents of a file."""

    return {
        "file": file_path,
        "content": read_file(file_path)
    }

@app.post("/api/files")
def create_file(request: WriteFileRequest):
    """Create or update a file inside the workspace."""

    result = write_file(
        request.file_path,
        request.content
    )

    return {
        "message": result
    }

@app.get("/api/search")
def search_files(query: str):
    """Search for text inside workspace files."""

    return {
        "query": query,
        "results": search_code(query)
    }

# Serve the MUBO web interface.
app.mount("/", StaticFiles(directory="web", html=True), name="web")