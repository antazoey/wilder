from wilderpy.errors import ArtistAlreadySignedError
from wilderpy.errors import ArtistNotFoundError
from wilderpy.models import Artist
from wilderpy.parser import parse_mgmt


def get_mgmt():
    """Returns a new instance of an :class:`wilderpy.mgmt.ArtistMgmt`."""
    return ArtistMgmt()


class ArtistMgmt:
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

    def get_artist_by_name(self, name):
        """Returns an :class:`wilderpy.models.Artist` for the given name.
        Raises :class:`wilderpy.errors.ArtistNotFoundError` when the name does not exist.
        """
        for artist in self.artists:
            if artist.name == name:
                return artist
        raise ArtistNotFoundError

    def get_all_albums_for_artist(self, artist_name):
        artist = self.get_artist_by_name(artist_name)
        return artist.discography

    def sign_new_artist(self, name):
        """Creates a new artist.
        Raises :class:`wilderpy.errors.ArtistAlreadySignedError` if the artist already exists.
        """
        if self.is_represented(name):
            raise ArtistAlreadySignedError
        artist = Artist(name)
        self.artists.append(artist)

    def is_represented(self, name):
        return name in self.artist_names
