import logging
import os
import shutil
import sys

import pathspec

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging import setup_logging  # noqa

PATTERNS_TO_CLEAN = [
    "__blobstorage__/",
    "**/__pycache__/",
    "__queuestorage__/",
    ".mypy_cache/",
    ".pytest_cache/",
    "reports/",
    "build/",
    "dist/",
    "__azurite_db_*.json",
    ".coverage",
    "!.venv/",
]


def delete_files(files, root, spec):
    """Delete files that match the given pattern.

    Args:
        files (list): A list of file names.
        root (str): The root directory.
        spec (pathspec.PathSpec): The pathspec object.
    """
    for filename in files:
        file_path = os.path.relpath(os.path.join(root, filename), ".")
        if not spec.match_file(file_path):
            continue

        try:
            os.remove(os.path.join(root, filename))
            logging.debug(f"Deleted file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to delete file {file_path}: {e}")


def delete_dirs(dirs, root, spec):
    """Delete directories that match the given pattern.

    Args:
        dirs (list): A list of directory names.
        root (str): The root directory.
        spec (pathspec.PathSpec): The pathspec object.
    """
    for dirname in dirs:
        dir_path = os.path.relpath(os.path.join(root, dirname), ".")
        if not spec.match_file(dir_path + "/"):
            continue

        try:
            shutil.rmtree(os.path.join(root, dirname))
            logging.debug(f"Deleted directory: {dir_path}")
        except Exception as e:
            logging.error(f"Failed to delete directory {dir_path}: {e}")


def clean(patterns):
    """
    Clean up the project directories,
    using the same patterns as .gitignore (gitwildmatch).

    Args:
        patterns (list): A list of patterns to match.
    """
    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)

    for root, dirs, files in os.walk(".", topdown=False):
        delete_files(files, root, spec)
        delete_dirs(dirs, root, spec)


if __name__ == "__main__":
    setup_logging()

    clean(PATTERNS_TO_CLEAN)
    logging.info("Cleaned up the project directories.")
