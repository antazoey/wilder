import logging
from threading import Lock

from log_util import add_handler_to_logger
from log_util import create_error_file_handler
from log_util import create_formatter_for_error_file
from log_util import get_error_log_path
from log_util import logger_has_handlers
from wilder.util import get_project_path

logger_deps_lock = Lock()


def get_server_logger():
    """Gets the logger where raw exceptions are logged."""
    logger = logging.getLogger("wilder_server_logger")
    if logger_has_handlers(logger):
        return logger

    with logger_deps_lock:
        if not logger_has_handlers(logger):
            formatter = create_formatter_for_error_file()
            base_path = get_project_path("log")
            err_log_path = get_error_log_path(base_path=base_path, proj_suffix="server")
            handler = create_error_file_handler(log_path=err_log_path)
            return add_handler_to_logger(logger, handler, formatter)
    return logger
