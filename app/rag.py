from .file_tools import search_code, read_file


CODE_KEYWORDS = [
    "code",
    "function",
    "class",
    "variable",
    "bug",
    "error",
    "print",
    "import",
    "file",
    "python",
]


def retrieve_file(file_name):
    """Retrieve the contents of a specific file."""

    try:
        return read_file(file_name)
    except Exception:
        return ""


def retrieve_code(query, limit=5):
    """Find relevant code from the workspace."""

    results = search_code(query)

    return results[:limit]


def build_code_context(query):
    """Build useful code context for the AI."""

    words = query.split()

    # Check whether the user mentioned a specific file.
    for word in words:
        if word.endswith((".py", ".js", ".html", ".css", ".json")):

            content = retrieve_file(word)

            if content:
                return f"File: {word}\n\n{content}"

    # Search the workspace for code-related questions.
    query_lower = query.lower()

    if any(keyword in query_lower for keyword in CODE_KEYWORDS):

        results = retrieve_code(query)

        if results:
            context = []

            for result in results:
                context.append(
                    f"File: {result['file']}\n"
                    f"Line {result['line']}: {result['text']}"
                )

            return "\n\n".join(context)

    return ""


