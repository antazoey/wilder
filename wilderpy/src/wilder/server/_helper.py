class HttpMethod:
    GET = "GET"
    POST = "POST"


class WildServerResponse:
    def __init__(self, error, message):
        self._error = error
        self._message = message

    @property
    def json(self):
        return {"error": self._error, "message": self._message}


def successful_response():
    return WildServerResponse(None, "successful")
