from .file_tools import list_files, read_file, write_file, search_code
from .terminal_tools import run_command, run_tests, git_status, git_diff

def handle_request(message):
    """Decide which workspace tool is needed."""

    message_lower = message.lower()

    if "what files" in message_lower or "list files" in message_lower:
        files = list_files()

        return "Files in the workspace:\n" + "\n".join(files)

    if message_lower.startswith("read "):
        file_path = message[5:].strip()

        try:
            content = read_file(file_path)
            return f"Contents of {file_path}:\n\n{content}"
        except Exception as error:
            return str(error)

    if message_lower.startswith("search "):
        query = message[7:].strip()

        results = search_code(query)

        if not results:
            return "No matches found."

        lines = []

        for result in results:
            lines.append(
                f"{result['file']}:{result['line']} - {result['text']}"
            )

        return "\n".join(lines)

    if message_lower.startswith("write "):
        request = message[6:].strip()

        if ":" not in request:
            return "Use this format: write filename.py: your code"

        file_path, content = request.split(":", 1)

        try:
            return write_file(
                file_path.strip(),
                content.strip()
            )
        except Exception as error:
            return str(error)

    if message_lower in ["git status", "status"]:
        try:
            result = git_status()

            if result["return_code"] == 0:
                return result["output"] or "Working tree is clean."

            return result["error"] or "Git status failed."

        except Exception as error:
            return str(error)

    if message_lower in ["git diff", "diff"]:
        try:
            result = git_diff()

            if result["return_code"] == 0:
                return result["output"] or "No changes found."

            return result["error"] or "Git diff failed."

        except Exception as error:
            return str(error)

    if message_lower in ["run tests", "run test"]:
        try:
            result = run_tests()

            if result["return_code"] == 0:
                return result["output"]

            return result["error"] or result["output"]

        except Exception as error:
            return str(error)

    if message_lower.startswith("run "):
        command = message[4:].strip()

        try:
            result = run_command(command)

            if result["return_code"] == 0:
                return result["output"] or "Command completed successfully."

            return result["error"] or "Command failed."

        except Exception as error:
            return str(error)




    return None