from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import get_track_dir_json
from wilder.lib.mgmt.album_dir import get_track_json_path
from wilder.lib.mgmt.album_dir import get_track_path
from wilder.lib.mgmt.album_dir import init_track_dir
from wilder.lib.util.conversion import to_int
from wilder.lib.util.sh import remove_file_if_exists
from wilder.lib.util.sh import save_json_as


class Track:
    def __init__(
        self,
        path,
        name,
        track_number,
        artist,
        album,
        description=None,
        collaborators=None,
    ):
        self.path = path
        self.name = name
        self._track_number = track_number
        self.artist = artist
        self.album = album
        self.description = description
        self.collaborators = collaborators

    @property
    def track_number(self):
        return to_int(self._track_number)

    @track_number.setter
    def track_number(self, track_number):
        self._track_number = to_int(track_number)

    @property
    def dir_json_path(self):
        """The path to the track JSON file."""
        return get_track_json_path(self.path)

    @classmethod
    def from_json(cls, album_json, track_name):
        """Creates a Track from JSON stored in the album dir."""
        album_path = album_json.get(Constants.PATH)
        album_name = album_json.get(Constants.NAME)
        artist_name = album_json.get(Constants.ARTIST)
        track_path = get_track_path(album_path, track_name)
        track_json = get_track_dir_json(track_path, track_name, artist_name, album_name)
        track_number = track_json.get(Constants.TRACK_NUMBER) or 1
        description = track_json.get(Constants.DESCRIPTION)
        collaborators = track_json.get(Constants.COLLABORATORS)
        return cls(
            track_path,
            track_name,
            track_number,
            artist_name,
            album_name,
            description=description,
            collaborators=collaborators,
        )

    def init_dir(self):
        """Initialize the track directory with the default files."""
        init_track_dir(self.path, self.name, self.artist, self.album)

    def to_json_for_track_dir(self):
        """Convert this object to JSON for the file in the track directory."""
        return {
            Constants.ARTIST: self.artist,
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }

    def update(self, track_number=None, description=None, collaborators=None):
        self.track_number = track_number or self.track_number
        self.description = description or self.description
        self.collaborators = collaborators or self.collaborators
        self.save_track_metadata()

    def save_track_metadata(self):
        """Save this instance's data to the file in the track directory."""
        remove_file_if_exists(self.dir_json_path)
        full_json = self.to_json_for_track_dir()
        save_json_as(self.dir_json_path, full_json)
        return self
