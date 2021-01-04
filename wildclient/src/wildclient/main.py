from wildclient.connection import create_connection
from wildclient.errors import OperationNotPermittedError
from wildclient.errors import WildBadRequestError
from wilder import BaseWildApi
from wilder import parse_mgmt
from wilder.constants import Constants
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wilder.models import Album
from wilder.models import Artist


def create_client(config):
    conn = create_connection(config.host, config.port)
    if conn:
        return WildClient(conn)


def _make_artist_params(artist_name):
    return {Constants.ARTIST: artist_name}


class WildClient(BaseWildApi):
    def __init__(self, conn):
        self.connection = conn
        super().__init__()

    def get_mgmt(self):
        _json = self._get(Constants.MGMT)
        return parse_mgmt(_json)

    """Artist"""

    def get_artists(self):
        """Get all artists."""
        _json = self._get(f"{Constants.ARTIST}/list").get(Constants.ARTISTS)
        return [Artist.from_json(a_json) for a_json in _json]

    def get_artist(self, name=None):
        """Get an artist."""
        _json = self._get(f"{Constants.ARTIST}", params={"artist": name})
        return Artist.from_json(_json)

    def focus_on_artist(self, artist_name):
        """Change the focus artist."""
        self._post(Constants.FOCUS, _make_artist_params(artist_name))

    def sign_new_artist(self, artist, bio=None):
        """Create a new artist."""
        try:
            params = _make_artist_params(artist)
            params[Constants.BIO] = bio
            self._post(Constants.SIGN, params)
        except WildBadRequestError as err:
            if f"{artist} already signed" in str(err):
                raise ArtistAlreadySignedError(artist)
            raise

    def unsign_artist(self, artist):
        """Remove a managed artist."""
        try:
            self._post(Constants.UNSIGN, _make_artist_params(artist))
        except WildBadRequestError as err:
            if f"{artist} is not signed" in str(err):
                raise ArtistNotSignedError(artist)
            raise

    def update_artist(self, name=None, bio=None):
        """Update artist information."""
        url = f"/{Constants.ARTIST}/update"
        self._post(url, json={Constants.ARTIST: name, Constants.BIO: bio})

    def rename_artist(self, new_name, artist_name=None, forget_old_name=False):
        """Change an artist's performer name."""
        url = f"/{Constants.ARTIST}/rename"
        _json = {
            Constants.ARTIST: artist_name,
            Constants.NEW_NAME: new_name,
            Constants.FORGET_OLD_NAME: forget_old_name,
        }
        self._post(url, json=_json)

    def add_alias(self, alias, artist_name=None):
        """Add an additional artist name, such as a 'formerly known as'."""
        url = f"/{Constants.ARTIST}/{Constants.ALIAS}"
        self._post(url, json={Constants.ARTIST: artist_name, Constants.ALIAS: alias})

    def remove_alias(self, alias, artist_name=None):
        """Remove one of the additional artist names."""
        url = f"{Constants.ARTIST}/{Constants.ALIAS}"
        self._delete(url, json={Constants.ARTIST: artist_name, Constants.ALIAS: alias})

    """Album"""

    def get_discography(self, artist_name=None):
        """Get all the albums for an artist."""
        url = f"{Constants.ALBUM}/{Constants.DISCOGRAPHY}"
        albums = self._get(url, params={Constants.ARTIST: artist_name}).get(
            Constants.ALBUMS
        )
        return [Album.from_json(artist_name, a_json) for a_json in albums]

    def get_album(self, name, artist_name=None):
        """Get an album by its title."""
        url = f"{Constants.ALBUM}"
        return self._get(
            url, params={Constants.ALBUM: name, Constants.ARTIST: artist_name}
        )

    def start_new_album(
        self,
        album_name,
        artist_name=None,
        description=None,
        album_type=None,
        status=None,
    ):
        """Start a new album."""
        url = f"{Constants.ALBUM}/{Constants.CREATE_ALBUM}"
        _json = {
            Constants.ALBUM: album_name,
            Constants.ARTIST: artist_name,
            Constants.DESCRIPTION: description,
            Constants.ALBUM_TYPE: album_type,
            Constants.STATUS: status,
        }
        self._post(url, json=_json)

    def update_album(
        self,
        album_name,
        artist_name=None,
        description=None,
        album_type=None,
        status=None,
    ):
        """Update an existing album."""
        url = f"{Constants.ALBUM}/{Constants.UPDATE}"
        _json = {
            Constants.ALBUM: album_name,
            Constants.ARTIST: artist_name,
            Constants.DESCRIPTION: description,
            Constants.ALBUM_TYPE: album_type,
            Constants.STATUS: status,
        }
        self._post(url, _json)

    """Internal"""

    def _get(self, endpoint, params=None):
        response = self.connection.get(f"/{endpoint}", params=params)
        if response:
            return response.json()

    def _post(self, endpoint, json=None):
        response = self.connection.post(f"/{endpoint}", json=json)
        if response:
            return response.json()

    def _delete(self, endpoint, json=None):
        response = self.connection.delete(f"/{endpoint}", json=json)
        if response:
            return response.json()

    def nuke(self):
        raise OperationNotPermittedError()
