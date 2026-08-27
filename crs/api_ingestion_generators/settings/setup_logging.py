import logging
import sys


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return the application logger.
    """

    logger = logging.getLogger()
    logger.setLevel(level)

    # Avoid adding duplicate handlers if setup_logging()
    # is called multiple times.
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger