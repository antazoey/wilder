from wilder import BaseWildApi
from wilder.client.connection import Connection
from wilder.client.connection import create_connection
from wilder.client.errors import WildBadRequestError
from wilder.client.errors import WildClientError
from wilder.client.errors import WildNotFoundError
from wilder.constants import Constants
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.parser import parse_artists
from wilder.parser import parse_mgmt


def create_client(config):
    conn = create_connection(config.host, config.port)
    return WildClient(conn)


def err_when_not_found(arg_key):
    def decorator(f):
        def decorate(*args, **kwargs):
            name = kwargs.get(arg_key)
            try:
                return f(*args, **kwargs)
            except WildNotFoundError as err:
                if f"{name} not found" in str(err):
                    raise ArtistNotFoundError(name)
                raise
        return decorate
    return decorator


def _make_artist_params(artist_name):
    return {Constants.ARTIST: artist_name}


def _handle_artist_not_found_bad_request(err, artist):
    if f"{artist} not found" in str(err):
        raise ArtistNotFoundError(artist)


class WildClient(BaseWildApi):
    def __init__(self, conn=None):
        self.connection = conn or create_connection("127.0.0.1", 443)
        BaseWildApi.__init__(self)

    def get_artists(self):
        _json = self._get(Constants.ARTISTS)
        return parse_artists(_json)

    def get_mgmt(self):
        _json = self._get(Constants.MGMT)
        return parse_mgmt(_json)

    @err_when_not_found(Constants.NAME)
    def get_artist_by_name(self, name):
        """Returns an :class:`wilder.models.Artist` for the given name.
        Raises :class:`wilder.errors.ArtistNotFoundError` when the name does not exist.
        """
        mgmt = self.get_mgmt()
        artist = mgmt.get_artist_by_name(name)
        if not artist:
            raise ArtistNotFoundError(name)
        return artist

    @err_when_not_found(Constants.ARTIST)
    def get_discography(self, artist):
        url = f"{artist}/{Constants.DISCOGRAPHY}"
        return self._get(url)

    def sign_new_artist(self, artist, bio):
        """Creates a new artist.
        Raises :class:`wilder.errors.ArtistAlreadySignedError` if the artist already exists.
        """
        try:
            params = _make_artist_params(artist)
            params[Constants.BIO] = bio
            return self._post(Constants.SIGN, params)
        except WildBadRequestError as err:
            if f"{artist} already signed" in str(err):
                raise ArtistAlreadySignedError(artist)
            raise

    def unsign_artist(self, artist):
        """Removed an artist."""
        try:
            return self._post(Constants.UNSIGN, _make_artist_params(artist))
        except WildBadRequestError as err:
            if f"{artist} is not signed" in str(err):
                raise ArtistNotSignedError(artist)
            raise

    def update_artist(self, name, bio=None):
        resource = f"{name}/update"
        try:
            return self._post(resource, {Constants.BIO: bio})
        except WildBadRequestError as err:
            _handle_artist_not_found_bad_request(err, name)
            raise

    def start_new_album(self, artist, album):
        try:
            resource = f"{artist}/{Constants.CREATE_ALBUM}"
            return self._post(resource, {Constants.ALBUM: album})
        except WildNotFoundError as err:
            _handle_artist_not_found_bad_request(err, artist)
            raise
    
    def focus_on_artist(self, artist_name):
        try:
            self._post(Constants.FOCUS, _make_artist_params(artist_name))
        except WildNotFoundError as err:
            _handle_artist_not_found_bad_request(err, artist_name)
            raise

    def _get(self, endpoint):
        response = self.connection.get(f"/{endpoint}")
        if response:
            return response.json()

    def _post(self, endpoint, params=None):
        response = self.connection.post(f"/{endpoint}", json=params)
        if response:
            return response.json()
