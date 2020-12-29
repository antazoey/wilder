from wilder.constants import COLLABORATORS
from wilder.constants import DESCRIPTION
from wilder.constants import NAME
from wilder.constants import TRACK_NUMBER


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

    @property
    def json(self):
        return {
            NAME: self.name,
            DESCRIPTION: self.description,
            TRACK_NUMBER: self.track_number,
            COLLABORATORS: self.collaborators,
        }
