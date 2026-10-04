from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .file_tools import list_files, read_file, write_file, search_code
from .agent import handle_request
from .ai import ask_local_ai
from .memory import create_memory_table, save_memory, get_recent_memories
from .rag import build_code_context

app = FastAPI()
create_memory_table()


class ChatRequest(BaseModel):
    message: str

class WriteFileRequest(BaseModel):
    file_path: str
    content: str



@app.post("/api/chat")
def chat(request: ChatRequest):

    # First check whether MUBO needs to use a workspace tool.
    tool_result = handle_request(request.message)

    if tool_result is not None:
        save_memory(request.message, tool_result)

        return {
            "response": tool_result
        }

    # Get recent conversations.
    memories = get_recent_memories(5)

    # Get relevant code from the workspace.
    code_context = build_code_context(request.message)

    prompt_parts = []

    if memories:
        memory_text = "\n\n".join(
            f"User: {user_message}\n"
            f"MUBO: {assistant_response}"
            for user_message, assistant_response in reversed(memories)
        )

        prompt_parts.append(
            "Previous conversation:\n"
            f"{memory_text}"
        )

    if code_context:
        prompt_parts.append(
            "Relevant workspace code:\n"
            f"{code_context}"
        )

    prompt_parts.append(
        "Current user question:\n"
        f"{request.message}"
    )

    prompt_parts.append(
        "Answer the current question directly. "
        "Use the previous conversation and workspace code "
        "only when relevant. "
        "Do not invent code or previous conversations."
    )

    prompt = "\n\n".join(prompt_parts)

    # Ask the local AI.
    answer = ask_local_ai(prompt)

    # Save the conversation.
    save_memory(request.message, answer)

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