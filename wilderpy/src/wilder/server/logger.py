import os
import logging
from threading import Lock

from logging.handlers import RotatingFileHandler
from wilder.util import get_project_path


logger_deps_lock = Lock()
ERROR_LOG_FILE_NAME = "wilder_errors.log"


def get_error_file_logger():
    """Gets the logger where raw exceptions are logged."""
    logger = logging.getLogger("code42_error_logger")
    if logger_has_handlers(logger):
        return logger

    with logger_deps_lock:
        if not logger_has_handlers(logger):
            formatter = create_formatter_for_error_file()
            handler = create_error_file_handler()
            return add_handler_to_logger(logger, handler, formatter)
    return logger


def create_error_file_handler(log_path=None):
    log_path = log_path or get_error_log_path()
    return RotatingFileHandler(
        log_path, maxBytes=250000000, encoding="utf-8", delay=True
    )


def get_error_log_path(base_path=None):
    log_path = base_path or get_project_path("log")
    return os.path.join(log_path, ERROR_LOG_FILE_NAME)


def logger_has_handlers(logger):
    return len(logger.handlers)


def create_formatter_for_error_file():
    return logging.Formatter("%(asctime)s %(message)s")


def add_handler_to_logger(logger, handler, formatter):
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
