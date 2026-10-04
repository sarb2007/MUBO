from .file_tools import list_files, read_file, write_file, search_code
from .terminal_tools import run_command, run_tests, git_status, git_diff, git_log, git_show
from .ai import ask_local_ai

pending_edit = None
def handle_request(message):
    """Decide which workspace tool is needed."""

    message_lower = message.lower()
    global pending_edit

    if message_lower == "approve":

        if pending_edit is None:
            return "There is no pending edit."

        try:
            file_path = pending_edit["file_path"]
            content = pending_edit["content"]

            result = write_file(file_path, content)

            pending_edit = None

            return result

        except Exception as error:
            return str(error)


    if message_lower == "reject":

        if pending_edit is None:
            return "There is no pending edit."

        file_path = pending_edit["file_path"]

        pending_edit = None

        return f"Edit for {file_path} rejected."

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

    if message_lower.startswith("edit "):
        request = message[5:].strip()

        if ":" not in request:
            return "Use this format: edit filename.py: describe the change"

        file_path, instruction = request.split(":", 1)

        file_path = file_path.strip()
        instruction = instruction.strip()

        try:
            current_code = read_file(file_path)

            prompt = (
                "You are editing a source code file.\n"
                "Modify the code according to the user's instruction.\n"
                "Return ONLY the complete updated file content.\n"
                "Do not use markdown code fences.\n"
                "Do not explain anything.\n\n"
                f"FILE: {file_path}\n\n"
                f"CURRENT CODE:\n{current_code}\n\n"
                f"USER INSTRUCTION:\n{instruction}"
            )

            updated_code = ask_local_ai(prompt, max_tokens=1000)
            

            pending_edit = {
                "file_path": file_path,
                "content": updated_code.strip()
            }

            return (
                f"Proposed changes for {file_path}:\n\n"
                f"{updated_code.strip()}\n\n"
                "⚠️ File has NOT been changed yet.\n"
                "Type 'approve' to apply or 'reject' to cancel."
            )

        except Exception as error:
            return str(error)

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

    if message_lower in ["git log", "log"]:
        try:
            result = git_log()

            if result["return_code"] == 0:
                return result["output"] or "No commits found."

            return result["error"] or "Git log failed."

        except Exception as error:
            return str(error)

    if message_lower in ["git show", "show commit"]:
        try:
            result = git_show()

            if result["return_code"] == 0:
                return result["output"] or "No commit found."

            return result["error"] or "Git show failed."

        except Exception as error:
            return str(error)

    if message_lower in ["review my changes", "review changes", "code review"]:
        try:
            result = git_diff()

            if result["return_code"] != 0:
                return result["error"] or "Could not get Git changes."

            if not result["output"]:
                return "There are no code changes to review."

            prompt = (
                "You are reviewing a Git diff from a Python software project.\n"
                "Only discuss issues that are directly supported by the diff.\n"
                "Do not invent files, code, or problems that are not shown.\n"
                "If the code looks correct, say so.\n"
                "Focus on real bugs, security risks, and practical improvements.\n"
                "Keep the review concise and explain why each issue matters.\n\n"
                f"GIT DIFF:\n{result['output']}"
            )

            return ask_local_ai(prompt, max_tokens=500)

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