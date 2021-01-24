import os

from wilder.lib.constants import Constants
from wilder.lib.errors import AlbumAlreadyExistsError
from wilder.lib.errors import AlbumNotFoundError
from wilder.lib.errors import ArtistHasNoAlbumsError
from wilder.lib.mgmt.album import Album
from wilder.lib.util.sh import expand_path
from wilder.lib.util.sh import remove_directory


class Artist:
    def __init__(self, discography=None, name=None, bio=None, also_known_as=None):
        self._discography = discography or []
        self.name = name
        self.bio = bio
        self.also_known_as = also_known_as or []

    @classmethod
    def from_json(cls, artist_json):
        """Create an artist from JSON stored in the MGMT JSON blob."""
        name = artist_json.get(Constants.NAME)
        bio = artist_json.get(Constants.BIO)
        also_known_as = artist_json.get(Constants.ALSO_KNOWN_AS)
        discography_json = artist_json.get(Constants.DISCOGRAPHY) or []
        discography = cls._parse_discography(discography_json, name)
        return cls(
            discography=discography, name=name, bio=bio, also_known_as=also_known_as
        )

    def get_discography(self):
        """Get all the albums of an artist."""
        if not self._discography:
            raise ArtistHasNoAlbumsError(self.name)
        return self._discography

    def to_json(self):
        """Convert an Artist to JSON for storing in the MGMT JSON."""
        return {
            Constants.NAME: self.name,
            Constants.BIO: self.bio,
            Constants.DISCOGRAPHY: [a.to_json_for_mgmt() for a in self._discography],
            Constants.ALSO_KNOWN_AS: self.also_known_as,
        }

    def create_album(
        self, path_location, name=None, description=None, album_type=None, status=None
    ):
        """Initialize a new album in a given directory."""
        self._assert_album_not_exists(name)
        path_location = expand_path(path_location)
        path_location = os.path.join(path_location, name)
        name = name or self._get_default_album_name()
        album = Album(
            path_location,
            name,
            self.name,
            description=description,
            album_type=album_type,
            status=status,
        )
        album.init_dir()
        self._discography.append(album)

    def _assert_album_not_exists(self, name):
        for alb in self._discography:
            if alb.name == name:
                raise AlbumAlreadyExistsError(alb.name)

    def delete_album(self, album, hard=False):
        """Remove an album from Wilder. This does not destroy the directory."""
        albums = []
        for alb in self._discography:
            if alb.name != album.name:
                albums.append(album)
            elif hard:
                remove_directory(alb.path)
        self._discography = albums

    def get_album(self, name):
        """Return an album by its name."""
        for alb in self._discography:
            if alb.name == name:
                return alb
        raise AlbumNotFoundError(name)

    def _get_default_album_name(self):
        album_number = len(self._discography) + 1
        return f"{self.name} {album_number}"

    def rename(self, new_name, forget_old_name=False):
        """Change the name of this artist."""
        old_name = self.name
        self.name = new_name
        self._try_append_aka(forget_old_name, old_name)

    def _try_append_aka(self, forget_old_name, old_name):
        if not forget_old_name and old_name not in self.also_known_as:
            self.also_known_as.append(old_name)

    def add_alias(self, alias):
        """Add an alternative name to this artist."""
        if alias not in self.also_known_as:
            self.also_known_as.append(alias)

    def remove_alias(self, alias):
        """Remove one of the previously-added alternative-names of this artist."""
        self.also_known_as = filter(lambda x: x != alias, self.also_known_as)

    @classmethod
    def _parse_discography(cls, disco_json, artist_name):
        return [Album.from_json(album_json, artist_name) for album_json in disco_json]
