from flask import Flask
from flask import jsonify
from flask import request
from wilder import get_mgmt
from wilder import get_mgmt_json
from wilder.constants import ARTISTS
from wilder.server.error import MissingAlbumError
from wilder.server.error import MissingArtistError
from wilder.server.error import WildServerError
from wilder.server.error import WildServerFailureError
from wilder.server.logger import get_server_logger


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


@app.route("/")
def mgmt():
    return get_mgmt_json(as_dict=False)


@app.route("/artists", methods=["GET"])
def artists():
    _mgmt = get_mgmt()
    return {ARTISTS: [a.json for a in _mgmt.artists]}


@app.route("/sign", methods=["POST"])
def sign():
    data = request.form
    _verify_sign_request_data(data)
    _mgmt = get_mgmt()
    _mgmt.start_new_album(data["artist"], data["album"])
    return {"status": "successful"}


@app.route("/discography/<artist>", methods=["GET"])
def albums(artist):
    _mgmt = get_mgmt()
    artist = _mgmt.get_artist_by_name(artist)
    return {"discography": [a.json for a in artist.discography]}


def _verify_sign_request_data(data):
    if not data.get("artist"):
        raise MissingArtistError()
    if not data.get("albums"):
        raise MissingAlbumError()
