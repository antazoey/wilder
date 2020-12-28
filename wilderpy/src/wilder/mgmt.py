from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.models import Artist
from wilder.parser import parse_mgmt
from wilder.parser import save


class Wilder:
    def __init__(self):
        self._mgmt = parse_mgmt()

    @property
    def artists(self):
        """The artists represented."""
        return self._mgmt.artists

    @property
    def artist_names(self):
        """The names of the artists represented."""
        return [a.name for a in self.artists]

    @property
    def json(self):
        return self._mgmt.json

    def get_artist_by_name(self, name):
        """Returns an :class:`wilder.models.Artist` for the given name.
        Raises :class:`wilder.errors.ArtistNotFoundError` when the name does not exist.
        """
        artist = self._mgmt.get_artist_by_name(name)
        if not artist:
            raise ArtistNotFoundError()
        return artist

    def sign_new_artist(self, name):
        """Creates a new artist.
        Raises :class:`wilder.errors.ArtistAlreadySignedError` if the artist already exists.
        """
        if self.is_represented(name):
            raise ArtistAlreadySignedError()
        artist = Artist(name)
        self.artists.append(artist)
        self._save()

    def start_new_album(self, artist_name, album_name):
        artist = self.get_artist_by_name(artist_name)
        artist.start_new_album(album_name)
        self._save()

    def unsign_artist(self, name):
        """Removed an artist."""
        if not self.is_represented(name):
            raise ArtistNotSignedError()
        del self._mgmt[name]
        self._save()

    def is_represented(self, name):
        """Returns True if the artist is represented by Wilder."""
        return name in self.artist_names

    def _save(self):
        return save(self.json)


def get_mgmt():
    """Returns a new instance of an :class:`wilder.mgmt.ArtistMgmt`."""
    return Wilder()
