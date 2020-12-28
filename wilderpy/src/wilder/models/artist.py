from wilder.constants import BIO
from wilder.constants import DISCOGRAPHY
from wilder.constants import NAME


class Artist:
    name = None
    bio = None

    # Relational
    discography = []

    def __init__(self, name=None):
        self.name = name

    @property
    def json(self):
        return {
            NAME: self.name,
            BIO: self.bio,
            DISCOGRAPHY: [a.json for a in self.discography],
        }
