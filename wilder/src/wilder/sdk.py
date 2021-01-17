import json
import shutil
from datetime import datetime

import wilder.lib.user as user
from wilder.lib.constants import Constants as Constants
from wilder.lib.errors import AlbumNotFoundError
from wilder.lib.errors import ArtistAlreadySignedError
from wilder.lib.errors import ArtistNotSignedError
from wilder.lib.errors import NoArtistsFoundError
from wilder.lib.errors import TrackNotFoundError
from wilder.lib.mgmt.artist import Artist
from wilder.lib.mgmt.track import Track
from wilder.lib.util.sh import save_as


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
    def __init__(self, artists=None, last_updated=None, focus_artist=None):
        self._artists = artists
        self._last_updated = last_updated
        self._focus_artist = focus_artist

    def __repr__(self):
        return f"Wilder-{self._focus_artist}"

    """Class"""

    @classmethod
    def from_json(cls, mgmt_json):
        last_updated = mgmt_json.get(Constants.LAST_UPDATED)
        focus_artist = mgmt_json.get(Constants.FOCUS_ARTIST)
        artists = _parse_artists(mgmt_json)
        return cls(
            artists=artists, last_updated=last_updated, focus_artist=focus_artist
        )

    def get_mgmt(self):
        """Get the full MGMT JSON blob."""
        return {
            Constants.LAST_UPDATED: self._last_updated,
            Constants.ARTISTS: [a.to_json() for a in self._artists],
            Constants.FOCUS_ARTIST: self._focus_artist,
        }

    """Artists"""

    def get_artists(self):
        """Get all artists."""
        return self._artists

    def get_artist(self, name=None):
        """Get an artist."""
        return self._get_artist_by_name(name) or self._get_focus_artist()

    def _get_artist_by_name(self, name):
        for artist in self._artists:
            if artist.name == name:
                return artist

    def _get_focus_artist(self):
        """Get the Wilder focus artist."""
        if not self._artists:
            raise NoArtistsFoundError()
        for artist in self._artists:
            if artist.name == self._focus_artist:
                return artist

        # If for some we have artists but none set as focus, set the first one.
        return self._set_first_artist_as_focus_artist()

    def _set_first_artist_as_focus_artist(self):
        first_artist = self._artists[0]
        self._focus_artist = first_artist.name
        self._save()
        return first_artist

    def focus_on_artist(self, artist_name):
        """Change the focus artist."""
        artist = self._get_artist_by_name(artist_name)
        self._focus_artist = artist.name
        self._save()

    def sign_new_artist(self, name, bio=None):
        """Create a new artist."""
        if self.is_represented(name):
            raise ArtistAlreadySignedError(name)
        artist = Artist(name=name, bio=bio)
        self._artists.append(artist)

        # Set focus artist if first artist signed
        if len(self._artists) == 1:
            self._focus_artist = artist.name
        self._save()

    def unsign_artist(self, name):
        """Remove an artist."""
        if not self.is_represented(name):
            raise ArtistNotSignedError(name)

        self._remove_artist_by_name(name)
        if not self._artists:
            self._focus_artist = None
        elif self._focus_artist == name:
            self._set_first_artist_as_focus_artist()
        self._save()

    def _remove_artist_by_name(self, name):
        new_artists = []
        for artist in self._artists:
            if artist.name != name:
                new_artists.append(artist)
        self._artists = new_artists

    def update_artist(self, name=None, bio=None):
        """Update artist information."""
        artist = self.get_artist(name=name)
        artist.bio = bio or artist.bio
        self._save()

    def rename_artist(self, new_name, artist_name=None, forget_old_name=False):
        """Change an artist's performer name."""
        if not new_name:
            raise ValueError("Must provide a new name when renaming an artist.")
        artist = self.get_artist(name=artist_name)
        old_name = artist.name
        artist.rename(new_name, forget_old_name=forget_old_name)
        if old_name == self._focus_artist:
            self._focus_artist = new_name
        self._save()

    def add_alias(self, alias, artist_name=None):
        """Add an additional artist name, such as a "formerly known as"."""
        artist = self.get_artist(name=artist_name)
        artist.add_alias(alias)
        self._save()

    def remove_alias(self, alias, artist_name=None):
        """Remove one of the additional artist names."""
        artist = self.get_artist(name=artist_name)
        artist.remove_alias(alias)
        self._save()

    """Albums"""

    def get_discography(self, artist_name=None):
        """Get all the albums for an artist."""
        artist_name = self.get_artist(name=artist_name)
        return artist_name.discography

    def get_album(self, name, artist_name=None):
        """Get an album by its title."""
        artist = self.get_artist(name=artist_name)
        album = artist.get_album_by_name(name)
        if not album:
            raise AlbumNotFoundError(name)
        return album

    def start_new_album(
        self,
        album_path,
        album_name=None,
        artist_name=None,
        description=None,
        album_type=None,
        status=None,
    ):
        """Start a new album."""
        artist = self.get_artist(name=artist_name)
        artist.start_new_album(
            album_path,
            name=album_name,
            description=description,
            album_type=album_type,
            status=status,
        )
        self._save()

    def update_album(
        self,
        album_name,
        artist_name=None,
        description=None,
        album_type=None,
        status=None,
    ):
        """Update an existing album."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.description = description or album.description
        album.album_type = album_type or album.album_type
        album.status = status or album.status
        self._save()

    def start_new_track(
        self,
        album_name,
        track_name,
        track_num,
        artist_name=None,
        description=None,
        collaborators=None,
    ):
        """Add a track to an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        track = Track(
            track_name, track_num, description=description, collaborators=collaborators
        )
        album.add_track(track)
        self._save()

    def delete_album(self, album_name, artist_name=None):
        """Delete an album."""
        artist = self.get_artist(artist_name)
        album = self.get_album(album_name, artist_name=artist_name)
        artist.delete_album(album)
        self._save()

    def get_tracks(self, album_name, artist_name=None):
        """Get all the tracks on an album."""
        artist = self.get_artist(artist_name)
        return artist.discography

    def play_track(self, album_name, track_name, artist_name=None):
        """Play a track from an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        track = album.get_track(track_name)
        if not track:
            raise TrackNotFoundError(album_name, track_name)

    """Other"""

    @staticmethod
    def nuke():
        shutil.rmtree(user.get_project_path())

    def _save(self):
        _json = self.get_mgmt()
        return save(_json)


def _parse_artists(mgmt_json):
    artist_paths = mgmt_json.get(Constants.ARTISTS) or []
    return [Artist.from_path_json(a) for a in artist_paths]


def get_wilder_sdk():
    """Parses the mgmt JSON file at the .wilder directory and returns the Mgmt object."""
    mgmt_json = user.get_mgmt_json()
    return Wilder.from_json(mgmt_json)


def save(mgmt_json_dict):
    """Save a MGMT dictionary to the .wilder/mgmt.json file."""
    mgmt_json_dict[Constants.LAST_UPDATED] = datetime.utcnow().timestamp()
    mgmt_json = json.dumps(mgmt_json_dict, indent=2)
    mgmt_path = user.get_mgmt_json_path()
    save_as(mgmt_path, mgmt_json)
