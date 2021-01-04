from flask import Flask
from flask import jsonify
from flask import request
from wilder import get_wilder_sdk
from wilder.constants import Constants as Consts
from wilder.errors import WildError
from wilder.errors import WildNotFoundError as WildCoreNotFoundError
from wilder.util import get_mgmt_json
from wildserver._helper import error_response
from wildserver._helper import HttpMethod
from wildserver._helper import successful_response
from wildserver.error import get_response_error_data
from wildserver.error import ShortErrorMessages
from wildserver.error import WildServerError


app = Flask(__name__)
_ARTIST = f"/{Consts.ARTIST}"
_ALBUM = f"/{Consts.ALBUM}"


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


@app.route("/")
def main():
    return "<html>Wild one</html>"


@app.route(f"/{Consts.MGMT}")
def mgmt():
    """Get full MGMT JSON"""
    return get_mgmt_json(as_dict=False)


"""*********"""
"""ARTIST(S)"""
"""*********"""


@app.route(f"{_ARTIST}/list", methods=[HttpMethod.GET])
def list_artists():
    """Get all artists."""
    _mgmt = get_wilder_sdk()
    _artists = _mgmt.get_artists()
    return {Consts.ARTISTS: [a.to_json() for a in _artists]}


@app.route(_ARTIST, methods=[HttpMethod.GET])
def get_artist():
    """Get an artist."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    _artist = _mgmt.get_artist(artist_name)
    return _artist.to_json()


@app.route(f"{_ARTIST}/{Consts.FOCUS}", methods=[HttpMethod.POST])
def focus():
    """Change the focus artist."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    _mgmt.focus_on_artist(artist_name)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.SIGN}", methods=[HttpMethod.POST])
def sign():
    """Sign a new artist."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    bio = _get_request_param(Consts.BIO)
    _mgmt.sign_new_artist(artist_name, bio=bio)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.UNSIGN}", methods=[HttpMethod.POST])
def unsign():
    """Remove a managed artist."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    _mgmt.unsign_artist(artist_name)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.UPDATE}", methods=[HttpMethod.POST])
def update_artist():
    """Update artist information."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    bio = _get_request_param(Consts.BIO)
    _mgmt.update_artist(name=artist_name, bio=bio)
    return successful_response()


@app.route(f"{_ARTIST}/rename", methods=[HttpMethod.POST])
def rename_artist():
    """Update artist information."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    new_name = _get_request_param(Consts.NEW_NAME)
    forget_old_name = _get_request_param(Consts.FORGET_OLD_NAME)
    _mgmt.rename_artist(
        new_name, artist_name=artist_name, forget_old_name=forget_old_name
    )
    return successful_response()


@app.route(
    f"{_ARTIST}/{Consts.ALIAS}",
    methods=[HttpMethod.POST, HttpMethod.DELETE, HttpMethod.GET],
)
def alias():
    """Add, remove, or retrieve artist aliases."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    if request.method == HttpMethod.POST:
        new_alias = _get_request_param(Consts.ALSO_KNOWN_AS)
        _mgmt.add_alias(new_alias, artist_name=artist_name)
    elif request.method == HttpMethod.DELETE:
        alias_to_delete = _get_request_param(Consts.ALSO_KNOWN_AS)
        _mgmt.remove_alias(alias_to_delete, artist_name=artist_name)
    else:
        _artist = _mgmt.get_artist_by_name(artist_name)
        return {Consts.ALSO_KNOWN_AS: _artist.also_known_as}


"""********"""
"""ALBUM(S)"""
"""********"""


@app.route(f"{_ALBUM}/{Consts.DISCOGRAPHY}", methods=[HttpMethod.GET])
def discography():
    """Get all albums for artist."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    albums = _mgmt.get_discography(artist_name=artist_name)
    return {Consts.DISCOGRAPHY: [a.to_json for a in albums]}


@app.route(_ALBUM, methods=[HttpMethod.GET])
def get_album():
    """Get an album."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    album_name = _get_request_param(Consts.ALBUM)
    _album = _mgmt.get_album(album_name, artist_name=artist_name)
    return _album.to_json()


@app.route(f"{_ALBUM}/{Consts.CREATE_ALBUM}", methods=[HttpMethod.POST])
def create_album():
    """Create a new album."""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    _album = _get_request_param(Consts.ALBUM)
    description = _get_request_param(Consts.DESCRIPTION)
    album_type = _get_request_param(Consts.ALBUM_TYPE)
    status = _get_request_param(Consts.STATUS)
    _mgmt.start_new_album(
        _album,
        artist_name=artist_name,
        description=description,
        album_type=album_type,
        status=status,
    )
    return successful_response()


@app.route(f"{_ALBUM}/{Consts.UPDATE}", methods=[HttpMethod.POST])
def update_album(album):
    """Update an album"""
    _mgmt = get_wilder_sdk()
    artist_name = _get_request_param(Consts.ARTIST)
    description = _get_request_param(Consts.DESCRIPTION)
    album_type = _get_request_param(Consts.ALBUM_TYPE)
    status = _get_request_param(Consts.STATUS)
    _mgmt.update_album(
        album,
        artist_name=artist_name,
        description=description,
        album_type=album_type,
        status=status,
    )
    return successful_response()


def _get_request_param(key):
    _json = request.json
    param = _json.get(key)
    return param
