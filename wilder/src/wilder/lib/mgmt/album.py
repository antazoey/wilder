import os

from wilder.lib.constants import Constants as Consts
from wilder.lib.errors import NoTracksFoundErrorWildError
from wilder.lib.errors import TrackAlreadyExistError
from wilder.lib.errors import TrackNotFoundError
from wilder.lib.mgmt.album_dir import get_album_dir_json
from wilder.lib.mgmt.album_dir import get_album_json_path
from wilder.lib.mgmt.album_dir import get_track_path
from wilder.lib.mgmt.album_dir import init_album_dir
from wilder.lib.mgmt.release import Release
from wilder.lib.mgmt.track import Track
from wilder.lib.util.conversion import to_int
from wilder.lib.util.sh import remove_directory
from wilder.lib.util.sh import remove_file_if_exists
from wilder.lib.util.sh import rename_directory
from wilder.lib.util.sh import save_json_as


class Album:
    def __init__(
        self,
        path,
        name,
        artist,
        description=None,
        album_type=None,
        status=None,
        tracks=None,
        releases=None,
    ):
        self.path = path
        self.name = name
        self.artist = artist
        self.description = description
        self.album_type = album_type
        self.status = status
        self._tracks = tracks
        self.releases = releases

    def init_dir(self):
        """Create the album directory with default files."""
        init_album_dir(self.path, self.name)

    @classmethod
    def from_json(cls, album_json, artist_name):
        """Create the Artist object from data from .wilder/mgmt.json."""
        path = album_json[Consts.PATH]
        name = album_json[Consts.NAME]
        album_json = get_album_dir_json(path, name)
        album = cls(
            path,
            name,
            artist=artist_name,
            description=album_json.get(Consts.DESCRIPTION, ""),
            album_type=album_json.get(Consts.ALBUM_TYPE),
            status=album_json.get(Consts.STATUS),
            tracks=_parse_tracks(album_json),
            releases=_parse_releases(artist_name, name, album_json),
        )
        return album.save_album_metadata()

    def get_tracks(self):
        if not self._tracks:
            raise NoTracksFoundErrorWildError(self.name)
        return sorted(self._tracks, key=lambda t: t.track_number)

    @property
    def dir_json_path(self):
        """The path to the album directory."""
        return get_album_json_path(self.path)

    def to_json_for_album_dir(self):
        """The JSON blob representing the artifact in the album's directory."""
        return {
            Consts.ARTIST: self.artist,
            Consts.NAME: self.name,
            Consts.PATH: self.path,
            Consts.DESCRIPTION: self.description,
            Consts.ALBUM_TYPE: self.album_type,
            Consts.STATUS: self.status,
            Consts.TRACKS: [t.name for t in self._tracks],
            Consts.RELEASES: [r.to_json() for r in self.releases],
        }

    def to_json_for_mgmt(self):
        """Convert this object to JSON for storing in the user's MGMT JSON."""
        # Figure out name if path is set but name for some reason isn't
        if not self.name and self.path:
            self.name = os.path.basename(os.path.normpath(self.path))
            self.save_album_metadata()

        return {Consts.NAME: self.name, Consts.PATH: self.path}

    def update(self, description=None, album_type=None, status=None, artist=None):
        """Update an album."""
        self.description = description or self.description
        self.album_type = album_type or self.album_type
        self.status = status or self.status
        self.artist = artist or self.artist
        self.save_album_metadata()

    def rename(self, new_name):
        self.name = new_name
        self.path = rename_directory(self.path, new_name)
        self.save_album_metadata()

    def create_track(
        self, track_name, track_number=None, description=None, collaborators=None
    ):
        """Add a track to an album."""
        tracks = self.get_tracks()
        current_tracks = [t.name for t in tracks]
        if track_name in current_tracks:
            raise TrackAlreadyExistError(track_name, self.name)
        track_path = get_track_path(self.path, track_name)
        track_number = track_number or len(current_tracks) + 1
        track = Track(
            track_path,
            track_name,
            track_number,
            self.artist,
            self.name,
            description=description,
            collaborators=collaborators or [],
        )
        track.init_dir()
        track.save_track_metadata()
        self._add_track(track)
        self.save_album_metadata()

    def _add_track(self, track):
        self._tracks.append(track)
        self.save_album_metadata()

    def save_album_metadata(self):
        """Save the current album context to the album's JSON file."""
        remove_file_if_exists(self.dir_json_path)
        full_json = self.to_json_for_album_dir()
        save_json_as(self.dir_json_path, full_json)
        return self

    def get_track(self, name):
        """Get a track on the album by name."""
        tracks = self.get_tracks()
        for track in tracks:
            if track.name == name:
                return track
        raise TrackNotFoundError(self.name, name)

    def get_first_track_by_number(self, track_number):
        """Returns the first track with the given number."""
        track_number = to_int(track_number)
        tracks = self.get_tracks()
        for track in tracks:
            if to_int(track.track_number) == track_number:
                return track
        raise TrackNotFoundError(
            self.name, str(track_number), prop_name=Consts.TRACK_NUMBER
        )

    def delete_track(self, track_name, hard=False):
        """Delete a track. Set hard to True to delete the directory."""
        tracks = self.get_tracks()
        for i in range(0, len(tracks)):
            if self._tracks[i].name != track_name:
                continue
            elif hard:
                remove_directory(self._tracks[i].path)
            del self._tracks[i]
            self.auto_set_track_numbers()
            self.save_album_metadata()
            break

    def rename_track(self, new_name, track_name):
        """Change the name of a track."""
        track = self.get_track(track_name)
        track.rename(new_name)
        self.save_album_metadata()

    def bulk_set_track_numbers(self, track_number_dict):
        for name, num in track_number_dict.items():
            track = self.get_track(name)
            track.track_number = num
            track.save_track_metadata()
        self.save_album_metadata()

    def auto_set_track_numbers(self):
        tracks = self.get_tracks()
        for i in range(0, len(tracks)):
            track = tracks[i]
            track.track_number = i + 1
            track.save_track_metadata()


def _parse_tracks(album_dir_json):
    tracks = album_dir_json.get(Consts.TRACKS, [])
    return [Track.from_json(album_dir_json, t) for t in tracks]


def _parse_releases(artist_name, album_name, album_dir_json):
    releases = album_dir_json.get(Consts.RELEASES)
    return [
        Release.from_json(artist_name, album_name, release_json)
        for release_json in releases
    ]
