from flask import Flask
from flask import jsonify
from flask import request
from wilder.constants import ALBUM
from wilder.constants import ARTIST
from wilder.constants import ARTISTS
from wilder.constants import CREATE_ALBUM
from wilder.constants import DISCOGRAPHY
from wilder.constants import MGMT
from wilder.constants import SIGN
from wilder.constants import UNSIGN
from wilder.errors import WildError
from wilder.errors import WildNotFoundError
from wilder.mgmt import get_mgmt
from wilder.server.error import MissingAlbumError, UNKNOWN_ERROR, WildBadRequestError
from wilder.server.error import MissingArtistError
from wilder.server.error import WildServerError
from wilder.server.error import WildServerFailureError
from wilder.server.error import WildNotFoundError as WilderHttpNotFoundError
from wilder.server.logger import get_server_logger
from wilder.util import get_mgmt_json

app = Flask(__name__)


class HttpMethod: 
    GET = "GET"
    POST = "POST"


@app.errorhandler(Exception)
def handle_unknown_errors(err):
    err = WildServerFailureError(str(err))
    response = jsonify(err.dict)
    return _set_response_from_wild_error(response, err)


@app.errorhandler(WildServerError)
def handle_server_errors(err):
    response = jsonify(err.dict)
    return _set_response_from_wild_error(response, err)


@app.errorhandler(WildNotFoundError)
def handle_not_found_wild_errors(err):
    response = jsonify({"Error": str(err)})
    err = WilderHttpNotFoundError(str(err))
    return _set_response_from_wild_error(response, err)


@app.errorhandler(WildError)
def handle_wild_errors(err):
    response = jsonify({"Error": str(err)})
    err = WildBadRequestError(str(err))
    return _set_response_from_wild_error(response, err)


def _set_response_from_wild_error(response, err):
    response.status_code = err.status_code
    response.text = str(err) or UNKNOWN_ERROR
    return response


@app.route(f"/{MGMT}")
def mgmt():
    return get_mgmt_json(as_dict=False)


@app.route(f"/{ARTISTS}", methods=[HttpMethod.GET])
def artists():
    _mgmt = get_mgmt()
    _artists = _mgmt.get_artists()
    return {ARTISTS: [a.json for a in _artists]}


@app.route(f"/{CREATE_ALBUM}", methods=[HttpMethod.POST])
def create_album():
    _verify_data_present(request.json_module, [ARTIST, ALBUM])
    _mgmt = get_mgmt()
    artist = request.json.get(ARTIST)
    album = request.json.get(ALBUM)
    _mgmt.start_new_album(artist, album)
    return _successful_response()


@app.route(f"/{SIGN}", methods=[HttpMethod.POST])
def sign():
    _json = request.json
    artist = _json.get(ARTIST)
    _verify_data_present(artist)
    _mgmt = get_mgmt()
    _mgmt.sign_new_artist(artist)
    return _successful_response()


@app.route(f"/{UNSIGN}", methods=[HttpMethod.POST])
def unsign():
    _json = request.json
    artist = _json.get(ARTIST)
    _verify_data_present(artist)
    _mgmt = get_mgmt()
    _mgmt.unsign_artist(artist)
    return _successful_response()


@app.route(f"/{DISCOGRAPHY}/<artist>", methods=[HttpMethod.GET])
def albums(artist):
    _mgmt = get_mgmt()
    artist = _mgmt.get_artist_by_name(artist)
    return {DISCOGRAPHY: [a.json for a in artist.discography]}
    

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
