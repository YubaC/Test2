import logging
import os

DEBUG = (
    os.environ.get("DEBUG", "False").lower() == "true"
    or os.environ.get("RUNNER_DEBUG") == "1"
)
LEVEL = logging.DEBUG if DEBUG else logging.INFO


class LoggingFormatter(logging.Formatter):
    """Custom logging formatter.

    Args:
        logging (module): The logging module.

    Returns:
        logging.Formatter: A custom logging formatter.
    """

    # ANSI 转义码颜色配置
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }
    RESET = "\033[0m"  # Reset to default color

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}[{record.levelname.capitalize()}]{self.RESET}"
        return super().format(record)


def setup_logging():
    """Configure log format and processor."""
    handler = logging.StreamHandler()
    handler.setFormatter(LoggingFormatter(fmt="%(levelname)s %(message)s"))

    logging.basicConfig(level=LEVEL, handlers=[handler])
