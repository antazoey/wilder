UNKNOWN_ERROR = "UNKNOWN_ERROR"


class WildServerError(Exception):
    def __init__(self, status_code, message, payload=None):
        self.status_code = status_code
        self.message = message
        self.payload = payload
        Exception.__init__(self, message)

    @property
    def dict(self):
        rv = dict(self.payload or ())
        rv["error"] = "UNKNOWN"
        rv["message"] = self.message
        return rv
