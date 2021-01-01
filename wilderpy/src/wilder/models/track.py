from wilder.constants import Constants


class Track:
    # The name of the track.
    name = None

    # The description of the track.
    description = None

    # The track number on the album it appears on.
    track_number = None

    # The .flp file.
    proj_file = None

    # Relational
    album = None

    # The artist of the track.
    artist = None

    # Additional collaborators on the track.
    collaborators = []

    @classmethod
    def from_json(cls, artist_name, album_name, track_json):
        track = cls()
        track.artist = artist_name
        track.album = album_name
        track.name = track_json.get(Constants.NAME)
        track.description = track_json.get(Constants.DESCRIPTION)
        track.track_number = track_json.get(Constants.TRACK_NUMBER)
        track.collaborators = track_json.get(Constants.COLLABORATORS)
        return track

    def to_json(self):
        return {
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }
