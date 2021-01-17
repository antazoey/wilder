import os

from wilder.lib.constants import Constants
from wilder.lib.errors import AlbumAlreadyExistsError
from wilder.lib.mgmt.album import Album
from wilder.lib.util.sh import expand_path


class Artist:
    def __init__(self, discography=None, name=None, bio=None, also_known_as=None):
        self.discography = discography or []
        self.name = name
        self.bio = bio
        self.also_known_as = also_known_as or []

    @classmethod
    def from_path_json(cls, artist_json):
        name = artist_json.get(Constants.NAME)
        bio = artist_json.get(Constants.BIO)
        also_known_as = artist_json.get(Constants.ALSO_KNOWN_AS)
        discography_json = artist_json.get(Constants.DISCOGRAPHY) or []
        discography = cls._parse_discography(name, discography_json)
        return cls(
            discography=discography, name=name, bio=bio, also_known_as=also_known_as
        )

    def to_json(self):
        return {
            Constants.NAME: self.name,
            Constants.BIO: self.bio,
            Constants.DISCOGRAPHY: [a.to_json_for_mgmt() for a in self.discography],
            Constants.ALSO_KNOWN_AS: self.also_known_as,
        }

    def start_new_album(
        self, path_location, name=None, description=None, album_type=None, status=None
    ):
        for alb in self.discography:
            if alb.name == name:
                raise AlbumAlreadyExistsError(alb.name)
        path_location = expand_path(path_location)
        path_location = os.path.join(path_location, name)
        name = name or self._get_default_album_name()
        album = Album(
            path_location,
            name=name,
            description=description,
            album_type=album_type,
            status=status,
        )
        album.init_dir()
        self.discography.append(album)

    def delete_album(self, album):
        albums = []
        for alb in self.discography:
            if alb.name != album.name:
                albums.append(album)
        self.discography = albums

    def get_album_by_name(self, name):
        for alb in self.discography:
            if alb.name == name:
                return alb

    def _get_default_album_name(self):
        album_number = len(self.discography) + 1
        return f"{self.name} {album_number}"

    def rename(self, new_name, forget_old_name=False):
        old_name = self.name
        self.name = new_name
        if not forget_old_name and old_name not in self.also_known_as:
            self.also_known_as.append(old_name)

    def add_alias(self, alias):
        if alias not in self.also_known_as:
            self.also_known_as.append(alias)

    def remove_alias(self, alias):
        self.also_known_as = filter(lambda x: x != alias, self.also_known_as)

    @classmethod
    def _parse_discography(cls, artist_name, disco_json):
        return [Album.from_json(artist_name, album_json) for album_json in disco_json]
