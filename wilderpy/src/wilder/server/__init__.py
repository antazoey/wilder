from flask import Flask
from flask import jsonify
from flask import request
from wilder import get_wilder_sdk
from wilder.constants import Constants as Consts
from wilder.errors import WildError
from wilder.errors import WildNotFoundError as WildCoreNotFoundError
from wilder.server._helper import error_response
from wilder.server._helper import HttpMethod
from wilder.server._helper import successful_response
from wilder.server.error import get_response_error_data
from wilder.server.error import ShortErrorMessages
from wilder.server.error import WildServerError
from wilder.util import get_mgmt_json


app = Flask(__name__)


"""**************"""
"""Error handlers"""
"""**************"""


@app.errorhandler(WildCoreNotFoundError)
def handle_not_found_wild_errors(err):
    _json = error_response(str(err), ShortErrorMessages.NOT_FOUND)
    response = jsonify(_json)
    response.status_code = 404
    return response


@app.errorhandler(WildServerError)
@app.errorhandler(Exception)
def handle_server_errors(err):
    msg = str(err)
    sc, short_msg = get_response_error_data(msg)
    response = (
        jsonify(err.dict)
        if hasattr(err, "json")
        else jsonify(error_response(msg, short_msg))
    )
    response.status_code = sc
    return response


@app.errorhandler(WildError)
def handle_wild_errors(err):
    response = jsonify(error_response(str(err), ShortErrorMessages.BAD_REQUEST))
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
    _mgmt = get_wilder_sdk()
    _artists = _mgmt.get_artists()
    return {Consts.ARTISTS: [a.to_json for a in _artists]}


@app.route(f"/{Consts.ARTIST}/<artist>", methods=[HttpMethod.GET])
def get_artist(artist):
    _mgmt = get_wilder_sdk()
    _artist = _mgmt.get_artist_by_name(artist)
    return _artist.to_json()


@app.route(f"/{Consts.SIGN}", methods=[HttpMethod.POST])
def sign():
    """Sign a new artist"""
    _artist = _get_request_param(Consts.ARTIST)
    _mgmt = get_wilder_sdk()
    _mgmt.sign_new_artist(_artist)
    return successful_response()


@app.route(f"/{Consts.UNSIGN}", methods=[HttpMethod.POST])
def unsign():
    """Remove a managed artist"""
    _artist = _get_request_param(Consts.ARTIST)
    _mgmt = get_wilder_sdk()
    _mgmt.unsign_artist(_artist)
    return successful_response()


@app.route(f"/<artist>/{Consts.UPDATE}", methods=[HttpMethod.POST])
def update_artist(artist):
    _mgmt = get_wilder_sdk()
    _bio = _get_request_param(Consts.BIO)
    _mgmt.update_artist(artist, _bio)
    return successful_response()


@app.route(f"/{Consts.FOCUS}", methods=[HttpMethod.POST, HttpMethod.GET])
def focus():
    """Get or set the focus artist"""
    _mgmt = get_wilder_sdk()
    if request.method == HttpMethod.POST:
        _artist_name = _get_request_param(Consts.ARTIST)
        _mgmt.focus_on_artist(_artist_name)
        return successful_response()
    else:
        _artist = _mgmt.get_focus_artist()
        return _artist.to_json


@app.route(
    f"/<artist>/{Consts.ALIAS}",
    methods=[HttpMethod.POST, HttpMethod.DELETE, HttpMethod.GET],
)
def alias(artist):
    _mgmt = get_wilder_sdk()
    if request.method == HttpMethod.POST:
        new_alias = _get_request_param(Consts.ALSO_KNOWN_AS)
        _mgmt.add_alias(artist, new_alias)
    elif request.method == HttpMethod.DELETE:
        alias_to_delete = _get_request_param(Consts.ALSO_KNOWN_AS)
        _mgmt.remove_alias(artist, alias_to_delete)
    else:
        _artist = _mgmt.get_artist_by_name(artist)
        return {Consts.ALSO_KNOWN_AS: _artist.also_known_as}


"""*****"""
"""ALBUM"""
"""*****"""


@app.route(f"/<artist>/{Consts.DISCOGRAPHY}", methods=[HttpMethod.GET])
def discography(artist):
    """Get all albums for artist"""
    _mgmt = get_wilder_sdk()
    albums = _mgmt.get_discography(artist)
    return {Consts.DISCOGRAPHY: [a.to_json for a in albums]}


@app.route(f"/<artist>/{Consts.CREATE_ALBUM}", methods=[HttpMethod.POST])
def create_album(artist):
    """Create an album"""
    _album = _get_request_param(Consts.ALBUM)
    _mgmt = get_wilder_sdk()
    _mgmt.start_new_album(artist, _album)
    return successful_response()


@app.route(f"/<artist>/{Consts.DISCOGRAPHY}/<album>/{Consts.UPDATE}", methods=[HttpMethod.POST])
def update_album(artist, album):
    """Update an album"""
    description = _get_request_param(Consts.DESCRIPTION)
    _mgmt = get_wilder_sdk()
    _mgmt.update_album(artist, album, description=description)
    return successful_response()


@app.route(f"/<artist>/{Consts.DISCOGRAPHY}/<album>/add-track")
def add_track(artist, album):
    # TODO
    pass


def _get_request_param(key):
    _json = request.json
    param = _json.get(key)
    return param
