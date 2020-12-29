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
from wilder.mgmt import get_mgmt
from wilder.server.error import MissingAlbumError
from wilder.server.error import MissingArtistError
from wilder.server.error import WildServerError
from wilder.server.error import WildServerFailureError
from wilder.server.logger import get_server_logger
from wilder.util import get_mgmt_json


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_unknown_errors(err):
    err = WildServerFailureError(str(err))
    response = jsonify(err.dict)
    return _set_response_from_wild_error(response, err)


@app.errorhandler(WildServerError)
def handle_server_errors(err):
    response = jsonify(err.dict())
    return _set_response_from_wild_error(response, err)


def _set_response_from_wild_error(response, err):
    response.status_code = err.status_code
    return response


@app.route(f"/{MGMT}")
def mgmt():
    return get_mgmt_json(as_dict=False)


@app.route(f"/{ARTISTS}", methods=["GET"])
def artists():
    _mgmt = get_mgmt()
    return {ARTISTS: [a.json for a in _mgmt.artists]}


@app.route(f"/{CREATE_ALBUM}", methods=["POST"])
def create_album():
    data = request.form
    _verify_create_album_request_data(data)
    _mgmt = get_mgmt()
    _mgmt.start_new_album(data[ARTIST], data[ALBUM])
    return _successful_response()


@app.route(f"/{SIGN}", methods=["POST"])
def sign():
    data = request.form
    _verify_present_artist(data)
    _mgmt = get_mgmt()
    _mgmt.sign_new_artist(data.get(ARTIST))
    return _successful_response()


@app.route(f"/{UNSIGN}", methods=["POST"])
def unsign():
    data = request.form
    _verify_present_artist(data)
    _mgmt = get_mgmt()
    _mgmt.unsign_artist(data.get(ARTIST))
    return _successful_response()


@app.route(f"/{DISCOGRAPHY}/<artist>", methods=["GET"])
def albums(artist):
    _mgmt = get_mgmt()
    artist = _mgmt.get_artist_by_name(artist)
    return {DISCOGRAPHY: [a.json for a in artist.discography]}


def _verify_create_album_request_data(data):
    _verify_present_artist(data)
    if not data.get(ALBUM):
        raise MissingAlbumError()


def _verify_present_artist(data):
    if not data.get(ARTIST):
        raise MissingArtistError()


def _successful_response():
    return {"status": "successful"}
