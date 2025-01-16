import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils import run_subprocess  # noqa
from config.logging import DEBUG, setup_logging  # noqa


def install_venv():
    logging.info("Setting up virtual environment...")
    if os.path.exists(".venv"):
        logging.info("Virtual environment already exists.")
        logging.info("Skipping virtual environment setup.")
        return
    return_code = run_subprocess("python -m venv .venv")
    if return_code:
        raise Exception("Failed to install virtual environment with venv")


def activate_venv():
    logging.info("Activating virtual environment...")
    if os.name == "nt":
        venv_path = ".venv/Scripts/activate"
    else:
        venv_path = ".venv/bin/activate"
    return_code = run_subprocess(f"source {venv_path}")
    if return_code:
        raise Exception("Failed to activate virtual environment")


def install_requirements():
    logging.info("Installing requirements...")
    return_code = run_subprocess("make install")
    if return_code:
        raise Exception("Failed to install requirements")


if __name__ == "__main__":
    setup_logging()

    try:
        install_venv()
        activate_venv()
        install_requirements()
        logging.info("Environment setup complete.")
    except Exception as e:
        logging.error(f"Environment setup failed: {e}")
        sys.exit(1)
