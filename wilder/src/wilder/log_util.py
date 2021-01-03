import logging
import os
from logging.handlers import RotatingFileHandler

from wilder.util import get_project_path
from wilder.constants import Constants


def create_error_file_handler(log_path=None):
    log_path = log_path or get_error_log_path()
    return RotatingFileHandler(
        log_path, maxBytes=250000000, encoding="utf-8", delay=True
    )


def get_error_log_path(base_path=None, proj_suffix=None):
    log_path = base_path or get_project_path("log")
    proj_prefix = Constants.WILDER
    proj_suffix = proj_suffix or ""
    return os.path.join(log_path, f"{proj_prefix}-{proj_suffix}.log")


def logger_has_handlers(logger):
    return len(logger.handlers)


def create_formatter_for_error_file():
    return logging.Formatter("%(asctime)s %(message)s")


def add_handler_to_logger(logger, handler, formatter):
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
