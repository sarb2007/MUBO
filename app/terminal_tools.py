import subprocess


# Commands that MUBO should never run.
BLOCKED_COMMANDS = [
    "rm",
    "sudo",
    "shutdown",
    "reboot",
    "mkfs",
    "dd",
]


def run_command(command):
    """Run a safe command inside the MUBO workspace."""

    command_name = command.strip().split()[0]

    if command_name in BLOCKED_COMMANDS:
        return {
            "command": command,
            "return_code": 1,
            "output": "",
            "error": "This command is blocked for safety."
        }

    result = subprocess.run(
        command,
        shell=True,
        cwd="workspace",
        capture_output=True,
        text=True,
        timeout=30
    )

    return {
        "command": command,
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr
    }

def run_tests():
    """Run the project's Python tests."""

    result = subprocess.run(
        "python -m pytest",
        shell=True,
        cwd="workspace",
        capture_output=True,
        text=True,
        timeout=30
    )

    return {
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr
    }

def git_status():
    """Show the current Git status."""

    result = subprocess.run(
        "git status --short",
        shell=True,
        cwd="workspace",
        capture_output=True,
        text=True,
        timeout=30
    )

    return {
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr
    }


def git_diff():
    """Show the current Git changes."""

    result = subprocess.run(
        "git diff",
        shell=True,
        cwd="workspace",
        capture_output=True,
        text=True,
        timeout=30
    )

    return {
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr
    }

if __name__ == "__main__":
    result = run_command("python test.py")
    print(result)