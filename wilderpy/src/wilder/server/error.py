class ShortErrorMessages:
    UNKNOWN = "UNKNOWN"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"


class WildServerError(Exception):
    def __init__(self, status_code, message, payload=None):
        self.status_code = status_code
        self.message = message
        self.payload = payload
        super().__init__(message)

    @property
    def dict(self):
        rv = dict(self.payload or ())
        rv["error"] = ShortErrorMessages.UNKNOWN
        rv["message"] = self.message
        return rv


def get_response_error_data(msg):
    msg = msg.lower()
    if "bad request" in msg:
        return 400, ShortErrorMessages.BAD_REQUEST
    elif "not found" in msg:
        return 404, ShortErrorMessages.NOT_FOUND
    elif "method not allowed" in msg:
        return 405, ShortErrorMessages.METHOD_NOT_ALLOWED
    return 500, ShortErrorMessages.UNKNOWN
