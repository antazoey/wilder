import logging
import traceback
from threading import Lock

from wilder.util.logging import add_handler_to_logger
from wilder.util.logging import create_error_file_handler
from wilder.util.logging import create_formatter_for_error_file
from wilder.util.logging import get_error_log_path
from wilder.util.logging import logger_has_handlers
from wilder.cli.util import get_user_project_path

# prevent loggers from printing stacks to stderr if a pipe is broken
logging.raiseExceptions = False

logger_deps_lock = Lock()


def _create_error_file_handler():
    log_path = get_cli_error_log_path()
    return create_error_file_handler(log_path=log_path)


def get_cli_error_log_path():
    log_path = get_user_project_path("log")
    return get_error_log_path(base_path=log_path, proj_suffix="cli")


def _get_error_file_logger():
    """Gets the logger where raw exceptions are logged."""
    logger = logging.getLogger("code42_error_logger")
    if logger_has_handlers(logger):
        return logger

    with logger_deps_lock:
        if not logger_has_handlers(logger):
            formatter = create_formatter_for_error_file()
            handler = _create_error_file_handler()
            return add_handler_to_logger(logger, handler, formatter)
    return logger


def get_view_error_details_message():
    """Returns the error message that is printed when errors occur."""
    return "View details using the command `wild logs`."


class CliLogger:
    def __init__(self):
        self._logger = _get_error_file_logger()

    def log_error(self, err):
        message = str(err) if err else None
        if message:
            self._logger.error(message)

    def log_verbose_error(self, invocation_str=None, http_request=None):
        """For logging traces, invocation strs, and request parameters during exceptions to the
        error log file."""
        prefix = (
            "Exception occurred."
            if not invocation_str
            else "Exception occurred from input: '{}'.".format(invocation_str)
        )
        message = "{}. See error below.".format(prefix)
        self.log_error(message)
        self.log_error(traceback.format_exc())
        if http_request:
            self.log_error("Request parameters: {}".format(http_request.body))


def get_main_cli_logger():
    return CliLogger()
