from flask import Flask
from flask import jsonify
from flask import request
from wilder import get_wilder_sdk
from wilder.constants import Constants as Consts
from wilder.errors import WildError
from wilder.errors import WildNotFoundError as WildCoreNotFoundError
from wilder.util import get_mgmt_json
from wildserver._helper import error_response
from wildserver._helper import get_request_param
from wildserver._helper import HttpMethod
from wildserver._helper import successful_response
from wildserver.error import get_response_error_data
from wildserver.error import ShortErrorMessages
from wildserver.error import WildServerError


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


"""*********"""
"""ARTIST(S)"""
"""*********"""


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
    _artist = get_request_param(request, Consts.ARTIST)
    _mgmt = get_wilder_sdk()
    _mgmt.sign_new_artist(_artist)
    return successful_response()


@app.route(f"/{Consts.UNSIGN}", methods=[HttpMethod.POST])
def unsign():
    """Remove a managed artist"""
    _artist = get_request_param(request, Consts.ARTIST)
    _mgmt = get_wilder_sdk()
    _mgmt.unsign_artist(_artist)
    return successful_response()


@app.route(f"/<artist>/{Consts.UPDATE}", methods=[HttpMethod.POST])
def update_artist(artist):
    _mgmt = get_wilder_sdk()
    _bio = get_request_param(request, Consts.BIO)
    _mgmt.update_artist(artist, _bio)
    return successful_response()


@app.route(
    f"{Consts.ARTISTS}/{Consts.FOCUS}", methods=[HttpMethod.POST, HttpMethod.GET]
)
def focus():
    """Get or set the focus artist"""
    _mgmt = get_wilder_sdk()
    if request.method == HttpMethod.POST:
        _artist_name = get_request_param(request, Consts.ARTIST)
        _mgmt.focus_on_artist(_artist_name)
        return successful_response()
    else:
        _artist = _mgmt.get_focus_artist()
        return _artist.to_json


@app.route(
    f"{Consts.ARTISTS}/<artist>/{Consts.ALIAS}",
    methods=[HttpMethod.POST, HttpMethod.DELETE, HttpMethod.GET],
)
def alias(artist):
    _mgmt = get_wilder_sdk()
    if request.method == HttpMethod.POST:
        new_alias = get_request_param(request, Consts.ALSO_KNOWN_AS)
        _mgmt.add_alias(artist, new_alias)
    elif request.method == HttpMethod.DELETE:
        alias_to_delete = get_request_param(request, Consts.ALSO_KNOWN_AS)
        _mgmt.remove_alias(artist, alias_to_delete)
    else:
        _artist = _mgmt.get_artist_by_name(artist)
        return {Consts.ALSO_KNOWN_AS: _artist.also_known_as}


"""********"""
"""ALBUM(S)"""
"""********"""


@app.route(f"/{Consts.ALBUMS}/<artist>/{Consts.DISCOGRAPHY}", methods=[HttpMethod.GET])
def discography(artist):
    """Get all albums for artist"""
    _mgmt = get_wilder_sdk()
    albums = _mgmt.get_discography(artist)
    return {Consts.DISCOGRAPHY: [a.to_json for a in albums]}


@app.route(
    f"/{Consts.ALBUMS}/<artist>/{Consts.CREATE_ALBUM}", methods=[HttpMethod.POST]
)
def create_album(artist):
    """Create an album"""
    _album = get_request_param(request, Consts.ALBUM)
    _mgmt = get_wilder_sdk()
    _mgmt.start_new_album(artist, _album)
    return successful_response()


@app.route(
    f"/{Consts.ALBUMS}/<artist>/{Consts.DISCOGRAPHY}/<album>/{Consts.UPDATE}",
    methods=[HttpMethod.POST],
)
def update_album(artist, album):
    """Update an album"""
    description = get_request_param(request, Consts.DESCRIPTION)
    _mgmt = get_wilder_sdk()
    _mgmt.update_album(artist, album, description=description)
    return successful_response()


@app.route(f"/{Consts.ALBUMS}/<artist>/{Consts.DISCOGRAPHY}/<album>/add-track")
def add_track(artist, album):
    # TODO
    pass
