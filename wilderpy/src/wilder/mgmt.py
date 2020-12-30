from wilder import BaseWildApi
from wilder.constants import Constants
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.models import Artist
from wilder.parser import parse_mgmt
from wilder.parser import save


class Wilder(BaseWildApi):
    def __init__(self, mgmt_obj=None):
        self._mgmt = mgmt_obj or parse_mgmt()

    def get_artists(self):
        """The artists represented."""
        return self._mgmt.artists

    def get_mgmt(self):
        return self._mgmt.json

    def get_artist_by_name(self, name):
        """Returns an :class:`wilder.models.Artist` for the given name.
        Raises :class:`wilder.errors.ArtistNotFoundError` when the name does not exist.
        """
        artist = self._mgmt.get_artist_by_name(name)
        if not artist:
            raise ArtistNotFoundError(name)
        return artist

    def get_discography(self, artist):
        artist = self.get_artist_by_name(artist)
        return {Constants.DISCOGRAPHY: [a.json for a in artist.discography]}

    def sign_new_artist(self, name, bio=None):
        """Creates a new artist.
        Raises :class:`wilder.errors.ArtistAlreadySignedError` if the artist already exists.
        """
        if self.is_represented(name):
            raise ArtistAlreadySignedError(name)
        artist = Artist(name=name, bio=bio)
        self._mgmt.artists.append(artist)
        self._save()

    def unsign_artist(self, name):
        """Removed an artist."""
        if not self.is_represented(name):
            raise ArtistNotSignedError(name)
        del self._mgmt[name]
        self._save()

    def update_artist(self, name, bio=None):
        artist = self.get_artist_by_name(name)
        artist.bio = bio or artist.bio
        self._save()

    def start_new_album(self, artist_name, album_name):
        artist = self.get_artist_by_name(artist_name)
        artist.start_new_album(album_name)
        self._save()

    def _save(self):
        return save(self.get_mgmt())
    
    def focus_on_artist(self, artist_name):
        artist = self.get_artist_by_name(artist_name)
        self._mgmt.focus_artist = artist.name
        self._save()


def get_mgmt(obj=None):
    """Returns a new instance of an :class:`wilder.mgmt.ArtistMgmt`."""
    return Wilder(obj)
