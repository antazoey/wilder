class WildClientError(Exception):
    """An error raises on the client."""


class WildHttpError(WildClientError):
    """An error raised when receiving an error response from the server."""

    def __init__(self, response):
        super().__init__(str(response))


class WildBadRequestError(WildHttpError):
    """An error returned when the client gets a 400 from the server."""


class WildNotFoundError(WildHttpError):
    """An error returned when the client gets a 404 from the server."""


class WildUnknownServerError(WildHttpError):
    """An error returned when the client gets a 500 from the server."""


class OperationNotPermittedError(WildClientError):
    """An error raised when an operation is not permitted for a client."""

    def __init__(self):
        msg = "This operation is for Wild servers only."
        super().__init__(msg)
