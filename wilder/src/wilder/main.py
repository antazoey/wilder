import json
import shutil
from datetime import datetime

import asfasdf
import wilder.lib.util.user as user
from wilder.constants import Constants as Consts
from wilder.errors import AlbumAlreadyExistsError
from wilder.errors import AlbumNotFoundError
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wilder.errors import NoArtistsFoundError
from wilder.mgmt import Track
from wilder.mgmt import Artist
from wilder.util.resources import get_artwork_path
from wilder.util.shellutil import create_dir_if_not_exists
from wilder.util.shellutil import expand_path
from wilder.util.shellutil import wopen


class BaseWildApi:
    def __init__(self):
        pass
    
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
    artists = []
    last_updated = None
    focus_artist = None
    
    """Class"""

    @classmethod
    def from_json(cls, mgmt_json):
        last_updated = mgmt_json.get(Constants.LAST_UPDATED)
        focus_artist = mgmt_json.get(Constants.FOCUS_ARTIST)
        artists = _parse_artists(mgmt_json)
        return cls(artists, last_updated=last_updated, focus_artist=focus_artist)

    def to_json(self):
        return {
            Constants.LAST_UPDATED: self.last_updated,
            Constants.ARTISTS: [a.to_json() for a in self.artists],
            Constants.FOCUS_ARTIST: self.focus_artist,
        }
    
    """API"""

    def get_mgmt(self):
        """Get the full MGMT JSON blob."""
        return self._mgmt

    """Artists"""

    def get_artists(self):
        """Get all artists."""
        return self.artists

    def get_artist(self, name=None):
        """Get an artist."""
        return self._get_artist_by_name(name=name) or self._get_focus_artist()

    def focus_on_artist(self, artist_name):
        """Change the focus artist."""
        artist = self._get_artist_by_name(artist_name)
        self._mgmt.focus_artist = artist.name
        self._save()

    def sign_new_artist(self, name, bio=None):
        """Create a new artist."""
        if self.is_represented(name):
            raise ArtistAlreadySignedError(name)
        artist = Artist(name=name, bio=bio)
        self._mgmt.artists.append(artist)

        # Set focus artist if first artist signed
        if len(self._mgmt.artists) == 1:
            self._mgmt.focus_artist = artist.name
        self._save()

    def unsign_artist(self, name):
        """Remove an artist."""
        if not self.is_represented(name):
            raise ArtistNotSignedError(name)
        focus_artist_name = self._mgmt.focus_artist
        del self._mgmt[name]
        if not len(self._mgmt.artists):
            self._mgmt.focus_artist = None
        elif len(self._mgmt.artists) == 1 or focus_artist_name == name:
            name = self._mgmt.artists[0].name
            self._mgmt.focus_artist = name
        self._save()

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
        focus_artist_name = self._get_focus_artist().name
        old_name = artist.name
        artist.name = new_name
        if not forget_old_name and old_name not in artist.also_known_as:
            artist.also_known_as.append(old_name)

        if old_name == focus_artist_name:
            self._mgmt.focus_artist = new_name
        self._save()

    def add_alias(self, alias, artist_name=None):
        """Add an additional artist name, such as a "formerly known as"."""
        artist = self.get_artist(name=artist_name)
        artist.also_known_as.append(alias)
        self._save()

    def remove_alias(self, alias, artist_name=None):
        """Remove one of the additional artist names."""
        artist = self.get_artist(name=artist_name)
        artist.also_known_as = filter(lambda x: x != alias, artist.also_known_as)
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
        for alb in artist.discography:
            if alb.name == album_name:
                raise AlbumAlreadyExistsError(alb.name)
        album_path = expand_path(album_path)
        album_path = f"{album_path}/{album_name}"
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
        albums = []
        for alb in artist.discography:
            if alb.name != album.name:
                albums.append(album)
        artist.discography = albums
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
            raise TrackNotFoundError()

    """Other"""

    @staticmethod
    def nuke():
        shutil.rmtree(get_project_path())

    def _save(self):
        mgmt = self.get_mgmt()
        _json = mgmt.to_json()
        return save(_json)

    def _get_focus_artist(self):
        """Get the Wilder focus artist."""
        artists = self.get_artists()
        artist_name = self._mgmt.focus_artist
        if not artists:
            raise NoArtistsFoundError()
        for artist in artists:
            if artist.name == artist_name:
                return artist
        return artists[0]


def _parse_artists(mgmt_json):
    artist_paths = mgmt_json.get(Constants.ARTISTS) or []
    return [Artist.from_path_json(a) for a in artist_paths]


def get_wilder_sdk(obj=None):
    """Parses the mgmt JSON file at the .wilder directory and returns the Mgmt object."""
    mgmt_json = user.get_mgmt_json()
    return Wilder.from_json(mgmt_json)


def save(mgmt_json_dict):
    """Save a MGMT dictionary to the .wilder/mgmt.json file."""
    mgmt_json_dict[Consts.LAST_UPDATED] = datetime.utcnow().timestamp()
    mgmt_json = json.dumps(mgmt_json_dict, indent=2)
    mgmt_path = user.get_mgmt_json_path()
    save_as(mgmt_path, mgmt_json)
