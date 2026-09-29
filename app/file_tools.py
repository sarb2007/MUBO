from pathlib import Path


# The folder MUBO is allowed to work inside.
WORKSPACE = Path("workspace").resolve()


def list_files():
    """Return all files inside the MUBO workspace."""

    files = []

    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(WORKSPACE)))

    return files


def read_file(file_path):
    """Read a file from the MUBO workspace."""

    path = (WORKSPACE / file_path).resolve()

    # Prevent MUBO from accessing files outside the workspace.
    if not path.is_relative_to(WORKSPACE):
        raise ValueError("File is outside the workspace.")

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    return path.read_text(encoding="utf-8")

def write_file(file_path, content):
    """Write content to a file inside the MUBO workspace."""

    path = (WORKSPACE / file_path).resolve()

    # Prevent MUBO from writing outside the workspace.
    if not path.is_relative_to(WORKSPACE):
        raise ValueError("File is outside the workspace.")

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content, encoding="utf-8")

    return f"File written: {file_path}"

def search_code(query):
    """Search for text inside files in the workspace."""

    results = []

    for path in WORKSPACE.rglob("*"):
        if not path.is_file():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            if query.lower() in line.lower():
                relative_path = path.relative_to(WORKSPACE)

                results.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "text": line.strip()
                })

    return results

if __name__ == "__main__":
    print(list_files())

    print(read_file("test.py"))

    print(write_file(
        "hello.py",
        'print("Hello from MUBO!")'
    ))

    print(search_code("MUBO"))