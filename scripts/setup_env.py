import logging
import os
import platform
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils import run_subprocess  # noqa
from config.logging import DEBUG, setup_logging  # noqa


def install_venv():
    """
    Create a virtual environment (.venv directory) if it doesn't exist.
    """
    if os.path.exists(".venv"):
        logging.info("Virtual environment already exists. Skipping creation.")
        return

    logging.info("Creating virtual environment...")
    return_code = run_subprocess("python -m venv .venv")
    if return_code:
        raise Exception(
            (
                "Failed to create virtual environment. "
                "Please check your Python installation and permissions."
            )
        )


def activate_and_install():
    """
    Activate the virtual environment and run 'make install' within the same subprocess.
    """
    logging.info("Activating virtual environment and installing dependencies...")

    if platform.system().lower().startswith("win"):
        # For Windows (using cmd)
        command = (
            'powershell -Command "& { . .venv\\Scripts\\Activate.ps1; make install }"'
        )
    else:
        # For Unix-like systems (Linux, macOS)
        command = 'bash -c "' "source .venv/bin/activate && " 'make install"'

    return_code = run_subprocess(command)
    if return_code:
        raise Exception(
            "Failed to activate virtual environment and install dependencies."
        )


if __name__ == "__main__":
    setup_logging()
    try:
        install_venv()
        activate_and_install()
        logging.info("Environment setup complete.")

        active_cmd = "source .venv/bin/activate"
        if platform.system().lower().startswith("win"):
            active_cmd = ".venv\\Scripts\\Activate.ps1"
        logging.info(
            f'You can now activate the virtual environment by running "{active_cmd}".'
        )
    except Exception as e:
        logging.error(f"Environment setup failed: {e}")
        sys.exit(1)
