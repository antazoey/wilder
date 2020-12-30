from flask import Flask
from flask import jsonify
from flask import request
from wilder.constants import Constants as Consts
from wilder.errors import WildError
from wilder.errors import WildNotFoundError as WildCoreNotFoundError
from wilder.mgmt import get_mgmt
from wilder.server._helper import _successful_response
from wilder.server._helper import _verify_data_present
from wilder.server._helper import HttpMethod
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
    response = jsonify(err.dict)
    response.status_code = 500
    return response


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
    _json = request.json
    artist = _json.get(Consts.ARTIST)
    _verify_data_present(artist)
    _mgmt = get_mgmt()
    _mgmt.sign_new_artist(artist)
    return _successful_response()


@app.route(f"/{Consts.UNSIGN}", methods=[HttpMethod.POST])
def unsign():
    """Remove a managed artist"""
    _json = request.json
    artist = _json.get(Consts.ARTIST)
    _verify_data_present(artist)
    _mgmt = get_mgmt()
    _mgmt.unsign_artist(artist)
    return _successful_response()


@app.route(f"<artist>/update")
def update_artist(artist):
    # TODO
    pass


@app.route(f"rename-artist")
def update_artist(artist):
    # TODO
    pass


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
    _verify_data_present(request.values, Consts.ALBUM)
    _mgmt = get_mgmt()
    album = request.json.get(Consts.ALBUM)
    _mgmt.start_new_album(artist, album)
    return _successful_response()


@app.route(f"<artist>/<album>/add-track")
def add_track(artist, album):
    # TODO
    pass
