from wilder.constants import COLLABORATORS
from wilder.constants import DESCRIPTION
from wilder.constants import NAME
from wilder.constants import TRACK_NUMBER


class Track:
    name = None
    description = None
    track_number = None

    # Relational
    album = None
    artist = None
    collaborators = []

    @property
    def json(self):
        return {
            NAME: self.name,
            DESCRIPTION: self.description,
            TRACK_NUMBER: self.track_number,
            COLLABORATORS: self.collaborators,
        }
