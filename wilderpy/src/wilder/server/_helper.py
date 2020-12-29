class HttpMethod:
    GET = "GET"
    POST = "POST"


def _verify_data_present(data, keys=None):
    if not data:
        raise MissingArtistError()

    if isinstance(data, str):
        return

    for key in keys:
        if key and not data.get(key):
            raise MissingArtistError()


def _successful_response():
    return {"status": "successful"}
