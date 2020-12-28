class Mgmt:
    artists = []

    def __init__(self, artists):
        self.artists = artists

    def dumps(self):
        return {"artists": [a.dumps() for a in self.artists]}
