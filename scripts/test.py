import argparse
import logging
import os
import shutil
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging import setup_logging  # noqa

OUTPUT_DIR = "reports"

ARGUMENTS_DEFINTION = [
    {
        "flags": ["-r", "--report"],
        "kwargs": {"action": "store_true", "help": "Request a HTML report"},
    },
]

PYTEST_ARGS = ["pytest"]
PYTEST_ARGS_REPORT = PYTEST_ARGS + [
    f"--cov-report=html:{OUTPUT_DIR}/coverage",
    f"--alluredir={OUTPUT_DIR}/allure-results",
]


def parse_args():
    """Parse the command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Process some arguments.")
    for arg in ARGUMENTS_DEFINTION:
        parser.add_argument(*arg["flags"], **arg["kwargs"])

    return parser.parse_args()


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
    except OSError as e:
        logging.error(f"Failed to start subprocess due to OS error: {e}")
        return 1

    if process.poll() is not None:
        logging.error("Subprocess failed to start: %s", process.poll())
        return process.poll()

    # Stream the subprocess output in real time
    if output:
        for line in process.stdout:
            logging.info(line.strip("\n"))

    process.wait()
    return process.returncode


def clean_output():
    """Clean the output directory."""
    logging.debug(f"Cleaning output directory: {OUTPUT_DIR}")
    try:
        shutil.rmtree(OUTPUT_DIR)
    except FileNotFoundError:
        pass
    os.makedirs(OUTPUT_DIR)


def convert_to_html():
    """Convert the pytest report to Allure format."""
    logging.debug("Converting pytest report to HTML through Allure...")
    return_code = run_subprocess(
        [
            "allure",
            "generate",
            f"{OUTPUT_DIR}/allure-results",
            "-o",
            f"{OUTPUT_DIR}/test",
        ],
        False,
    )
    if return_code:
        shutil.rmtree(OUTPUT_DIR)
        raise Exception(
            "Failed to generate report. This is likely due to missing Allure CLI."
        )
    shutil.rmtree(f"{OUTPUT_DIR}/allure-results")


def run_tests(args):
    """Run the tests.

    Args:
        args (argparse.Namespace): The parsed arguments.
    """
    if not args.report:
        logging.debug("Running tests...No report requested.")
        try:
            return_code = run_subprocess(PYTEST_ARGS)
        except Exception as e:
            logging.error(f"Failed to run tests: {e}")
            sys.exit(1)

        return return_code

    logging.debug(
        f"Running tests...Report requested, and will be saved to dir {OUTPUT_DIR}."
    )
    clean_output()
    try:
        return_code = run_subprocess(" ".join(PYTEST_ARGS_REPORT))
    except Exception as e:
        logging.error(f"Failed to run tests: {e}")
        sys.exit(1)

    logging.debug("Tests complete.")
    logging.debug("Converting to HTML...")

    convert_to_html()
    logging.debug("Conversion complete.")

    logging.info(f'Report saved to directory "{OUTPUT_DIR}".')
    logging.info("Both test and coverage reports are available.")

    return return_code


if __name__ == "__main__":
    setup_logging()

    try:
        args = parse_args()
        return_code = run_tests(args)
        if return_code:
            raise Exception(f"Tests failed with return code {return_code}")
    except Exception as e:
        logging.error(f"Failed to run tests: {e}")
        sys.exit(1)
