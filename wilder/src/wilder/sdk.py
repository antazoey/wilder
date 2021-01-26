import shutil
from datetime import datetime

import wilder.lib.user as user
from wilder.lib.constants import Constants as Constants
from wilder.lib.errors import ArtistAlreadyExistsError
from wilder.lib.errors import ArtistNotFoundError
from wilder.lib.errors import NoArtistsFoundError
from wilder.lib.mgmt.artist import Artist
from wilder.lib.player import play_album
from wilder.lib.player import play_track
from wilder.lib.util.sh import save_json_as


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
        try:
            return name in self.artist_names
        except NoArtistsFoundError:
            # To handle case where adding first artist
            return False


class Wilder(BaseWildApi):
    def __init__(
        self, artists=None, last_updated=None, focus_artist=None,
    ):
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
            artists=artists, last_updated=last_updated, focus_artist=focus_artist,
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
        artists = self._artists
        if not artists:
            raise NoArtistsFoundError()
        return artists

    def get_artist(self, name=None):
        """Get an artist."""
        artist = (
            self._get_focus_artist() if not name else self._get_artist_by_name(name)
        )
        return artist

    def _get_artist_by_name(self, name):
        artists = self.get_artists()
        for artist in artists:
            if artist.name == name:
                return artist
        raise ArtistNotFoundError(name)

    def _get_focus_artist(self):
        """Get the Wilder focus artist."""
        artists = self.get_artists()
        for artist in artists:
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

    def create_artist(self, name, bio=None):
        """Create a new artist."""
        if self.is_represented(name):
            raise ArtistAlreadyExistsError(name)
        artist = Artist(name=name, bio=bio)
        self._artists.append(artist)

        # Set focus artist if first artist signed
        if len(self._artists) == 1:
            self._focus_artist = artist.name
        self._save()

    def delete_artist(self, name):
        """Remove an artist."""
        if not self.is_represented(name):
            raise ArtistNotFoundError(name)

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
        album = artist.get_album(name)
        return album

    def create_album(
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
        artist.create_album(
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
        album.update(description=description, album_type=album_type, status=status)
        self._save()

    def rename_album(self, new_name, album_name, artist_name=None, hard=False):
        """Change the name of an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.rename(new_name, hard=hard)
        self._save()

    def delete_album(self, album_name, artist_name=None, hard=False):
        """Delete an album."""
        artist = self.get_artist(artist_name)
        album = self.get_album(album_name, artist_name=artist_name)
        artist.delete_album(album, hard=hard)
        self._save()

    def play_album(self, album_name, audio_type, artist_name=None):
        """Play a whole album."""
        album = self.get_album(album_name, artist_name=artist_name)
        play_album(album, audio_type)

    """Tracks"""

    def create_track(
        self,
        track_name,
        album_name,
        artist_name=None,
        track_number=None,
        description=None,
        collaborators=None,
    ):
        """Add a track to an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.create_track(
            track_name,
            track_number=track_number,
            description=description,
            collaborators=collaborators,
        )
        self._save()

    def update_track(
        self,
        track_name,
        album_name,
        artist_name=None,
        track_number=None,
        description=None,
        collaborators=None,
    ):
        """Update track metadata."""
        track = self.get_track(track_name, album_name, artist_name=artist_name)
        track.update(
            track_number=track_number,
            description=description,
            collaborators=collaborators,
        )

    def get_tracks(self, album_name, artist_name=None):
        """Get all the tracks on an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        return album.tracks

    def get_track(self, track_name, album_name, artist_name=None):
        """Get a single track from an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        return album.get_track(track_name)

    def delete_track(self, track_name, album_name, artist_name=None, hard=None):
        """Delete a track from an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.delete_track(track_name, hard=hard)

    def rename_track(self, new_name, track_name, album_name, artist_name=None):
        """Change the name of a track."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.rename_track(new_name, track_name)

    def bulk_set_track_numbers(self, track_numbers, album_name, artist_name=None):
        """Bulk set all of the track numbers on an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.bulk_set_track_numbers(track_numbers)

    def auto_set_track_numbers(self, album_name, artist_name=None):
        """Automatically adjust the track numbers on an album."""
        album = self.get_album(album_name, artist_name=artist_name)
        album.auto_set_track_numbers()

    def play_track(self, track_name, album_name, audio_type=None, artist_name=None):
        """Play a track from an album."""
        track = self.get_track(track_name, album_name, artist_name=artist_name)
        path = track.get_file(audio_type=audio_type)
        return play_track(path)

    """Other"""

    @staticmethod
    def nuke():
        shutil.rmtree(user.get_project_path())

    def _save(self):
        _json = self.get_mgmt()
        return save(_json)


def _parse_artists(mgmt_json):
    artist_paths = mgmt_json.get(Constants.ARTISTS) or []
    return [Artist.from_json(a) for a in artist_paths]


def get_wilder_sdk():
    """Parses the mgmt JSON file at the .wilder directory and returns the Mgmt object."""
    mgmt_json = user.get_mgmt_json()
    return Wilder.from_json(mgmt_json)


def save(mgmt_json_dict):
    """Save a MGMT dictionary to the .wilder/mgmt.json file."""
    mgmt_json_dict[Constants.LAST_UPDATED] = datetime.utcnow().timestamp()
    mgmt_path = user.get_mgmt_json_path()
    save_json_as(mgmt_path, mgmt_json_dict)
