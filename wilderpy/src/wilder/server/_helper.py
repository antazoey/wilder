class HttpMethod:
    GET = "GET"
    POST = "POST"


ERROR_KEY = "error"
MESSAGE_KEY = "message"


def error_response(message, err):
    return _response(message, err=err)


def successful_response():
    return _response("successful")


def _response(message, err=None):
    return {ERROR_KEY: err, MESSAGE_KEY: message}
