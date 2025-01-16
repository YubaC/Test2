import sys
import subprocess
import platform


DANGER = "\033[91m"
SUCCESS = "\033[92m"
WARN = "\033[93m"
INFO = "\033[94m"
RESET = "\033[0m"


def install_dependencies(requirements_path):
    """Install dependencies from a requirements file.

    Args:
        requirements_path (str): The path to the requirements file.
    """
    cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_path]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to install dependencies: {result.stderr}")


def main():
    if len(sys.argv) < 2:
        print("Usage: setup_env.py <requirements-file-path>")
        sys.exit(1)

    requirements_file = sys.argv[1]

    try:
        print(f"Installing dependencies from {requirements_file} ...")
        install_dependencies(requirements_file)
        print("Dependencies installed successfully.")

        print()
        system_name = platform.system().lower()
        if system_name.startswith("win"):
            print(f"{SUCCESS}Environment setup complete!{RESET}")
            print("Remember to activate your venv with: .venv\\Scripts\\activate")
        else:
            print("Remember to activate your venv with: source .venv/bin/activate")

        print(
            "You can also visit https://code.visualstudio.com/docs/python/environments#_working-with-python-interpreters to set up your Python interpreter in VS Code."
        )
    except Exception as e:
        print(f"{DANGER}Failed to install dependencies: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
