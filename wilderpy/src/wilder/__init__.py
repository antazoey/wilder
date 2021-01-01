import json
import os
import shutil
from datetime import datetime

from wilder.constants import Constants as Consts
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.errors import NoArtistsFoundError
from wilder.models.artist import Artist
from wilder.models.mgmt import Mgmt
from wilder.util import get_mgmt_json
from wilder.util import get_mgmt_json_path
from wilder.util import get_project_path


class BaseWildApi:
    def get_artists(self):
        """Override"""
        return []

    @property
    def artist_names(self):
        """The names of the artists represented."""
        artists = self.get_artists()
        return [a.name for a in artists]

    def is_represented(self, name):
        """Returns True if the artist is represented by Wilder."""
        return name in self.artist_names


class Wilder(BaseWildApi):
    def __init__(self, mgmt_obj=None):
        self._mgmt = mgmt_obj or parse_mgmt()

    def get_artists(self):
        """The artists represented."""
        return self._mgmt.artists

    def get_mgmt_json(self):
        return self._mgmt.to_json()

    def get_focus_artist(self):
        artists = self.get_artists()
        artist_name = self._mgmt.focus_artist
        if not artists:
            raise NoArtistsFoundError()
        for artist in artists:
            if artist.name == artist_name:
                return artist
        return artists[0]

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
        return artist.discography

    def sign_new_artist(self, name, bio=None, also_known_as=None):
        """Creates a new artist.
        Raises :class:`wilder.errors.ArtistAlreadySignedError` if the artist already exists.
        """
        if self.is_represented(name):
            raise ArtistAlreadySignedError(name)
        artist = Artist(name=name, bio=bio, also_known_as=also_known_as)
        self._mgmt.artists.append(artist)

        # Set focus artist if first artist signed
        if len(self._mgmt.artists) == 1:
            self._mgmt.focus_artist = artist.name

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

    def add_alias(self, artist_name, alias):
        artist = self.get_artist_by_name(artist_name)
        artist.also_known_as.append(alias)
        self._save()

    def remove_alias(self, artist_name, alias):
        artist = self.get_artist_by_name(artist_name)
        artist.also_known_as = filter(lambda x: x != alias, artist.also_known_as)
        self._save()

    def start_new_album(self, artist_name, album_name):
        artist = self.get_artist_by_name(artist_name)
        artist.start_new_album(album_name)
        self._save()

    def focus_on_artist(self, artist_name):
        artist = self.get_artist_by_name(artist_name)
        self._mgmt.focus_artist = artist.name
        self._save()

    @staticmethod
    def nuke():
        shutil.rmtree(get_project_path())
    
    def _save(self):
        return save(self.get_mgmt_json())


def get_wilder_sdk(obj=None):
    """Returns a new instance of an :class:`wilder.mgmt.ArtistMgmt`."""
    return Wilder(obj)


def parse_mgmt(mgmt_json=None):
    # Parses the given mgmt json.
    # Give it a path to a JSON file to parse that file.
    # Give it None (or no arg) to parse the user config file.
    # Give it the raw dict to just use that.

    if mgmt_json is None or isinstance(mgmt_json, str):
        mgmt_json = get_mgmt_json(mgmt_path=mgmt_json)

    return Mgmt.from_json(mgmt_json)


def save(mgmt_json_dict):
    """Save a MGMT dictionary to the mgmt.json file."""
    mgmt_json_dict[Consts.LAST_UPDATED] = datetime.utcnow().timestamp()
    mgmt_json = json.dumps(mgmt_json_dict)
    mgmt_path = get_mgmt_json_path()
    os.remove(mgmt_path)
    with open(mgmt_path, "w") as mgmt_file:
        mgmt_file.write(mgmt_json)
