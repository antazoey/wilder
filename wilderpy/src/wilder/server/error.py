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
        rv["message"] = self.message
        return rv


class WildBadRequestError(WildServerError):
    def __init__(self, message, payload=None):
        WildServerError.__init__(self, 400, message, payload)
        

class WildNotFoundError(WildServerError):
    """A base error for when a resource is not found."""
    def __init__(self, message, payload=None):
        WildServerError.__init__(self, 404, message, payload)


class WildServerFailureError(WildServerError):
    def __init__(self, err_str):
        WildServerError.__init__(self, 500, f"{UNKNOWN_ERROR}: {str(err_str)}")


class MissingArtistError(WildBadRequestError):
    def __init__(self):
        WildBadRequestError.__init__(self, "MISSING_ARTIST")


class MissingAlbumError(WildBadRequestError):
    def __init__(self):
        WildBadRequestError.__init__(self, "MISSING_ALBUM")
