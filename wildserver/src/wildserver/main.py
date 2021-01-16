from flask import Flask
from flask import jsonify
from flask import request
from wilder import get_wilder_sdk
from wilder.constants import Constants as Consts
from wilder.errors import WildError
from wilder.errors import WildNotFoundError as WildCoreNotFoundError
from wilder.util.user import get_mgmt_json
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


"""****"""
"""MGMT"""
"""****"""


@app.route("/")
def main():
    return "<html>HeWild one</html>"


@app.route(f"/{Consts.MGMT}")
def mgmt():
    """Get full MGMT JSON"""
    return get_mgmt_json(as_dict=False)


"""*********"""
"""ARTIST(S)"""
"""*********"""


@app.route(f"{_ARTIST}/{Consts.LIST}", methods=[HttpMethod.GET])
def artist_list():
    """Get all artists."""
    wilder = get_wilder_sdk()
    _artists = wilder.get_artists()
    return {Consts.ARTISTS: [a.to_json() for a in _artists]}


@app.route(_ARTIST, methods=[HttpMethod.GET])
def artist():
    """Get an artist."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_query_param(Consts.ARTIST)
    _artist = wilder.get_artist(artist_name)
    return _artist.to_json()


@app.route(f"{_ARTIST}/{Consts.FOCUS}", methods=[HttpMethod.POST])
def artist_focus():
    """Change the focus artist."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    wilder.focus_on_artist(artist_name)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.SIGN}", methods=[HttpMethod.POST])
def artist_sign():
    """Sign a new artist."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    bio = _get_request_data_param(Consts.BIO)
    wilder.sign_new_artist(artist_name, bio=bio)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.UNSIGN}", methods=[HttpMethod.POST])
def artist_unsign():
    """Remove a managed artist."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    wilder.unsign_artist(artist_name)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.UPDATE}", methods=[HttpMethod.POST])
def artist_update():
    """Update artist information."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    bio = _get_request_data_param(Consts.BIO)
    wilder.update_artist(name=artist_name, bio=bio)
    return successful_response()


@app.route(f"{_ARTIST}/{Consts.RENAME}", methods=[HttpMethod.POST])
def artist_rename():
    """Update artist information."""
    wilder = get_wilder_sdk()
    new_name = _get_request_data_param(Consts.NEW_NAME)
    artist_name = _get_request_data_param(Consts.ARTIST)
    forget_old_name = _get_request_data_param(Consts.FORGET_OLD_NAME)
    wilder.rename_artist(
        new_name, artist_name=artist_name, forget_old_name=forget_old_name
    )
    return successful_response()


@app.route(
    f"{_ARTIST}/{Consts.ALIAS}",
    methods=[HttpMethod.POST, HttpMethod.DELETE, HttpMethod.GET],
)
def artist_alias():
    """Add, remove, or retrieve artist aliases."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    if request.method == HttpMethod.POST:
        new_alias = _get_request_data_param(Consts.ALSO_KNOWN_AS)
        wilder.add_alias(new_alias, artist_name=artist_name)
    elif request.method == HttpMethod.DELETE:
        alias_to_delete = _get_request_data_param(Consts.ALSO_KNOWN_AS)
        wilder.remove_alias(alias_to_delete, artist_name=artist_name)
    else:
        _artist = wilder.get_artist_by_name(artist_name)
        return {Consts.ALSO_KNOWN_AS: _artist.also_known_as}


"""********"""
"""ALBUM(S)"""
"""********"""


@app.route(f"{_ALBUM}/{Consts.DISCOGRAPHY}", methods=[HttpMethod.GET])
def album_discography():
    """Get all albums for artist."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    albums = wilder.get_discography(artist_name=artist_name)
    return {Consts.DISCOGRAPHY: [a.to_json for a in albums]}


@app.route(_ALBUM, methods=[HttpMethod.GET])
def album():
    """Get an album."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_query_param(Consts.ARTIST)
    album_name = _get_request_query_param(Consts.ALBUM)
    _album = wilder.get_album(album_name, artist_name=artist_name)
    return _album.to_json()


@app.route(f"{_ALBUM}/{Consts.CREATE_ALBUM}", methods=[HttpMethod.POST])
def album_create():
    """Create a new album."""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    path = _get_request_data_param(Consts.PATH)
    _album = _get_request_data_param(Consts.ALBUM)
    description = _get_request_data_param(Consts.DESCRIPTION)
    album_type = _get_request_data_param(Consts.ALBUM_TYPE)
    status = _get_request_data_param(Consts.STATUS)
    wilder.start_new_album(
        path,
        name=_album,
        artist_name=artist_name,
        description=description,
        album_type=album_type,
        status=status,
    )
    return successful_response()


@app.route(f"{_ALBUM}/{Consts.UPDATE}", methods=[HttpMethod.POST])
def album_update():
    """Update an album"""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    _album = _get_request_data_param(Consts.ALBUM)
    description = _get_request_data_param(Consts.DESCRIPTION)
    album_type = _get_request_data_param(Consts.ALBUM_TYPE)
    status = _get_request_data_param(Consts.STATUS)
    wilder.update_album(
        _album,
        artist_name=artist_name,
        description=description,
        album_type=album_type,
        status=status,
    )
    return successful_response()


@app.route(f"{_ALBUM}/{Consts.CREATE_TRACK}")
def album_create_track():
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    _album = _get_request_data_param(Consts.ALBUM)
    track = _get_request_data_param(Consts.TRACK)
    track_num = _get_request_data_param(Consts.TRACK_NUMBER)
    description = _get_request_data_param(Consts.DESCRIPTION)
    collaborators = _get_request_data_param(Consts.COLLABORATORS)
    wilder.start_new_track(
        album_name,
        track,
        track_num,
        artist_name=artist_name,
        description=description,
        collaborators=collaborators,
    )


@app.route(f"{_ALBUM}/{Consts.DELETE}", methods=[HttpMethod.POST])
def album_delete():
    """Delete an album"""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    _album = _get_request_data_param(Consts.ALBUM)
    wilder.delete_album(_album, artist_name=artist_name)
    return successful_response()


@app.route(f"{_ALBUM}/{Consts.LIST_TRACKS}", methods=[HttpMethod.GET])
def album_list_tracks():
    """List the tracks on an album"""
    wilder = get_wilder_sdk()
    artist_name = _get_request_data_param(Consts.ARTIST)
    _album = _get_request_data_param(Consts.ALBUM)
    return {Consts.ALBUMS: [t.to_json() for t in _album.tracks]}


def _get_request_query_param(key):
    return request.args.get(key)


def _get_request_data_param(key):
    return request.json.get(key)
