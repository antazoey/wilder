from wilder import BaseWildApi
from wilder.client.connection import Connection
from wilder.client.connection import create_connection
from wilder.client.errors import WildClientError
from wilder.constants import ALBUM
from wilder.constants import ARTIST
from wilder.constants import ARTISTS
from wilder.constants import CREATE_ALBUM
from wilder.constants import MGMT
from wilder.constants import SIGN
from wilder.constants import UNSIGN
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.parser import parse_artists
from wilder.parser import parse_mgmt
from wilder.server import WildBadRequestError
from wilder.server.error import WildNotFoundError


def create_client(config):
    conn = create_connection(config.host, config.port)
    return WildClient(conn)


class WildClient(BaseWildApi):
    def __init__(self, conn=None):
        self.connection = conn or create_connection("127.0.0.1", 443)
        BaseWildApi.__init__(self)

    def get_artists(self):
        _json = self._get(ARTISTS)
        return parse_artists(_json)

    def get_mgmt(self):
        _json = self._get(MGMT)
        return parse_mgmt(_json)

    def get_artist_by_name(self, name):
        """Returns an :class:`wilder.models.Artist` for the given name.
        Raises :class:`wilder.errors.ArtistNotFoundError` when the name does not exist.
        """
        mgmt = self.get_mgmt()
        try:
            return mgmt.get_artist_by_name(name)
        except WildNotFoundError as err:
            if f"{name} not found" in str(err):
                raise ArtistNotFoundError(name)
            raise

    def sign_new_artist(self, artist):
        """Creates a new artist.
        Raises :class:`wilder.errors.ArtistAlreadySignedError` if the artist already exists.
        """
        try:
            return self._post(SIGN, {ARTIST: artist})
        except WildBadRequestError as err:
            if f"{artist} already signed" in str(err):
                raise ArtistAlreadySignedError(artist)
            raise

    def unsign_artist(self, artist):
        """Removed an artist."""
        try:
            return self._post(UNSIGN, {ARTIST: artist})
        except WildBadRequestError as err:
            if f"{artist} is not signed" in str(err):
                raise ArtistNotSignedError(artist)
            raise

    def start_new_album(self, artist, album):
        return self._post(CREATE_ALBUM, {ARTIST: artist, ALBUM: album})

    def _get(self, endpoint):
        response = self.connection.get(f"/{endpoint}")
        if response:
            return response.json()

    def _post(self, endpoint, params=None):
        response = self.connection.post(f"/{endpoint}", json=params)
        if response:
            return response.json()
