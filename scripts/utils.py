import logging
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging import DEBUG  # noqa

# If system is Windows, we can use `python` to run the command
# In Unix-like systems, we need to use `python3` instead
PY_CMD = "python" if os.name == "nt" else "python3"


def run_subprocess(command, output=True):
    """Run a subprocess command.

    Args:
        command (str): The command to run.

    Returns:
        int: The return code of the subprocess.
    """
    logging.debug(f"Running subprocess command: {command}")

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except Exception as e:
        if isinstance(e, OSError):
            logging.error(f"Failed to start subprocess due to OS error: {e}")
        else:
            logging.error(f"Failed to start subprocess: {e}")
        return 1

    if process.poll() is not None:
        logging.error("Subprocess failed to start: %s", process.poll())
        return process.poll()

    # Stream the subprocess output in real time
    for line in process.stdout:
        if output:
            print(line)
        elif DEBUG:
            logging.debug(line.strip("\n"))

    process.wait()
    return process.returncode
