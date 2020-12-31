from flask import Flask
from flask import jsonify
from flask import request
from wilder.constants import Constants as Consts
from wilder.errors import WildError
from wilder.errors import WildNotFoundError as WildCoreNotFoundError
from wilder.mgmt import get_mgmt
from wilder.server._helper import HttpMethod
from wilder.server._helper import successful_response
from wilder.server.error import WildServerError
from wilder.util import get_mgmt_json


app = Flask(__name__)


"""**************"""
"""Error handlers"""
"""**************"""


@app.errorhandler(WildCoreNotFoundError)
def handle_not_found_wild_errors(err):
    response = jsonify({"error": "NOT_FOUND", "message": str(err)})
    response.status_code = 404
    return response


@app.errorhandler(WildServerError)
@app.errorhandler(Exception)
def handle_server_errors(err):
    msg = str(err)
    response = (
        jsonify(err.dict)
        if hasattr(err, "json")
        else jsonify({"error": "UNKNOWN", "message": msg})
    )
    response.status_code = _get_status_code(msg)
    return response


def _get_status_code(msg):
    msg = msg.lower()
    if "bad request" in msg:
        return 400
    elif "not found" in msg:
        return 404
    return 500


@app.errorhandler(WildError)
def handle_wild_errors(err):
    response = jsonify({"error": "BAD_REQUEST", "message": str(err)})
    response.status_code = 400
    return response


"""******"""
"""MGMT"""
"""******"""


@app.route(f"/{Consts.MGMT}")
def mgmt():
    """Get full MGMT JSON"""
    return get_mgmt_json(as_dict=False)


"""******"""
"""ARTIST"""
"""******"""


@app.route(f"/{Consts.ARTISTS}", methods=[HttpMethod.GET])
def artists():
    """Get all artists"""
    _mgmt = get_mgmt()
    _artists = _mgmt.get_artists()
    return {Consts.ARTISTS: [a.json for a in _artists]}


@app.route(f"/{Consts.SIGN}", methods=[HttpMethod.POST])
def sign():
    """Sign a new artist"""
    _artist = _get_request_param(Consts.ARTIST)
    _mgmt = get_mgmt()
    _mgmt.sign_new_artist(_artist)
    return successful_response()


@app.route(f"/{Consts.UNSIGN}", methods=[HttpMethod.POST])
def unsign():
    """Remove a managed artist"""
    _artist = _get_request_param(Consts.ARTIST)
    _mgmt = get_mgmt()
    _mgmt.unsign_artist(_artist)
    return successful_response()


@app.route(f"/<artist>/{Consts.UPDATE}", methods=[HttpMethod.POST])
def update_artist(artist):
    _mgmt = get_mgmt()
    _bio = _get_request_param(Consts.BIO)
    _mgmt.update_artist(artist, _bio)
    return successful_response()


@app.route(f"/{Consts.FOCUS}", methods=[HttpMethod.POST, HttpMethod.GET])
def focus():
    _mgmt = get_mgmt()
    if request.method == HttpMethod.POST:
        _artist_name = _get_request_param(Consts.ARTIST)
        _mgmt.focus_on_artist(_artist_name)
        return successful_response()
    else:
        _artist = _mgmt.get_focus_artist()
        return _artist.json


"""*****"""
"""ALBUM"""
"""*****"""


@app.route(f"/<artist>/{Consts.DISCOGRAPHY}", methods=[HttpMethod.GET])
def discography(artist):
    """Get all albums for artist"""
    _mgmt = get_mgmt()
    return _mgmt.get_discography(artist)


@app.route(f"/<artist>/{Consts.CREATE_ALBUM}", methods=[HttpMethod.POST])
def create_album(artist):
    """Create an album"""
    _album = _get_request_param(Consts.ALBUM)
    _mgmt = get_mgmt()
    _mgmt.start_new_album(artist, _album)
    return successful_response()


@app.route(f"/<artist>/<album>/add-track")
def add_track(artist, album):
    # TODO
    pass


def _get_request_param(key):
    _json = request.json
    artist = _json.get(key)
    return artist
