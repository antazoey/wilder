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


def _as_artist_dict(artist_name):
    return {Constants.ARTIST: artist_name}


def _as_artist_url(endpoint):
    return _as_url(Constants.ARTIST, endpoint)


def _as_album_url(endpoint):
    return _as_url(Constants.ALBUM, endpoint)


def _as_url(group, resource):
    return f"{group}/{resource}"


def _send_alias_request(artist_name, alias, method):
    url = _as_artist_url(Constants.ALIAS)
    _json = {Constants.ARTIST: artist_name, Constants.ALIAS: alias}
    method(url, json=_json)


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
        url = _as_artist_url(Constants.LIST)
        _json = self._get(url).get(Constants.ARTISTS)
        return [Artist.from_json(a_json) for a_json in _json]

    def get_artist(self, name=None):
        """Get an artist."""
        _json = self._get(Constants.ARTIST, params={"artist": name})
        return Artist.from_json(_json)

    def focus_on_artist(self, artist_name):
        """Change the focus artist."""
        url = _as_artist_url(Constants.FOCUS)
        self._post(url, _as_artist_dict(artist_name))

    def sign_new_artist(self, artist, bio=None):
        """Create a new artist."""
        try:
            data = _as_artist_dict(artist)
            data[Constants.BIO] = bio
            url = _as_artist_url(Constants.SIGN)
            self._post(url, data)
        except WildBadRequestError as err:
            if f"{artist} already signed" in str(err):
                raise ArtistAlreadySignedError(artist)
            raise

    def unsign_artist(self, artist):
        """Remove a managed artist."""
        try:
            url = _as_artist_url(Constants.UNSIGN)
            self._post(url, _as_artist_dict(artist))
        except WildBadRequestError as err:
            if f"{artist} is not signed" in str(err):
                raise ArtistNotSignedError(artist)
            raise

    def update_artist(self, name=None, bio=None):
        """Update artist information."""
        url = _as_artist_url(Constants.UPDATE)
        self._post(url, json={Constants.ARTIST: name, Constants.BIO: bio})

    def rename_artist(self, new_name, artist_name=None, forget_old_name=False):
        """Change an artist's performer name."""
        url = _as_artist_url(Constants.RENAME)
        data = _as_artist_dict(artist_name)
        data[Constants.NEW_NAME] = new_name
        data[Constants.FORGET_OLD_NAME] = forget_old_name
        self._post(url, json=data)

    def add_alias(self, alias, artist_name=None):
        """Add an additional artist name, such as a 'formerly known as'."""
        _send_alias_request(alias, artist_name, self._post)

    def remove_alias(self, alias, artist_name=None):
        """Remove one of the additional artist names."""
        _send_alias_request(alias, artist_name, self._delete)

    """Album"""

    def get_discography(self, artist_name=None):
        """Get all the albums for an artist."""
        url = _as_album_url(Constants.DISCOGRAPHY)
        albums = self._get(url, params=_as_artist_dict(artist_name)).get(
            Constants.ALBUMS
        )
        return [Album.from_json(artist_name, a_json) for a_json in albums]

    def get_album(self, name, artist_name=None):
        """Get an album by its title."""
        url = f"{Constants.ALBUM}"
        params = _as_artist_dict(artist_name)
        params[Constants.ALBUM] = name
        return self._get(url, params=params)

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
        data = _as_artist_dict(artist_name)
        data[Constants.ALBUM] = album_name
        data[Constants.DESCRIPTION] = description
        data[Constants.ALBUM_TYPE] = album_type
        data[Constants.STATUS] = status
        self._post(url, json=data)

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
