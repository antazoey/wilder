class Artist:
    name = None
    bio = None

    # Relational
    discography = []

    def __init__(self, name=None):
        self.name = name

    @property
    def data(self):
        return {"name": self.name, "bio": self.bio, "discography": self.discography}
