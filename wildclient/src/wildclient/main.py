from wildclient.connection import create_connection
from wildclient.errors import OperationNotPermittedError
from wildclient.errors import WildBadRequestError
from wilder.constants import Constants
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.errors import NoArtistsFoundError
from wilder.model import parse_mgmt
from wilder.models import Artist
from wilder.models import BaseWildApi


def create_client(config):
    conn = create_connection(config.host, config.port)
    if conn:
        return WildClient(conn)


def err_when_not_found(arg_keys):
    def decorator(f):
        def decorate(*args, **kwargs):
            name = kwargs.get(arg_keys)
            try:
                return f(*args, **kwargs)
            except Exception as err:
                if f"not found" in str(err):
                    raise ArtistNotFoundError(name)
                raise

        return decorate

    return decorator


def _make_artist_params(artist_name):
    return {Constants.ARTIST: artist_name}


def _make_artist_resource(artist, resource):
    return f"{artist}/{resource}"


class WildClient(BaseWildApi):
    def __init__(self, conn):
        self.connection = conn
        super().__init__()

    def get_artists(self):
        _json = self._get(Constants.ARTISTS)
        return [Artist.from_json(a_json) for a_json in _json]

    def get_mgmt_json(self):
        _json = self._get(Constants.MGMT)
        return parse_mgmt(_json)

    def get_focus_artist(self):
        artist_json = self._get(Constants.FOCUS)
        if artist_json:
            return Artist.from_json(artist_json)
        raise NoArtistsFoundError()

    @err_when_not_found(Constants.NAME)
    def get_artist_by_name(self, name):
        return self._get(f"{Constants.ARTIST}/{name}")

    def get_discography(self, artist):
        artist = artist or self.get_focus_artist()
        url = f"{artist}/{Constants.DISCOGRAPHY}"
        return self._get(url)

    def sign_new_artist(self, artist, bio):
        try:
            params = _make_artist_params(artist)
            params[Constants.BIO] = bio
            return self._post(Constants.SIGN, params)
        except WildBadRequestError as err:
            if f"{artist} already signed" in str(err):
                raise ArtistAlreadySignedError(artist)
            raise

    def unsign_artist(self, artist):
        try:
            return self._post(Constants.UNSIGN, _make_artist_params(artist))
        except WildBadRequestError as err:
            if f"{artist} is not signed" in str(err):
                raise ArtistNotSignedError(artist)
            raise

    @err_when_not_found(Constants.NAME)
    def update_artist(self, name, bio=None):
        resource = _make_artist_resource(name, "update")
        return self._post(resource, {Constants.BIO: bio})

    def add_alias(self, artist_name, alias):
        resource = _make_artist_resource(artist_name, Constants.ALIAS)
        return self._post(resource, alias)

    def remove_alias(self, artist_name, alias):
        resource = _make_artist_resource(artist_name, Constants.ALIAS)
        return self._delete(resource, alias)

    @err_when_not_found("artist_name")
    def start_new_album(self, artist_name, album):
        resource = _make_artist_resource(artist_name, Constants.CREATE_ALBUM)
        return self._post(resource, {Constants.ALBUM: album})

    @err_when_not_found("artist_name")
    def focus_on_artist(self, artist_name):
        return self._post(Constants.FOCUS, _make_artist_params(artist_name))

    @err_when_not_found("artist_name")
    def update_album(self):
        pass

    def _get(self, endpoint):
        response = self.connection.get(f"/{endpoint}")
        if response:
            return response.to_json()

    def _post(self, endpoint, params=None):
        response = self.connection.post(f"/{endpoint}", json=params)
        if response:
            return response.to_json()

    def _delete(self, endpoint, params=None):
        response = self.connection.delete(f"/{endpoint}", json=params)
        if response:
            return response.to_json()

    def nuke(self):
        raise OperationNotPermittedError()
